"""Neo4j Community Edition — connection wrapper and raw Cypher execution."""
from __future__ import annotations
from typing import Any

from loguru import logger
from neo4j import GraphDatabase  # type: ignore

import leaseguard.config as cfg


class Neo4jClient:
    """Thread-safe wrapper around the official neo4j Python driver."""

    def __init__(
        self,
        uri:      str | None = None,
        user:     str | None = None,
        password: str | None = None,
        database: str | None = None,
    ) -> None:
        self._uri      = uri      or cfg.NEO4J_URI
        self._user     = user     or cfg.NEO4J_USER
        self._password = password or cfg.NEO4J_PASSWORD
        self._database = database or cfg.NEO4J_DATABASE
        self._driver   = GraphDatabase.driver(
            self._uri,
            auth=(self._user, self._password),
            # Fail fast when Neo4j is down instead of long retry loops that
            # flood the logs on every health-check poll.
            connection_timeout=5.0,
            connection_acquisition_timeout=5.0,
            max_transaction_retry_time=5.0,
        )
        logger.debug(f"Neo4jClient connected  uri={self._uri}")

    # ── Query execution ────────────────────────────────────────────────────

    def run(self, query: str, **params: Any) -> list[dict]:
        """Execute *query* and return results as a list of plain dicts."""
        with self._driver.session(database=self._database) as session:
            result = session.run(query, **params)
            return [dict(record) for record in result]

    def run_write(self, query: str, **params: Any) -> list[dict]:
        """Execute a write transaction."""
        with self._driver.session(database=self._database) as session:
            return session.execute_write(
                lambda tx: [dict(r) for r in tx.run(query, **params)]
            )

    # ── Helpers ────────────────────────────────────────────────────────────

    def ping(self) -> bool:
        """Return True if Neo4j is reachable, False otherwise."""
        try:
            self.run("RETURN 1 AS ok")
            return True
        except Exception as exc:
            logger.warning(f"Neo4j ping failed: {exc}")
            return False

    def node_counts(self) -> dict[str, int]:
        """Return count of nodes per label — useful for dashboard stats."""
        rows = self.run(
            "MATCH (n) RETURN labels(n)[0] AS lbl, count(n) AS cnt"
        )
        return {r["lbl"]: r["cnt"] for r in rows if r.get("lbl")}

    def close(self) -> None:
        self._driver.close()

    # ── Context manager ────────────────────────────────────────────────────

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()
