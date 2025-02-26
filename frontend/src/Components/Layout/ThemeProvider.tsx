import { createContext, useContext, useState, ReactNode } from "react";
import {
  createTheme,
  ThemeProvider as MUIThemeProvider,
  CssBaseline,
} from "@mui/material";

interface ThemeContextType {
  isDarkMode: boolean;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// eslint-disable-next-line react-refresh/only-export-components
export const useThemeContext = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error("useThemeContext must be used within a ThemeProvider");
  }
  return context;
};

const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const [isDarkMode, setIsDarkMode] = useState(localStorage.getItem("darkMode") === "true" || false);

  const toggleTheme = () => setIsDarkMode((prev) => !prev);

  const theme = createTheme({
    palette: {
      mode: isDarkMode ? "dark" : "light",
      primary: {
        main: "#3d3c3c",
      },
      secondary: {
        main: "#9c27b0",
      },
    },
    components: {
        MuiButtonBase: {
          styleOverrides: {
              root: {
              "&:focus": {
                outline: "none !important", // Rimuove il bordo focus
              },
              "&:focus-visible": {
                  outline: "none !important",
              },
              },
          },
      },
      MuiButton:{
        styleOverrides:{
          outlined:{
            color: "inherit !important",
            "&:focus": {
                outline: "none !important", // Rimuove il bordo focus
              },
              "&:hover": {
                outline: "none !important", // Rimuove il bordo focus
                border: "1px solid white !important",
              },
              "&:focus-visible": {
                  outline: "none !important",
              },
          }
        }
      },
      MuiDialog:{
        styleOverrides:{
          paper:{
            backgroundColor: isDarkMode ? '#121212 !important' : '#fff',
            margin: '0px',
          }
        }
      }, 
    },
});

  return (
    <ThemeContext.Provider value={{ isDarkMode, toggleTheme }}>
      <MUIThemeProvider theme={theme}>
        <CssBaseline />
        {children}
      </MUIThemeProvider>
    </ThemeContext.Provider>
  );
};

export default ThemeProvider;