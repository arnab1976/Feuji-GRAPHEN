import { createTheme } from "@mui/material/styles";

// Semantic colours carried over from the Streamlit graph legend so the two
// front-ends stay visually consistent:
//   Property #4C8DFF · Tenant #27D199 · Lease #9B7CF6 · Clause #FB5A6A
export const NODE_COLORS = {
  Property: "#4C8DFF",
  Tenant: "#27D199",
  Lease: "#9B7CF6",
  Clause: "#FB5A6A",
};

const shared = {
  typography: {
    fontFamily: '"Roboto","Helvetica","Arial",sans-serif',
    h4: { fontWeight: 700, letterSpacing: "-0.5px" },
    h5: { fontWeight: 600 },
    h6: { fontWeight: 600 },
    button: { textTransform: "none", fontWeight: 600 },
  },
  shape: { borderRadius: 12 },
  components: {
    MuiCard: {
      defaultProps: { elevation: 0 },
      styleOverrides: {
        root: ({ theme }) => ({
          border: `1px solid ${theme.palette.divider}`,
          borderRadius: 16,
        }),
      },
    },
    MuiButton: { defaultProps: { disableElevation: true } },
    MuiAppBar: { defaultProps: { elevation: 0 } },
  },
};

export const makeTheme = (mode) =>
  createTheme({
    ...shared,
    palette: {
      mode,
      primary: { main: "#6200EE", light: "#9B7CF6", dark: "#4B00B5" },
      secondary: { main: "#03DAC6", dark: "#00A896" },
      success: { main: "#27D199" },
      error: { main: "#FB5A6A" },
      info: { main: "#4C8DFF" },
      ...(mode === "dark"
        ? {
            background: { default: "#0E1726", paper: "#152036" },
            divider: "rgba(255,255,255,0.10)",
          }
        : {
            background: { default: "#F5F6FA", paper: "#FFFFFF" },
            divider: "rgba(0,0,0,0.08)",
          }),
    },
  });
