import { useEffect, useState } from "react";
import {
  Box,
  Typography,
  Chip,
  Divider,
  Alert,
  CircularProgress,
  Grid,
  Paper,
  IconButton,
  Tooltip,
  Stack,
} from "@mui/material";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import ErrorIcon from "@mui/icons-material/Error";
import RefreshIcon from "@mui/icons-material/Refresh";
import api from "../api.js";

function Stat({ label, value }) {
  return (
    <Paper
      variant="outlined"
      sx={{ p: 1.25, textAlign: "center", borderRadius: 2, height: "100%" }}
    >
      <Typography variant="h6" sx={{ fontWeight: 700, lineHeight: 1.2 }}>
        {value}
      </Typography>
      <Typography variant="caption" color="text.secondary">
        {label}
      </Typography>
    </Paper>
  );
}

const STACK_CHIPS = [
  "Neo4j Community",
  "ChromaDB",
  "spaCy NER",
  "sentence-transformers",
  "Groq / Ollama",
];

export default function Sidebar({ refreshKey, onRefresh }) {
  const [health, setHealth] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let alive = true;
    setLoading(true);
    Promise.allSettled([api.health(), api.summary()]).then(
      ([h, s]) => {
        if (!alive) return;
        setHealth(h.status === "fulfilled" ? h.value : { neo4j: false });
        setStats(s.status === "fulfilled" ? s.value : null);
        setLoading(false);
      }
    );
    return () => {
      alive = false;
    };
  }, [refreshKey]);

  const neo4jOk = health?.neo4j;
  const fmt = (n) => (n == null ? 0 : Number(n).toLocaleString());
  const money = (n) => `$${Number(n || 0).toFixed(2)}`;

  return (
    <Box sx={{ p: 2, overflowY: "auto" }}>
      <Stack direction="row" alignItems="center" justifyContent="space-between">
        <Typography variant="overline" color="text.secondary">
          Connection
        </Typography>
        <Tooltip title="Refresh stats">
          <IconButton size="small" onClick={onRefresh}>
            <RefreshIcon fontSize="small" />
          </IconButton>
        </Tooltip>
      </Stack>

      {loading ? (
        <Box sx={{ display: "flex", justifyContent: "center", py: 2 }}>
          <CircularProgress size={22} />
        </Box>
      ) : neo4jOk ? (
        <Alert icon={<CheckCircleIcon fontSize="inherit" />} severity="success" sx={{ py: 0.25 }}>
          Neo4j connected
        </Alert>
      ) : (
        <Alert icon={<ErrorIcon fontSize="inherit" />} severity="error" sx={{ py: 0.25 }}>
          Neo4j not reachable — start it on localhost:7687
        </Alert>
      )}

      <Divider sx={{ my: 2 }} />
      <Typography variant="overline" color="text.secondary">
        Portfolio at a glance
      </Typography>

      {stats ? (
        <Grid container spacing={1} sx={{ mt: 0.5 }}>
          <Grid item xs={6}>
            <Stat label="Leases" value={fmt(stats.lease_count)} />
          </Grid>
          <Grid item xs={6}>
            <Stat label="Properties" value={fmt(stats.property_count)} />
          </Grid>
          <Grid item xs={6}>
            <Stat label="Tenants" value={fmt(stats.tenant_count)} />
          </Grid>
          <Grid item xs={6}>
            <Stat label="Avg Rent PSF" value={money(stats.avg_rent_psf)} />
          </Grid>
          <Grid item xs={12}>
            <Stat label="Total Sqft" value={fmt(stats.total_sqft)} />
          </Grid>
          <Grid item xs={12}>
            <Alert severity="warning" sx={{ py: 0.25 }}>
              {fmt(stats.high_risk_clauses)} high-risk clauses
            </Alert>
          </Grid>
        </Grid>
      ) : (
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          Ingest leases to see portfolio stats.
        </Typography>
      )}

      <Divider sx={{ my: 2 }} />
      <Typography variant="overline" color="text.secondary">
        Free Stack
      </Typography>
      <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.75, mt: 1 }}>
        {STACK_CHIPS.map((c) => (
          <Chip key={c} label={c} size="small" variant="outlined" />
        ))}
      </Box>
    </Box>
  );
}
