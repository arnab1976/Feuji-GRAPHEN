import os
import sqlite3
import json
from loguru import logger
from datetime import datetime

# Optional: Attempt to use psycopg2 if available and DATABASE_URL is set
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False

DATABASE_URL = os.environ.get("DATABASE_URL")

class DBClient:
    def __init__(self):
        self.use_postgres = HAS_POSTGRES and DATABASE_URL
        if self.use_postgres:
            logger.info("Using PostgreSQL for file tracking.")
            self._init_postgres()
        else:
            logger.warning("PostgreSQL not configured or psycopg2 missing. Falling back to SQLite.")
            self.sqlite_db = os.path.join(os.path.dirname(__file__), "..", "data", "tracking.db")
            os.makedirs(os.path.dirname(self.sqlite_db), exist_ok=True)
            self._init_sqlite()

    def _init_postgres(self):
        try:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS upload_sessions (
                            tracking_id VARCHAR(255) PRIMARY KEY,
                            scenario_tracking_id VARCHAR(255),
                            industry VARCHAR(255),
                            use_case VARCHAR(255),
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    cur.execute(
                        "ALTER TABLE upload_sessions ADD COLUMN IF NOT EXISTS "
                        "scenario_tracking_id VARCHAR(255)"
                    )
                    cur.execute(
                        "ALTER TABLE upload_sessions ADD COLUMN IF NOT EXISTS industry VARCHAR(255)"
                    )
                    cur.execute(
                        "ALTER TABLE upload_sessions ADD COLUMN IF NOT EXISTS use_case VARCHAR(255)"
                    )
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS uploaded_files (
                            id SERIAL PRIMARY KEY,
                            tracking_id VARCHAR(255) REFERENCES upload_sessions(tracking_id),
                            filename VARCHAR(255),
                            content_type VARCHAR(100),
                            file_data BYTEA,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS validation_runs (
                            run_id VARCHAR(64) PRIMARY KEY,
                            tracking_id VARCHAR(255),
                            scenario_id VARCHAR(255),
                            domain VARCHAR(255),
                            use_case VARCHAR(255),
                            snapshot_hash VARCHAR(64),
                            overall_score DOUBLE PRECISION,
                            overall_zone VARCHAR(16),
                            required_layer_failure BOOLEAN DEFAULT FALSE,
                            status VARCHAR(32) DEFAULT 'completed',
                            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                        );
                    """)
                    cur.execute("""
                        CREATE TABLE IF NOT EXISTS validation_layer_results (
                            id SERIAL PRIMARY KEY,
                            run_id VARCHAR(64) REFERENCES validation_runs(run_id) ON DELETE CASCADE,
                            layer_id VARCHAR(8),
                            layer_order INTEGER,
                            name VARCHAR(255),
                            score DOUBLE PRECISION,
                            zone VARCHAR(16),
                            hard_failure BOOLEAN DEFAULT FALSE,
                            checks_passed INTEGER,
                            checks_total INTEGER,
                            summary TEXT,
                            remediation TEXT,
                            details_json TEXT,
                            duration_ms DOUBLE PRECISION,
                            UNIQUE(run_id, layer_id)
                        );
                    """)
                    cur.execute(
                        "CREATE INDEX IF NOT EXISTS idx_validation_context "
                        "ON validation_runs(tracking_id, scenario_id, started_at DESC)"
                    )
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to initialize PostgreSQL: {e}")
            self.use_postgres = False
            self.sqlite_db = os.path.join(os.path.dirname(__file__), "..", "data", "tracking.db")
            os.makedirs(os.path.dirname(self.sqlite_db), exist_ok=True)
            self._init_sqlite()

    def _init_sqlite(self):
        with sqlite3.connect(self.sqlite_db) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS upload_sessions (
                    tracking_id TEXT PRIMARY KEY,
                    scenario_tracking_id TEXT,
                    industry TEXT,
                    use_case TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS uploaded_files (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tracking_id TEXT REFERENCES upload_sessions(tracking_id),
                    filename TEXT,
                    content_type TEXT,
                    file_data BLOB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS validation_runs (
                    run_id TEXT PRIMARY KEY,
                    tracking_id TEXT,
                    scenario_id TEXT,
                    domain TEXT,
                    use_case TEXT,
                    snapshot_hash TEXT,
                    overall_score REAL,
                    overall_zone TEXT,
                    required_layer_failure INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'completed',
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS validation_layer_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT,
                    layer_id TEXT,
                    layer_order INTEGER,
                    name TEXT,
                    score REAL,
                    zone TEXT,
                    hard_failure INTEGER DEFAULT 0,
                    checks_passed INTEGER,
                    checks_total INTEGER,
                    summary TEXT,
                    remediation TEXT,
                    details_json TEXT,
                    duration_ms REAL,
                    UNIQUE(run_id, layer_id)
                );
            """)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_validation_context "
                "ON validation_runs(tracking_id, scenario_id, started_at DESC)"
            )
            columns = {
                row[1] for row in conn.execute("PRAGMA table_info(upload_sessions)").fetchall()
            }
            for column in ("scenario_tracking_id", "industry", "use_case"):
                if column not in columns:
                    conn.execute(
                        f"ALTER TABLE upload_sessions ADD COLUMN {column} TEXT"
                    )

    def create_session(
        self,
        tracking_id: str,
        scenario_tracking_id: str = "",
        industry: str = "",
        use_case: str = "",
    ):
        if self.use_postgres:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO upload_sessions
                            (tracking_id, scenario_tracking_id, industry, use_case)
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (tracking_id) DO UPDATE SET
                            scenario_tracking_id = COALESCE(NULLIF(EXCLUDED.scenario_tracking_id, ''), upload_sessions.scenario_tracking_id),
                            industry = COALESCE(NULLIF(EXCLUDED.industry, ''), upload_sessions.industry),
                            use_case = COALESCE(NULLIF(EXCLUDED.use_case, ''), upload_sessions.use_case)
                        """,
                        (tracking_id, scenario_tracking_id, industry, use_case),
                    )
                conn.commit()
        else:
            with sqlite3.connect(self.sqlite_db) as conn:
                conn.execute(
                    """
                    INSERT OR IGNORE INTO upload_sessions
                        (tracking_id, scenario_tracking_id, industry, use_case)
                    VALUES (?, ?, ?, ?)
                    """,
                    (tracking_id, scenario_tracking_id, industry, use_case),
                )
                conn.execute(
                    """
                    UPDATE upload_sessions SET
                        scenario_tracking_id = CASE WHEN ? <> '' THEN ? ELSE scenario_tracking_id END,
                        industry = CASE WHEN ? <> '' THEN ? ELSE industry END,
                        use_case = CASE WHEN ? <> '' THEN ? ELSE use_case END
                    WHERE tracking_id = ?
                    """,
                    (
                        scenario_tracking_id, scenario_tracking_id,
                        industry, industry,
                        use_case, use_case,
                        tracking_id,
                    ),
                )

    def save_file(self, tracking_id: str, filename: str, content_type: str, file_data: bytes):
        if self.use_postgres:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "INSERT INTO uploaded_files (tracking_id, filename, content_type, file_data) VALUES (%s, %s, %s, %s)",
                        (tracking_id, filename, content_type, psycopg2.Binary(file_data)),
                    )
                conn.commit()
        else:
            with sqlite3.connect(self.sqlite_db) as conn:
                conn.execute(
                    "INSERT INTO uploaded_files (tracking_id, filename, content_type, file_data) VALUES (?, ?, ?, ?)",
                    (tracking_id, filename, content_type, sqlite3.Binary(file_data)),
                )

    def get_recent_sessions(self, limit: int = 5):
        if self.use_postgres:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(
                        """
                        SELECT s.tracking_id,
                               s.scenario_tracking_id,
                               s.industry,
                               s.use_case,
                               s.created_at,
                               COALESCE(COUNT(f.id), 0) AS file_count
                        FROM upload_sessions s
                        LEFT JOIN uploaded_files f ON f.tracking_id = s.tracking_id
                        GROUP BY s.tracking_id, s.scenario_tracking_id, s.industry, s.use_case, s.created_at
                        ORDER BY s.created_at DESC
                        LIMIT %s
                        """,
                        (limit,),
                    )
                    rows = [dict(r) for r in cur.fetchall()]
                    for r in rows:
                        if r.get("created_at") is not None:
                            r["created_at"] = str(r["created_at"])
                        r["file_count"] = int(r.get("file_count") or 0)
                    return rows
        else:
            with sqlite3.connect(self.sqlite_db) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute(
                    """
                    SELECT s.tracking_id,
                           s.scenario_tracking_id,
                           s.industry,
                           s.use_case,
                           s.created_at,
                           COALESCE(COUNT(f.id), 0) AS file_count
                    FROM upload_sessions s
                    LEFT JOIN uploaded_files f ON f.tracking_id = s.tracking_id
                    GROUP BY s.tracking_id
                    ORDER BY s.created_at DESC
                    LIMIT ?
                    """,
                    (limit,),
                )
                rows = [dict(r) for r in cur.fetchall()]
                for r in rows:
                    if r.get("created_at") is not None:
                        r["created_at"] = str(r["created_at"])
                    r["file_count"] = int(r.get("file_count") or 0)
                return rows

    def get_session(self, tracking_id: str):
        columns = (
            "tracking_id, scenario_tracking_id, industry, use_case, created_at"
        )
        if self.use_postgres:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(
                        f"SELECT {columns} FROM upload_sessions WHERE tracking_id = %s",
                        (tracking_id,),
                    )
                    row = cur.fetchone()
                    return dict(row) if row else None
        with sqlite3.connect(self.sqlite_db) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                f"SELECT {columns} FROM upload_sessions WHERE tracking_id = ?",
                (tracking_id,),
            ).fetchone()
            return dict(row) if row else None

    def delete_session(self, tracking_id: str):
        """Delete one upload session and all files owned by it."""
        if self.use_postgres:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "SELECT COUNT(*) FROM uploaded_files WHERE tracking_id = %s",
                        (tracking_id,),
                    )
                    file_count = int(cur.fetchone()[0] or 0)
                    cur.execute(
                        "DELETE FROM uploaded_files WHERE tracking_id = %s",
                        (tracking_id,),
                    )
                    cur.execute(
                        "DELETE FROM upload_sessions WHERE tracking_id = %s",
                        (tracking_id,),
                    )
                    deleted = cur.rowcount > 0
                conn.commit()
                return {"deleted": deleted, "file_count": file_count}
        with sqlite3.connect(self.sqlite_db) as conn:
            file_count = int(conn.execute(
                "SELECT COUNT(*) FROM uploaded_files WHERE tracking_id = ?",
                (tracking_id,),
            ).fetchone()[0] or 0)
            conn.execute(
                "DELETE FROM uploaded_files WHERE tracking_id = ?",
                (tracking_id,),
            )
            cursor = conn.execute(
                "DELETE FROM upload_sessions WHERE tracking_id = ?",
                (tracking_id,),
            )
            return {"deleted": cursor.rowcount > 0, "file_count": file_count}


    def get_files_for_session(self, tracking_id: str):
        if self.use_postgres:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("SELECT id, filename, content_type FROM uploaded_files WHERE tracking_id = %s", (tracking_id,))
                    return [dict(r) for r in cur.fetchall()]
        else:
            with sqlite3.connect(self.sqlite_db) as conn:
                conn.row_factory = sqlite3.Row
                cur = conn.cursor()
                cur.execute("SELECT id, filename, content_type FROM uploaded_files WHERE tracking_id = ?", (tracking_id,))
                return [dict(r) for r in cur.fetchall()]

    def get_file_content(self, file_id: int):
        if self.use_postgres:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT filename, content_type, file_data FROM uploaded_files WHERE id = %s", (file_id,))
                    res = cur.fetchone()
                    if res:
                        return {"filename": res[0], "content_type": res[1], "file_data": res[2]}
        else:
            with sqlite3.connect(self.sqlite_db) as conn:
                cur = conn.cursor()
                cur.execute("SELECT filename, content_type, file_data FROM uploaded_files WHERE id = ?", (file_id,))
                res = cur.fetchone()
                if res:
                    return {"filename": res[0], "content_type": res[1], "file_data": res[2]}
        return None

    def get_validation_contexts(self, limit: int = 100):
        """Return persisted upload contexts available to Control Tower."""
        return self.get_recent_sessions(limit=max(1, min(int(limit), 500)))

    @staticmethod
    def _decode_validation_run(row, layer_rows=None):
        if not row:
            return None
        payload = dict(row)
        for key in ("started_at", "completed_at"):
            if payload.get(key) is not None:
                payload[key] = str(payload[key])
        payload["overall_score"] = float(payload.get("overall_score") or 0)
        payload["required_layer_failure"] = bool(payload.get("required_layer_failure"))
        if layer_rows is not None:
            layers = []
            for layer_row in layer_rows:
                layer = dict(layer_row)
                details = layer.pop("details_json", None)
                try:
                    detail_payload = json.loads(details or "{}")
                except (TypeError, json.JSONDecodeError):
                    detail_payload = {}
                layer.update(detail_payload)
                layer["score"] = float(layer.get("score") or 0)
                layer["hard_failure"] = bool(layer.get("hard_failure"))
                layers.append(layer)
            payload["layers"] = layers
            payload["summary"] = {
                zone: sum(1 for layer in layers if layer.get("zone") == zone)
                for zone in ("green", "amber", "red")
            }
        return payload

    def save_validation_run(self, run_id: str, result: dict):
        context = result.get("context") or {}
        run_values = (
            run_id,
            context.get("tracking_id") or "",
            context.get("scenario_id") or "",
            context.get("domain") or "",
            context.get("use_case") or "",
            result.get("snapshot_hash") or "",
            float(result.get("overall_score") or 0),
            result.get("overall_zone") or "red",
            bool(result.get("required_layer_failure")),
            "completed",
        )
        if self.use_postgres:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO validation_runs
                            (run_id, tracking_id, scenario_id, domain, use_case,
                             snapshot_hash, overall_score, overall_zone,
                             required_layer_failure, status, completed_at)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP)
                        """,
                        run_values,
                    )
                    for order, layer in enumerate(result.get("layers") or [], start=1):
                        cur.execute(
                            """
                            INSERT INTO validation_layer_results
                                (run_id, layer_id, layer_order, name, score, zone,
                                 hard_failure, checks_passed, checks_total, summary,
                                 remediation, details_json, duration_ms)
                            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            """,
                            (
                                run_id, layer.get("layer_id"), order, layer.get("name"),
                                float(layer.get("score") or 0), layer.get("zone"),
                                bool(layer.get("hard_failure")),
                                int(layer.get("checks_passed") or 0),
                                int(layer.get("checks_total") or 0),
                                layer.get("summary") or "",
                                layer.get("remediation") or "",
                                json.dumps({"checks": layer.get("checks") or []}),
                                float(layer.get("duration_ms") or 0),
                            ),
                        )
                conn.commit()
        else:
            with sqlite3.connect(self.sqlite_db) as conn:
                conn.execute(
                    """
                    INSERT INTO validation_runs
                        (run_id, tracking_id, scenario_id, domain, use_case,
                         snapshot_hash, overall_score, overall_zone,
                         required_layer_failure, status, completed_at)
                    VALUES (?,?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)
                    """,
                    run_values,
                )
                for order, layer in enumerate(result.get("layers") or [], start=1):
                    conn.execute(
                        """
                        INSERT INTO validation_layer_results
                            (run_id, layer_id, layer_order, name, score, zone,
                             hard_failure, checks_passed, checks_total, summary,
                             remediation, details_json, duration_ms)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """,
                        (
                            run_id, layer.get("layer_id"), order, layer.get("name"),
                            float(layer.get("score") or 0), layer.get("zone"),
                            int(bool(layer.get("hard_failure"))),
                            int(layer.get("checks_passed") or 0),
                            int(layer.get("checks_total") or 0),
                            layer.get("summary") or "",
                            layer.get("remediation") or "",
                            json.dumps({"checks": layer.get("checks") or []}),
                            float(layer.get("duration_ms") or 0),
                        ),
                    )
        return self.get_validation_run(run_id)

    def get_validation_run(self, run_id: str):
        if self.use_postgres:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute("SELECT * FROM validation_runs WHERE run_id = %s", (run_id,))
                    row = cur.fetchone()
                    if not row:
                        return None
                    cur.execute(
                        "SELECT * FROM validation_layer_results WHERE run_id = %s ORDER BY layer_order",
                        (run_id,),
                    )
                    return self._decode_validation_run(row, cur.fetchall())
        with sqlite3.connect(self.sqlite_db) as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                "SELECT * FROM validation_runs WHERE run_id = ?", (run_id,)
            ).fetchone()
            if not row:
                return None
            layers = conn.execute(
                "SELECT * FROM validation_layer_results WHERE run_id = ? ORDER BY layer_order",
                (run_id,),
            ).fetchall()
            return self._decode_validation_run(row, layers)

    def list_validation_runs(
        self,
        limit: int = 25,
        tracking_id: str = "",
        scenario_id: str = "",
        domain: str = "",
        use_case: str = "",
    ):
        filters = {
            "tracking_id": tracking_id,
            "scenario_id": scenario_id,
            "domain": domain,
            "use_case": use_case,
        }
        where = [f"{key} = %s" for key, value in filters.items() if value] if self.use_postgres else [
            f"{key} = ?" for key, value in filters.items() if value
        ]
        values = [value for value in filters.values() if value]
        clause = f" WHERE {' AND '.join(where)}" if where else ""
        capped = max(1, min(int(limit), 200))
        if self.use_postgres:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cur:
                    cur.execute(
                        f"SELECT * FROM validation_runs{clause} ORDER BY started_at DESC LIMIT %s",
                        (*values, capped),
                    )
                    return [self._decode_validation_run(row) for row in cur.fetchall()]
        with sqlite3.connect(self.sqlite_db) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                f"SELECT * FROM validation_runs{clause} ORDER BY started_at DESC LIMIT ?",
                (*values, capped),
            ).fetchall()
            return [self._decode_validation_run(row) for row in rows]

    def get_previous_validation_run(self, tracking_id: str, scenario_id: str):
        rows = self.list_validation_runs(
            limit=1, tracking_id=tracking_id, scenario_id=scenario_id
        )
        return rows[0] if rows else None

    def delete_validation_run(self, run_id: str):
        if self.use_postgres:
            with psycopg2.connect(DATABASE_URL) as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        "DELETE FROM validation_layer_results WHERE run_id = %s",
                        (run_id,),
                    )
                    cur.execute(
                        "DELETE FROM validation_runs WHERE run_id = %s",
                        (run_id,),
                    )
                    deleted = cur.rowcount > 0
                conn.commit()
                return deleted
        with sqlite3.connect(self.sqlite_db) as conn:
            conn.execute(
                "DELETE FROM validation_layer_results WHERE run_id = ?", (run_id,)
            )
            cursor = conn.execute(
                "DELETE FROM validation_runs WHERE run_id = ?", (run_id,)
            )
            return cursor.rowcount > 0

db_client = DBClient()
