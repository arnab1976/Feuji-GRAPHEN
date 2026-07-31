import { useState } from "react";
import {
  Stack,
  Typography,
  Alert,
  Card,
  CardContent,
  TextField,
  Button,
  MenuItem,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Box,
  CircularProgress,
  Chip,
} from "@mui/material";
import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import SearchIcon from "@mui/icons-material/Search";
import { DataGrid } from "@mui/x-data-grid";
import api from "../api.js";

const EXAMPLES = [
  "Which leases expire in the next 90 days?",
  "Which tenant has the highest concentration risk?",
  "Are there any high-risk termination clauses?",
  "What is the average rent PSF across the portfolio?",
  "Show me all NNN leases in Austin",
  "Give me a portfolio summary",
];

export default function AskTab() {
  const [question, setQuestion] = useState("");
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const ask = async () => {
    if (!question.trim()) return;
    setBusy(true);
    setError(null);
    setResult(null);
    try {
      setResult(await api.ask(question.trim()));
    } catch (ex) {
      setError(ex?.response?.data?.detail || ex.message);
    } finally {
      setBusy(false);
    }
  };

  const graphRows = (result?.graph_context || []).map((r, i) => ({ id: i, ...r }));
  const graphCols =
    graphRows.length > 0
      ? Object.keys(result.graph_context[0]).map((k) => ({
          field: k,
          headerName: k,
          flex: 1,
          minWidth: 120,
        }))
      : [];

  return (
    <Stack spacing={2}>
      <Typography variant="h4">Ask About Your Lease Portfolio</Typography>
      <Alert severity="info">
        Every answer is grounded in the Neo4j knowledge graph — not raw document text.
        The AI cites specific graph nodes and document chunks for every claim.
      </Alert>

      <Card>
        <CardContent>
          <Stack spacing={2}>
            <TextField
              select
              label="Example questions"
              value=""
              onChange={(e) => setQuestion(e.target.value)}
              fullWidth
            >
              <MenuItem value="">— custom question —</MenuItem>
              {EXAMPLES.map((ex) => (
                <MenuItem key={ex} value={ex}>
                  {ex}
                </MenuItem>
              ))}
            </TextField>
            <TextField
              label="Your question"
              placeholder="e.g. Which leases expire in the next 90 days?"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && ask()}
              fullWidth
              multiline
              maxRows={3}
            />
            <Box>
              <Button
                variant="contained"
                startIcon={busy ? <CircularProgress size={18} color="inherit" /> : <SearchIcon />}
                onClick={ask}
                disabled={busy || !question.trim()}
              >
                {busy ? "Querying…" : "Ask"}
              </Button>
            </Box>
          </Stack>
        </CardContent>
      </Card>

      {error && <Alert severity="error">{error}</Alert>}

      {result && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              💡 Answer
            </Typography>
            <Typography sx={{ whiteSpace: "pre-wrap", lineHeight: 1.7 }}>
              {result.answer}
            </Typography>

            <Box sx={{ mt: 2 }}>
              <Accordion disableGutters>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Chip size="small" color="info" label={`Graph context · ${graphRows.length} rows`} />
                </AccordionSummary>
                <AccordionDetails>
                  {graphRows.length ? (
                    <DataGrid
                      autoHeight
                      density="compact"
                      rows={graphRows}
                      columns={graphCols}
                      hideFooter={graphRows.length <= 100}
                      disableRowSelectionOnClick
                    />
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      No graph rows retrieved.
                    </Typography>
                  )}
                </AccordionDetails>
              </Accordion>

              <Accordion disableGutters>
                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                  <Chip
                    size="small"
                    color="secondary"
                    label={`Document context · ${(result.doc_context || []).length} chunks`}
                  />
                </AccordionSummary>
                <AccordionDetails>
                  <Stack spacing={1.5}>
                    {(result.doc_context || []).map((c, i) => (
                      <Box key={i}>
                        <Typography variant="caption" color="text.secondary">
                          {c.source || "chunk"} — score {Number(c.score || 0).toFixed(3)}
                        </Typography>
                        <Box
                          component="pre"
                          sx={{
                            whiteSpace: "pre-wrap",
                            fontSize: 12,
                            bgcolor: "action.hover",
                            p: 1.5,
                            borderRadius: 1,
                            m: 0,
                          }}
                        >
                          {(c.text || "").slice(0, 400)}
                        </Box>
                      </Box>
                    ))}
                    {!(result.doc_context || []).length && (
                      <Typography variant="body2" color="text.secondary">
                        No document chunks retrieved.
                      </Typography>
                    )}
                  </Stack>
                </AccordionDetails>
              </Accordion>
            </Box>
          </CardContent>
        </Card>
      )}
    </Stack>
  );
}
