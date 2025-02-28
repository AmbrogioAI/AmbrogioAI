import {
  Backdrop,
  CircularProgress,
  Stack,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";

interface LoadingScreenProps {
    loadingText: string;
    isLoading?: boolean;
    childrenAfterLoading?: React.ReactNode;
}

function LoadingScreen({ loadingText,isLoading }: LoadingScreenProps) {

  const [dots, setDots] = useState("");

  useEffect(() => {
    const interval = setInterval(() => {
      setDots((prev) => (prev.length < 3 ? prev + "." : ""));
    }, 500);

    return () => clearInterval(interval);
  }, []);

  return (
    <Backdrop
      sx={(theme) => ({ marginTop: "0px !important",color: "#fff", zIndex: theme.zIndex.drawer + 1 })}
      open={isLoading??true}
    >
      <Stack spacing={10} alignItems="center">
        <CircularProgress size="200px" color="inherit" />
        <Typography variant="h5">{loadingText + dots}</Typography>
      </Stack>
    </Backdrop>
  );
}

export default LoadingScreen;
