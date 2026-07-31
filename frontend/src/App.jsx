import { useEffect, useMemo, useState } from "react";
import {
  Box,
  CssBaseline,
  ThemeProvider,
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Tabs,
  Tab,
  Drawer,
  Tooltip,
  useMediaQuery,
} from "@mui/material";
import ApartmentIcon from "@mui/icons-material/Apartment";
import DarkModeIcon from "@mui/icons-material/DarkMode";
import LightModeIcon from "@mui/icons-material/LightMode";
import MenuIcon from "@mui/icons-material/Menu";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import ChatIcon from "@mui/icons-material/Chat";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import HubIcon from "@mui/icons-material/Hub";
import DownloadIcon from "@mui/icons-material/Download";

import { makeTheme } from "./theme.js";
import Sidebar from "./components/Sidebar.jsx";
import IngestTab from "./tabs/IngestTab.jsx";
import AskTab from "./tabs/AskTab.jsx";
import RiskTab from "./tabs/RiskTab.jsx";
import GraphTab from "./tabs/GraphTab.jsx";
import ExportTab from "./tabs/ExportTab.jsx";

const DRAWER_WIDTH = 300;

const TABS = [
  { label: "Ingest Leases", icon: <UploadFileIcon />, El: IngestTab },
  { label: "Ask AI", icon: <ChatIcon />, El: AskTab },
  { label: "Risk Dashboard", icon: <WarningAmberIcon />, El: RiskTab },
  { label: "Knowledge Graph", icon: <HubIcon />, El: GraphTab },
  { label: "Export", icon: <DownloadIcon />, El: ExportTab },
];

export default function App() {
  const prefersDark = useMediaQuery("(prefers-color-scheme: dark)");
  const [mode, setMode] = useState("dark");
  const [tab, setTab] = useState(0);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0); // bump to reload sidebar stats
  const isDesktop = useMediaQuery("(min-width:900px)");

  useEffect(() => {
    setMode(prefersDark ? "dark" : "light");
  }, [prefersDark]);

  const theme = useMemo(() => makeTheme(mode), [mode]);
  const ActiveTab = TABS[tab].El;
  const bumpStats = () => setRefreshKey((k) => k + 1);

  const drawer = <Sidebar refreshKey={refreshKey} onRefresh={bumpStats} />;

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: "flex", minHeight: "100vh" }}>
        <AppBar
          position="fixed"
          color="default"
          sx={{
            zIndex: (t) => t.zIndex.drawer + 1,
            backdropFilter: "blur(8px)",
            backgroundColor: (t) =>
              t.palette.mode === "dark"
                ? "rgba(21,32,54,0.85)"
                : "rgba(255,255,255,0.85)",
            borderBottom: (t) => `1px solid ${t.palette.divider}`,
          }}
        >
          <Toolbar>
            {!isDesktop && (
              <IconButton
                edge="start"
                onClick={() => setMobileOpen((o) => !o)}
                sx={{ mr: 1 }}
              >
                <MenuIcon />
              </IconButton>
            )}
            <ApartmentIcon color="primary" sx={{ mr: 1 }} />
            <Typography variant="h6" sx={{ fontWeight: 700 }}>
              LeaseGuard
            </Typography>
            <Typography
              variant="caption"
              sx={{ ml: 1.5, opacity: 0.6, display: { xs: "none", sm: "block" } }}
            >
              Knowledge Graph Lease Intelligence · Material UI
            </Typography>
            <Box sx={{ flexGrow: 1 }} />
            <Tooltip title={mode === "dark" ? "Light theme" : "Dark theme"}>
              <IconButton
                onClick={() => setMode((m) => (m === "dark" ? "light" : "dark"))}
              >
                {mode === "dark" ? <LightModeIcon /> : <DarkModeIcon />}
              </IconButton>
            </Tooltip>
          </Toolbar>
        </AppBar>

        {/* Sidebar — permanent on desktop, temporary drawer on mobile */}
        <Box
          component="nav"
          sx={{ width: { md: DRAWER_WIDTH }, flexShrink: { md: 0 } }}
        >
          {isDesktop ? (
            <Drawer
              variant="permanent"
              open
              sx={{
                "& .MuiDrawer-paper": {
                  width: DRAWER_WIDTH,
                  boxSizing: "border-box",
                  borderRight: (t) => `1px solid ${t.palette.divider}`,
                },
              }}
            >
              <Toolbar />
              {drawer}
            </Drawer>
          ) : (
            <Drawer
              variant="temporary"
              open={mobileOpen}
              onClose={() => setMobileOpen(false)}
              ModalProps={{ keepMounted: true }}
              sx={{
                "& .MuiDrawer-paper": {
                  width: DRAWER_WIDTH,
                  boxSizing: "border-box",
                },
              }}
            >
              <Toolbar />
              {drawer}
            </Drawer>
          )}
        </Box>

        {/* Main content */}
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            width: { md: `calc(100% - ${DRAWER_WIDTH}px)` },
            bgcolor: "background.default",
          }}
        >
          <Toolbar />
          <Box
            sx={{
              borderBottom: 1,
              borderColor: "divider",
              px: { xs: 1, md: 3 },
              position: "sticky",
              top: 64,
              zIndex: 2,
              bgcolor: "background.default",
            }}
          >
            <Tabs
              value={tab}
              onChange={(_, v) => setTab(v)}
              variant="scrollable"
              scrollButtons="auto"
            >
              {TABS.map((t) => (
                <Tab key={t.label} icon={t.icon} iconPosition="start" label={t.label} />
              ))}
            </Tabs>
          </Box>
          <Box sx={{ p: { xs: 2, md: 3 } }}>
            <ActiveTab onDataChanged={bumpStats} />
          </Box>
        </Box>
      </Box>
    </ThemeProvider>
  );
}
