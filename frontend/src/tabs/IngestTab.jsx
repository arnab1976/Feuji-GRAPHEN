import { useRef, useState } from "react";
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  LinearProgress,
  Chip,
  Stack,
} from "@mui/material";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import RocketLaunchIcon from "@mui/icons-material/RocketLaunch";
import { DataGrid } from "@mui/x-data-grid";
import api from "../api.js";

const RESULT_COLS = [
  { field: "file", headerName: "File", flex: 1.4, minWidth: 180 },
  { field: "lease_id", headerName: "Lease ID", flex: 1, minWidth: 120 },
  { field: "tenant", headerName: "Tenant", flex: 1.2, minWidth: 140 },
  { field: "address", headerName: "Property", flex: 1.4, minWidth: 160 },
  {
    field: "status",
    headerName: "Status",
    width: 130,
    renderCell: (p) =>
      p.value === "success" ? (
        <Chip label="Ingested" color="success" size="small" />
      ) : (
        <Chip label="Failed" color="error" size="small" title={p.row.error} />
      ),
  },
];

export default function IngestTab({ onDataChanged }) {
  const [files, setFiles] = useState([]);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const inputRef = useRef(null);

  const pick = (e) => {
    setFiles(Array.from(e.target.files || []));
    setResults([]);
    setError(null);
  };

  const process = async () => {
    setBusy(true);
    setError(null);
    const out = [];
    for (let i = 0; i < files.length; i++) {
      const f = files[i];
      try {
        const r = await api.ingest(f, (ev) => {
          const pct = ev.total ? ev.loaded / ev.total : 0;
          setProgress(((i + pct) / files.length) * 100);
        });
        out.push({
          id: `${i}`,
          file: f.name,
          lease_id: r.lease_id,
          tenant: r.extracted?.tenant_name || "Unknown",
          address: r.extracted?.property_address || "Unknown",
          status: "success",
        });
      } catch (ex) {
        out.push({
          id: `${i}`,
          file: f.name,
          lease_id: "—",
          tenant: "—",
          address: "—",
          status: "failed",
          error: ex?.response?.data?.detail || ex.message,
        });
      }
      setProgress(((i + 1) / files.length) * 100);
    }
    setResults(out);
    setBusy(false);
    onDataChanged?.();
  };

  const okCount = results.filter((r) => r.status === "success").length;

  return (
    <Stack spacing={2}>
      <Typography variant="h4">Upload &amp; Process Lease Documents</Typography>
      <Alert severity="info">
        Upload commercial lease PDFs, Word docs, CSV, or Excel files. Documents go through NLP + LLM;
        spreadsheets map columns (tenant, property, dates, rent, sqft) directly into Neo4j.
      </Alert>

      <Card>
        <CardContent>
          <input
            ref={inputRef}
            type="file"
            accept="application/pdf,.pdf,.doc,.docx,.csv,.xlsx,.xls,application/vnd.ms-excel,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,text/csv"
            multiple
            hidden
            onChange={pick}
          />
          <Stack
            direction={{ xs: "column", sm: "row" }}
            spacing={2}
            alignItems={{ sm: "center" }}
          >
            <Button
              variant="outlined"
              startIcon={<CloudUploadIcon />}
              onClick={() => inputRef.current?.click()}
              disabled={busy}
            >
              Choose PDF / Word / CSV / Excel
            </Button>
            <Typography variant="body2" color="text.secondary">
              {files.length
                ? `${files.length} file(s) selected: ${files
                    .map((f) => f.name)
                    .join(", ")}`
                : "No files selected"}
            </Typography>
            <Box sx={{ flexGrow: 1 }} />
            <Button
              variant="contained"
              startIcon={<RocketLaunchIcon />}
              onClick={process}
              disabled={busy || files.length === 0}
            >
              Process uploaded files
            </Button>
          </Stack>

          {busy && (
            <Box sx={{ mt: 2 }}>
              <LinearProgress variant="determinate" value={progress} />
              <Typography variant="caption" color="text.secondary">
                Processing… {Math.round(progress)}%
              </Typography>
            </Box>
          )}
        </CardContent>
      </Card>

      {error && <Alert severity="error">{error}</Alert>}

      {results.length > 0 && (
        <>
          <Alert severity={okCount ? "success" : "warning"}>
            Processed {okCount} of {results.length} lease(s).
          </Alert>
          <Card>
            <DataGrid
              autoHeight
              rows={results}
              columns={RESULT_COLS}
              hideFooter={results.length <= 100}
              disableRowSelectionOnClick
            />
          </Card>
        </>
      )}
    </Stack>
  );
}
