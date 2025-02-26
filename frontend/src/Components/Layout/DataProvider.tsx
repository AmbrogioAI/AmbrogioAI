import React, { createContext, useContext, useEffect } from "react";
import { getModel } from "../../routes/getCurrentModel";
import { testLatency } from "../../routes/test";
import { CircularProgress } from "@mui/material";

export function DataProvider({ children }: { children: React.ReactNode }) {
  return <DataGetter>{children}</DataGetter>;
}

// il tipo dei dati condivisi
interface DataContextType {
  modelName: string | null;
  setModelName: React.Dispatch<React.SetStateAction<string | null>>;
  latency: number | null;
}

// Creiamo il contesto
const DataContext = createContext<DataContextType | undefined>(undefined);

// Hook personalizzato per usare il contesto più facilmente
export const useDataContext = () => {
  const context = useContext(DataContext);
  if (!context) {
    throw new Error("useDataContext must be used within a DataProvider");
  }
  return context;
};

export const DataGetter = ({ children }: { children: React.ReactNode }) => {
  const [modelName, setModelName] = React.useState<string | null>(null);
  const [latency, setLatency] = React.useState<number | null>(null);
  const [loading, setLoading] = React.useState<boolean>(true);


  useEffect(() => {
    getModel().then((model) => {
      setModelName(model);
    });
    setTimeout(() => {
      setLoading(false);
    }, 2100);
    const id = setInterval(() => {
      testLatency().then((latency) => {
        setLatency(latency);
      });
    }, 10000);

    return () => {
      console.log(modelName)
      clearInterval(id);
    };
  },[modelName]);

  return (
    <DataContext.Provider value={{ modelName, latency, setModelName }}>
      {loading ? <CircularProgress size="5rem" color="secondary" /> : children}
    </DataContext.Provider>
  );
};
