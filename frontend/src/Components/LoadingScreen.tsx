import {
  Backdrop,
  CircularProgress,
  Stack,
  Typography,
} from "@mui/material";

interface LoadingScreenProps {
    loadingText: string;
    isLoading?: boolean;
}

function LoadingScreen({ loadingText,isLoading }: LoadingScreenProps) {
  return (
    <Backdrop
      sx={(theme) => ({ color: "#fff", zIndex: theme.zIndex.drawer + 1 })}
      open={isLoading??true}
    >
      <Stack spacing={10} alignItems="center">
        <CircularProgress size="200px" color="inherit" />
        <Typography variant="h5">{loadingText}</Typography>
      </Stack>
    </Backdrop>
  );
}

export default LoadingScreen;
