import { useState } from "react";
import LoadingScreen from "./LoadingScreen";
import { Backdrop, Button, Paper, Typography } from "@mui/material";
import React from "react";
import takePhoto from "../routes/takePhoto";
import { askToPredict } from "../routes/askToPredict";

enum Modes {
  singlePhoto = 0,
  prediction = 1,
}

interface LoadingPhotoScreenProps {
  mode: Modes;
  handleClose: () => void;
}

function LoadingPhotoScreen({ mode, handleClose }: LoadingPhotoScreenProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [close, setClose] = useState(false);

  React.useEffect(() => {
    console.log("mode", mode);
    setIsLoading(true);
    switch (mode) {
      case Modes.singlePhoto:
        takePhoto()
          .then((res) => {
            console.log("Photo taken", res);
            setIsLoading(false);
          })
          .catch((err) => {
            console.error(err);
            setIsLoading(false);
          });
        break;
      case Modes.prediction:
        askToPredict()
          .then((res) => {
            console.log("Prediction done", res);
            setIsLoading(false);
          })
          .catch((err) => {
            console.error(err);
            setIsLoading(false);
          });
        break;
      default:
        setIsLoading(false);
        break;
    }
  }, [mode]);

  return (
    <div style={{ marginTop: "0px !important" }}>
      <LoadingScreen isLoading={isLoading} loadingText={"Loading Photo"} />
      <Backdrop
        sx={(theme) => ({ color: "#fff", zIndex: theme.zIndex.drawer + 1 })}
        open={!isLoading && !close}
      >
        <Paper>
          <Typography variant="h5">Loading Photo finished</Typography>
          <Typography variant="h5">with mode = {mode}</Typography>
          <Button
            onClick={() => {
              setClose(true);
              handleClose();
            }}
          >
            Close
          </Button>
        </Paper>
      </Backdrop>
    </div>
  );
}

export { LoadingPhotoScreen, Modes };
