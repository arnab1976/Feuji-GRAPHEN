import { useEffect, useState } from "react";
import {
  Stack,
  Typography,
  Card,
  CardContent,
  Button,
  Alert,
  Box,
  CircularProgress,
} from "@mui/material";
import DownloadIcon from "@mui/icons-material/Download";
import { DataGrid } from "@mui/x-data-grid";
import api from "../api.js";

function download(filename, text, type) {
  const blob = new Blob([text], { type });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

function toCsv(rows) {
  if (!rows.length) return "";
  const cols = Object.keys(rows[0]);
  const esc = (v) => {
    const s = v == null ? "" : String(v);
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  return [
    cols.join(","),
    ...rows.map((r) => cols.map((c) => esc(r[c])).join(",")),
  ].join("\n");
}

export default function ExportTab() {
  const [leases, setLeases] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    api
      .leases(500)
      .then(setLeases)
      .catch((ex) => setError(ex?.response?.data?.detail || ex.message))
      .finally(() => setLoading(false));
  }, []);

  const cols =
    leases.length > 0
      ? Object.keys(leases[0]).map((k) => ({
          field: k,
          headerName: k,
          flex: 1,
          minWidth: 130,
        }))
      : [];
  const rows = leases.map((r, i) => ({ id: i, ...r }));

  const exportSummary = async () => {
    const s = await api.summary();
    download(
      "portfolio_summary.json",
      JSON.stringify(s, null, 2),
      "application/json"
    );
  };

  return (
    <Stack spacing={2}>
      <Typography variant="h4">📊 Export Lease Data</Typography>

      {error && <Alert severity="error">{error}</Alert>}

      {loading ? (
        <Box sx={{ display: "flex", justifyContent: "center", py: 4 }}>
          <CircularProgress />
        </Box>
      ) : leases.length === 0 ? (
        <Alert severity="info">
          No leases to export yet — ingest some documents first.
        </Alert>
      ) : (
        <>
          <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5}>
            <Button
              variant="contained"
              startIcon={<DownloadIcon />}
              onClick={() =>
                download("leaseguard_leases.csv", toCsv(leases), "text/csv")
              }
            >
              Download CSV
            </Button>
            <Button
              variant="outlined"
              startIcon={<DownloadIcon />}
              onClick={() =>
                download(
                  "leaseguard_leases.json",
                  JSON.stringify(leases, null, 2),
                  "application/json"
                )
              }
            >
              Download JSON
            </Button>
            <Button
              variant="outlined"
              startIcon={<DownloadIcon />}
              onClick={exportSummary}
            >
              Portfolio Summary JSON
            </Button>
          </Stack>

          <Card>
            <CardContent sx={{ p: 0 }}>
              <DataGrid
                autoHeight
                density="compact"
                rows={rows}
                columns={cols}
                pageSizeOptions={[10, 25, 50]}
                initialState={{
                  pagination: { paginationModel: { pageSize: 25 } },
                }}
                disableRowSelectionOnClick
              />
            </CardContent>
          </Card>
        </>
      )}
    </Stack>
  );
}
