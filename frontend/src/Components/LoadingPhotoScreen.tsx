import { useState } from "react";
import LoadingScreen from "./LoadingScreen";
import { Backdrop, Button, Paper, Stack, Typography } from "@mui/material";
import React from "react";
import takePhoto from "../routes/takePhoto";
import { askToPredict } from "../routes/askToPredict";
import { t } from "../translations/t";
import { useDataContext } from "./Layout/DataProvider";

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
  const [isLoading, setIsLoading] = useState(false);
  const [close, setClose] = useState(false);
  const [image, setImage] = useState("");
  const [prediction, setPrediction] = useState([] as number[]);

  React.useEffect(() => {
    console.log("mode", mode);
    setIsLoading(true);
    switch (mode) {
      case Modes.singlePhoto:
        takePhoto()
          .then((res) => {
            setImage(res);
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
            setImage(res.image);
            setPrediction(res.prediction);
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
              style={{ width: "90%", objectFit: "contain",borderRadius:"10px" }}
              src={image}
            />
            {
              prediction.length > 0 && (
                <Stack
                  spacing={2}
                  direction={"column"}
                  justifyContent={"flex-start"}
                  alignItems={"center"}
                  overflow={"auto"}
                  width={"100%"}
                >
                  <Typography variant="h5">
                    {t("Prediction", language)}
                  </Typography>
                  <Typography variant="h6">
                    {prediction.map((item, index) => (
                      <div key={index}>
                        {t("Class"+index, language)}: {item}
                      </div>
                    ))}
                  </Typography>
                </Stack>
              )
            }
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
