import { useState } from "react";
import LoadingScreen from "./LoadingScreen";
import { Backdrop, Button, Paper, Stack, Typography } from "@mui/material";
import React from "react";
import { askToPredict } from "../routes/askToPredict";
import { t } from "../translations/t";
import { useDataContext } from "./Layout/DataProvider";
import capturePhoto from "../Utils/takeAPhoto";

enum Modes {
  singlePhoto = 0,
  prediction = 1,
}

interface LoadingPhotoScreenProps {
  mode: Modes;
  handleClose: () => void;
}

function LoadingPhotoScreen({ mode, handleClose }: LoadingPhotoScreenProps) {
  const { language } = useDataContext();
  const [isLoading, setIsLoading] = useState(true);
  const [close, setClose] = useState(false);
  const [image, setImage] = useState("");
  const [prediction, setPrediction] = useState([] as number[]);

  React.useEffect(() => {
    if (Modes.prediction === mode) {
      askToPredict()
        .then((res) => {
          console.log(res.prediction);
          setPrediction(res.prediction);
          setImage(res.image);
          setIsLoading(false);
        })
        .catch((err) => {
          console.error(err);
          setIsLoading(false);
        });
    } else {
      capturePhoto().then((res) => {
        setImage(res!);
        setIsLoading(false);
      });
    }
  }, []);

  return (
    <div style={{ marginTop: "0px !important" }}>
      <LoadingScreen
        isLoading={isLoading}
        loadingText={t("LoadingPhoto", language)}
      />
      <Backdrop
        sx={(theme) => ({ color: "#fff", zIndex: theme.zIndex.drawer + 1 })}
        open={!isLoading && !close}
      >
        <Paper
          style={{
            width: "80%",
            height: "80%",
            padding: "20px",
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            flexDirection: "column",
          }}
          elevation={3}
        >
          <Stack
            spacing={2}
            direction={"column"}
            justifyContent={"flex-start"}
            alignItems={"center"}
            overflow={"auto"}
            width={"100%"}
          >
            <Typography variant="h5">
              {t("ThisIsWhatISee", language)}
            </Typography>
            <img
              style={{
                width: "90%",
                height: "90%",
                objectFit: "contain",
                borderRadius: "10px",
              }}
              src={image}
            />
          </Stack>
          <Stack
            spacing={2}
            direction={"column"}
            justifyContent={"flex-start"}
            alignItems={"center"}
            overflow={"auto"}
            width={"100%"}
          >
            <Typography variant="h5">{t("Prediction", language)}</Typography>
            {prediction.map((item, index) => (
              <Typography variant="h6" key={index}>
                {t("Class" + index, language)}: {(item * 100).toFixed(2)} %
              </Typography>
            ))}
          </Stack>
          <Button
            variant="contained"
            color="primary"
            style={{ width: "80%", marginTop: "20px" }}
            onClick={() => {
              setClose(true);
              handleClose();
            }}
          >
            {t("Close", language)}
          </Button>
        </Paper>
      </Backdrop>
    </div>
  );
}

export { LoadingPhotoScreen, Modes };
