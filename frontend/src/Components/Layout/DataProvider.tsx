import React, { createContext, useContext, useEffect } from "react";
import { getModel } from "../../routes/getCurrentModel";
import { testLatency } from "../../routes/test";
import { Language, t } from "../../translations/t";
import LoadingScreen from "../LoadingScreen";

export function DataProvider({ children }: { children: React.ReactNode }) {
  return <DataGetter>{children}</DataGetter>;
}

// il tipo dei dati condivisi
interface DataContextType {
  setLanguage: React.Dispatch<React.SetStateAction<Language>>;
  language: Language;
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
  const [language, setLanguage] = React.useState<Language>(Language.IT);

  useEffect(() => {
    let isMounted = true;

    getModel().then((model) => {
      if (isMounted && model !== modelName) {
        setModelName(model);
      }
    });

    testLatency().then((latency) => {
      if (isMounted) setLatency(latency);
    });

    setTimeout(() => {
      if (isMounted) setLoading(false);
    }, 2100);

    const id = setInterval(() => {
      testLatency().then((latency) => {
        if (isMounted) setLatency(latency);
      });
    }, 10000);

    return () => {
      isMounted = false;
      clearInterval(id);
    };
  }, [modelName]);

  return (
    <DataContext.Provider
      value={{ modelName, latency, setModelName, language, setLanguage }}
    >
      {loading ? (
        <LoadingScreen loadingText={t("loadingServer", language)} />
      ) : (
        children
      )}
    </DataContext.Provider>
  );
};
