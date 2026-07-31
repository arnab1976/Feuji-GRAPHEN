import { useEffect, useState } from "react";
import {
  Stack,
  Typography,
  Card,
  CardContent,
  CardHeader,
  Grid,
  Button,
  Alert,
  ToggleButtonGroup,
  ToggleButton,
  Slider,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Chip,
  Box,
  CircularProgress,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import RefreshIcon from "@mui/icons-material/Refresh";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip as RTooltip,
  CartesianGrid,
} from "recharts";
import { DataGrid } from "@mui/x-data-grid";
import api from "../api.js";

export default function RiskTab() {
  const [days, setDays] = useState(90);
  const [threshold, setThreshold] = useState(25);
  const [expiring, setExpiring] = useState([]);
  const [conc, setConc] = useState([]);
  const [clauses, setClauses] = useState([]);
  const [report, setReport] = useState(null);
  const [reportBusy, setReportBusy] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = () => {
    setLoading(true);
    Promise.allSettled([api.expiring(days), api.concentration(), api.clauses()]).then(
      ([e, c, cl]) => {
        setExpiring(e.status === "fulfilled" ? e.value : []);
        setConc(c.status === "fulfilled" ? c.value : []);
        setClauses(cl.status === "fulfilled" ? cl.value : []);
        if (e.status === "rejected") setError("Could not load risk data — is Neo4j running?");
        setLoading(false);
      }
    );
  };

  useEffect(load, [days]);

  const genReport = async () => {
    setReportBusy(true);
    try {
      const r = await api.portfolioReport();
      setReport(r.report);
    } catch (ex) {
      setReport(`Report generation failed: ${ex?.response?.data?.detail || ex.message}`);
    } finally {
      setReportBusy(false);
    }
  };

  const expCols = [
    { field: "lease_id", headerName: "Lease", width: 110 },
    { field: "tenant", headerName: "Tenant", flex: 1, minWidth: 140 },
    { field: "property", headerName: "Property", flex: 1.3, minWidth: 160 },
    { field: "expiration_date", headerName: "Expires", width: 120 },
    { field: "sqft", headerName: "Sqft", width: 100 },
    { field: "annual_rent", headerName: "Annual Rent", width: 130 },
  ];
  const expRows = expiring.map((r, i) => ({ id: i, ...r }));

  const concCols = [
    { field: "tenant", headerName: "Tenant", flex: 1, minWidth: 150 },
    { field: "lease_count", headerName: "Leases", width: 90 },
    { field: "total_sqft", headerName: "Total Sqft", width: 130 },
    {
      field: "concentration_pct",
      headerName: "Share %",
      width: 110,
      renderCell: (p) => `${Number(p.value || 0).toFixed(1)}%`,
    },
    {
      field: "flag",
      headerName: "Flag",
      width: 80,
      renderCell: (p) =>
        Number(p.row.concentration_pct || 0) > threshold ? (
          <Chip label="⚠" color="warning" size="small" />
        ) : null,
    },
  ];
  const concRows = conc.map((r, i) => ({ id: i, ...r }));

  const chartData = expiring
    .filter((r) => r.sqft != null)
    .map((r) => ({ tenant: r.tenant, sqft: Number(r.sqft) }));

  return (
    <Stack spacing={2}>
      <Stack direction="row" alignItems="center" justifyContent="space-between">
        <Typography variant="h4">⚠️ Portfolio Risk Dashboard</Typography>
        <Button startIcon={<RefreshIcon />} onClick={load}>
          Refresh
        </Button>
      </Stack>
      <Typography variant="body2" color="text.secondary">
        All data sourced live from Neo4j graph traversals.
      </Typography>

      {error && <Alert severity="warning">{error}</Alert>}

      <Card>
        <CardHeader title="🗓️ Lease Expiration Risk" />
        <CardContent>
          <Typography variant="body2" gutterBottom>
            Show leases expiring within:
          </Typography>
          <ToggleButtonGroup
            exclusive
            size="small"
            value={days}
            onChange={(_, v) => v && setDays(v)}
            sx={{ mb: 2 }}
          >
            {[30, 60, 90, 180].map((d) => (
              <ToggleButton key={d} value={d}>
                {d} days
              </ToggleButton>
            ))}
          </ToggleButtonGroup>

          {loading ? (
            <Box sx={{ display: "flex", justifyContent: "center", py: 3 }}>
              <CircularProgress />
            </Box>
          ) : expRows.length ? (
            <>
              <Box sx={{ height: 260, mb: 2 }}>
                <ResponsiveContainer>
                  <BarChart data={chartData}>
                    <CartesianGrid strokeDasharray="3 3" opacity={0.2} />
                    <XAxis dataKey="tenant" hide />
                    <YAxis />
                    <RTooltip />
                    <Bar dataKey="sqft" fill="#6200EE" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </Box>
              <DataGrid
                autoHeight
                density="compact"
                rows={expRows}
                columns={expCols}
                hideFooter={expRows.length <= 100}
                disableRowSelectionOnClick
              />
            </>
          ) : (
            <Alert severity="success">No leases expire in the next {days} days.</Alert>
          )}
        </CardContent>
      </Card>

      <Grid container spacing={2}>
        <Grid item xs={12} md={6}>
          <Card sx={{ height: "100%" }}>
            <CardHeader title="👥 Tenant Concentration" />
            <CardContent>
              <Typography variant="body2" gutterBottom>
                Flag above: {threshold}%
              </Typography>
              <Slider
                value={threshold}
                onChange={(_, v) => setThreshold(v)}
                min={10}
                max={50}
                valueLabelDisplay="auto"
                sx={{ mb: 1 }}
              />
              {concRows.length ? (
                <DataGrid
                  autoHeight
                  density="compact"
                  rows={concRows}
                  columns={concCols}
                  hideFooter={concRows.length <= 100}
                  disableRowSelectionOnClick
                />
              ) : (
                <Typography variant="body2" color="text.secondary">
                  No concentration data.
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card sx={{ height: "100%" }}>
            <CardHeader title="🚨 High-Risk Clauses" />
            <CardContent>
              {clauses.length ? (
                clauses.slice(0, 8).map((c, i) => (
                  <Accordion key={i} disableGutters>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                      <Typography variant="body2" sx={{ fontWeight: 600 }}>
                        {c.lease_id} — {(c.property || "").slice(0, 35)}
                      </Typography>
                    </AccordionSummary>
                    <AccordionDetails>
                      <Typography variant="caption" color="text.secondary">
                        Tenant: {c.tenant}
                      </Typography>
                      <Typography variant="body2" sx={{ mt: 0.5 }}>
                        {c.clause_text}
                      </Typography>
                    </AccordionDetails>
                  </Accordion>
                ))
              ) : (
                <Alert severity="success">No high-risk clauses detected.</Alert>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      <Card>
        <CardHeader title="🤖 AI Portfolio Risk Report" />
        <CardContent>
          <Button
            variant="contained"
            onClick={genReport}
            disabled={reportBusy}
            startIcon={reportBusy ? <CircularProgress size={18} color="inherit" /> : null}
          >
            {reportBusy ? "Analysing…" : "Generate AI risk report"}
          </Button>
          {report && (
            <Typography sx={{ whiteSpace: "pre-wrap", mt: 2, lineHeight: 1.7 }}>
              {report}
            </Typography>
          )}
        </CardContent>
      </Card>
    </Stack>
  );
}
