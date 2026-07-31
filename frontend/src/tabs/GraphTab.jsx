import { useEffect, useMemo, useRef, useState } from "react";
import {
  Stack,
  Typography,
  Alert,
  Card,
  CardContent,
  Button,
  Slider,
  Box,
  Chip,
  CircularProgress,
  TextField,
  useTheme,
} from "@mui/material";
import RefreshIcon from "@mui/icons-material/Refresh";
import DownloadIcon from "@mui/icons-material/Download";
import { DataGrid } from "@mui/x-data-grid";
import ForceGraph2D from "react-force-graph-2d";
import api from "../api.js";
import { NODE_COLORS } from "../theme.js";

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
  const headers = [
    "Lease ID",
    "Start Date",
    "End Date",
    "Rent PSF",
    "SqFt",
    "Annual Rent",
    "Lease Type",
    "Escalation %",
    "Property",
    "City",
    "State",
    "Property SqFt",
    "Property Note",
    "Tenant",
    "Industry",
    "Tenant Note",
    "Relationship",
    "Graph Edges",
    "Special Clauses",
    "Clause Details",
    "Renewal Options",
    "Termination Rights",
    "Source File",
  ];
  const esc = (v) => {
    const s = v == null ? "" : String(v);
    return /[",\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  return [
    headers.join(","),
    ...rows.map((r) =>
      [
        esc(r.lease_id),
        esc(r.start_date),
        esc(r.end_date),
        esc(r.rent_psf),
        esc(r.sqft),
        esc(r.annual_rent),
        esc(r.lease_type),
        esc(r.escalation_pct),
        esc(r.property),
        esc(r.city),
        esc(r.state),
        esc(r.property_sqft),
        esc(r.property_note || ""),
        esc(r.tenant),
        esc(r.industry),
        esc(r.tenant_note || ""),
        esc(r.relationship || ""),
        esc(Array.isArray(r.graph_edges) ? r.graph_edges.join("; ") : ""),
        esc(Array.isArray(r.special_clauses) ? r.special_clauses.join("; ") : ""),
        esc(Array.isArray(r.clause_details) ? r.clause_details.join(" | ") : ""),
        esc(Array.isArray(r.renewal_options) ? r.renewal_options.join(" | ") : ""),
        esc(Array.isArray(r.termination_rights) ? r.termination_rights.join(" | ") : ""),
        esc(r.source_file || ""),
      ].join(",")
    ),
  ].join("\n");
}

export default function GraphTab() {
  const theme = useTheme();
  const wrapRef = useRef(null);
  const [limit, setLimit] = useState(60);
  const [data, setData] = useState({ nodes: [], links: [] });
  const [rels, setRels] = useState([]);
  const [relFilter, setRelFilter] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [width, setWidth] = useState(800);

  useEffect(() => {
    const el = wrapRef.current;
    if (!el) return;
    const ro = new ResizeObserver((entries) => {
      setWidth(entries[0].contentRect.width);
    });
    ro.observe(el);
    return () => ro.disconnect();
  }, []);

  const render = async () => {
    setLoading(true);
    setError(null);
    try {
      const [g, relationships] = await Promise.all([
        api.graph(limit),
        api.relationships(1000).catch(() => []),
      ]);
      // Backend returns {nodes:[{id,label,type}], edges:[{from,to,label}]}.
      // react-force-graph wants links with source/target.
      setData({
        nodes: g.nodes,
        links: (g.edges || []).map((e) => ({
          source: e.from,
          target: e.to,
          label: e.label,
        })),
      });
      setRels(Array.isArray(relationships) ? relationships : []);
    } catch (ex) {
      setError(ex?.response?.data?.detail || ex.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    render();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const filteredRels = useMemo(() => {
    const q = relFilter.trim().toLowerCase();
    if (!q) return rels;
    return rels.filter((r) =>
      [
        r.lease_id,
        r.property,
        r.city,
        r.state,
        r.property_note,
        r.tenant,
        r.industry,
        r.tenant_note,
        r.lease_type,
        r.source_file,
        r.relationship,
        ...(r.special_clauses || []),
        ...(r.clause_details || []),
        ...(r.renewal_options || []),
        ...(r.termination_rights || []),
        ...(r.graph_edges || []),
      ]
        .join(" ")
        .toLowerCase()
        .includes(q)
    );
  }, [rels, relFilter]);

  const relCols = [
    { field: "lease_id", headerName: "Lease ID", width: 110 },
    { field: "property", headerName: "Property", flex: 1.1, minWidth: 160 },
    {
      field: "city_state",
      headerName: "City / State",
      width: 120,
      valueGetter: (_v, row) => [row.city, row.state].filter(Boolean).join(", "),
    },
    { field: "tenant", headerName: "Tenant", flex: 1, minWidth: 140 },
    { field: "industry", headerName: "Industry", width: 120 },
    { field: "start_date", headerName: "Start", width: 110 },
    { field: "end_date", headerName: "End", width: 110 },
    { field: "rent_psf", headerName: "Rent PSF", width: 100 },
    { field: "sqft", headerName: "SqFt", width: 90 },
    { field: "annual_rent", headerName: "Annual Rent", width: 120 },
    { field: "lease_type", headerName: "Lease Type", width: 120 },
    { field: "escalation_pct", headerName: "Escalation %", width: 110 },
    { field: "relationship", headerName: "Relationship path", flex: 1.2, minWidth: 260 },
    {
      field: "graph_edges",
      headerName: "Graph edges",
      width: 180,
      valueGetter: (_v, row) =>
        Array.isArray(row.graph_edges) ? row.graph_edges.join(", ") : "",
    },
    {
      field: "special_clauses",
      headerName: "Special clauses",
      flex: 1,
      minWidth: 160,
      valueGetter: (_v, row) =>
        Array.isArray(row.special_clauses) && row.special_clauses.length
          ? row.special_clauses.join(", ")
          : "None visible in graph",
    },
    {
      field: "renewal_options",
      headerName: "Renewal options",
      flex: 1,
      minWidth: 160,
      valueGetter: (_v, row) =>
        Array.isArray(row.renewal_options) ? row.renewal_options.join(" | ") : "",
    },
    {
      field: "termination_rights",
      headerName: "Termination rights",
      flex: 1,
      minWidth: 160,
      valueGetter: (_v, row) =>
        Array.isArray(row.termination_rights)
          ? row.termination_rights.join(" | ")
          : "",
    },
    { field: "source_file", headerName: "Source file", width: 150 },
  ];

  return (
    <Stack spacing={2}>
      <Typography variant="h4">🔗 Knowledge Graph Explorer</Typography>
      <Alert severity="info">
        Interactive visualisation of the Neo4j graph. Drag nodes to explore; scroll to
        zoom. Nodes are colour-coded by type.
      </Alert>

      <Box sx={{ display: "flex", gap: 1, flexWrap: "wrap" }}>
        {Object.entries(NODE_COLORS).map(([type, color]) => (
          <Chip
            key={type}
            label={type}
            size="small"
            sx={{ bgcolor: color, color: "#fff", fontWeight: 600 }}
          />
        ))}
      </Box>

      <Card>
        <CardContent>
          <Typography variant="body2" gutterBottom>
            Max nodes to display: {limit}
          </Typography>
          <Box sx={{ display: "flex", alignItems: "center", gap: 2, mb: 2 }}>
            <Slider
              value={limit}
              onChange={(_, v) => setLimit(v)}
              min={20}
              max={150}
              step={10}
              valueLabelDisplay="auto"
              sx={{ maxWidth: 300 }}
            />
            <Button
              variant="contained"
              startIcon={<RefreshIcon />}
              onClick={render}
              disabled={loading}
            >
              Render graph
            </Button>
          </Box>

          {error && <Alert severity="error">{error}</Alert>}

          <Box
            ref={wrapRef}
            sx={{
              height: 560,
              borderRadius: 2,
              overflow: "hidden",
              bgcolor: theme.palette.mode === "dark" ? "#0E1726" : "#f0f2f8",
              position: "relative",
            }}
          >
            {loading && (
              <Box
                sx={{
                  position: "absolute",
                  inset: 0,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  zIndex: 2,
                }}
              >
                <CircularProgress />
              </Box>
            )}
            {data.nodes.length > 0 && (
              <ForceGraph2D
                graphData={data}
                width={width}
                height={560}
                backgroundColor={theme.palette.mode === "dark" ? "#0E1726" : "#f0f2f8"}
                nodeColor={(n) => NODE_COLORS[n.type] || "#AAAAAA"}
                nodeLabel={(n) => `${n.type}: ${n.id}`}
                linkColor={() => (theme.palette.mode === "dark" ? "#334466" : "#c0c8d8")}
                linkDirectionalArrowLength={3}
                linkDirectionalArrowRelPos={1}
                nodeCanvasObjectMode={() => "after"}
                nodeCanvasObject={(node, ctx, scale) => {
                  const label = node.label || "";
                  const fontSize = 11 / scale;
                  ctx.font = `${fontSize}px Roboto, sans-serif`;
                  ctx.fillStyle =
                    theme.palette.mode === "dark" ? "#e8ecf5" : "#1a2233";
                  ctx.textAlign = "center";
                  ctx.textBaseline = "top";
                  ctx.fillText(label, node.x, node.y + 6);
                }}
              />
            )}
          </Box>
          {!loading && data.nodes.length === 0 && !error && (
            <Alert severity="info" sx={{ mt: 2 }}>
              No graph nodes yet — ingest some leases first.
            </Alert>
          )}
        </CardContent>
      </Card>

      <Card>
        <CardContent>
          <Stack
            direction={{ xs: "column", sm: "row" }}
            spacing={1.5}
            alignItems={{ sm: "center" }}
            justifyContent="space-between"
            sx={{ mb: 2 }}
          >
            <Box>
              <Typography variant="h6">Complete relationship table</Typography>
              <Typography variant="body2" color="text.secondary">
                Every connection in the graph as structured rows ({rels.length}{" "}
                leases)
              </Typography>
            </Box>
            <Stack direction="row" spacing={1}>
              <Button
                variant="contained"
                startIcon={<DownloadIcon />}
                disabled={!rels.length}
                onClick={() =>
                  download(
                    "knowledge_graph_relationships.csv",
                    toCsv(rels),
                    "text/csv;charset=utf-8"
                  )
                }
              >
                Download CSV
              </Button>
              <Button
                variant="outlined"
                startIcon={<DownloadIcon />}
                disabled={!rels.length}
                onClick={() =>
                  download(
                    "knowledge_graph_relationships.json",
                    JSON.stringify(rels, null, 2),
                    "application/json"
                  )
                }
              >
                Download JSON
              </Button>
            </Stack>
          </Stack>

          <TextField
            size="small"
            fullWidth
            placeholder="Filter by lease, property, tenant, or clause…"
            value={relFilter}
            onChange={(e) => setRelFilter(e.target.value)}
            sx={{ mb: 2, maxWidth: 480 }}
          />

          <Box sx={{ height: 420 }}>
            <DataGrid
              rows={filteredRels}
              columns={relCols}
              density="compact"
              pageSizeOptions={[25, 50, 100]}
              initialState={{ pagination: { paginationModel: { pageSize: 25 } } }}
              disableRowSelectionOnClick
            />
          </Box>
        </CardContent>
      </Card>
    </Stack>
  );
}
