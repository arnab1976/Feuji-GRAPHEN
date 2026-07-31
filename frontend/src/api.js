import axios from "axios";

// In dev, Vite proxies /api → http://localhost:8000 (see vite.config.js).
// In a production build served by FastAPI itself, same-origin /api also works.
const client = axios.create({ baseURL: "/api", timeout: 120000 });

export const api = {
  health: () => client.get("/health").then((r) => r.data),
  summary: () => client.get("/summary").then((r) => r.data),
  leases: (limit = 200) =>
    client.get("/leases", { params: { limit } }).then((r) => r.data),
  expiring: (days = 90) =>
    client.get("/expiring", { params: { days } }).then((r) => r.data),
  concentration: () => client.get("/concentration").then((r) => r.data),
  clauses: () => client.get("/clauses").then((r) => r.data),
  cities: () => client.get("/cities").then((r) => r.data),
  graph: (limit = 60) =>
    client.get("/graph", { params: { limit } }).then((r) => r.data),
  relationships: (limit = 1000) =>
    client.get("/relationships", { params: { limit } }).then((r) => r.data),
  ask: (question) => client.post("/ask", { question }).then((r) => r.data),
  portfolioReport: () =>
    client.get("/risk/portfolio/report").then((r) => r.data),
  ingest: (file, onProgress) => {
    const form = new FormData();
    form.append("file", file);
    return client
      .post("/ingest", form, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: onProgress,
      })
      .then((r) => r.data);
  },
};

export default api;
