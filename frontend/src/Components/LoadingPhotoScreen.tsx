import { useState, useEffect,useRef } from "react";
import LoadingScreen from "./LoadingScreen";
import { Backdrop, Button, Paper, Typography } from "@mui/material";
import { askToPredict } from "../routes/askToPredict";
import { t } from "../translations/t";
import { useDataContext } from "./Layout/DataProvider";
import capturePhoto from "../Utils/takeAPhoto";
import { useThemeContext } from "./Layout/ThemeProvider";

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
  const { isDarkMode } = useThemeContext();
  const executedRef = useRef(false);
  // Stato per il conto alla rovescia
  const maxCountdown = 3; // Imposta il tempo del countdown in secondi
  const [countdown, setCountdown] = useState(maxCountdown);

  useEffect(() => {
    const interval = setInterval(() => {
      setCountdown((prev) => prev - 1);
    }, 1000);
    if (executedRef.current) return;
    executedRef.current = true;
    
    if (Modes.prediction === mode) {
      setTimeout(() => {
        clearInterval(interval); // Ferma il countdown
        askToPredict()
          .then((res) => {
            setPrediction(res.prediction);
            setImage(res.image);
            setIsLoading(false);
          })
          .catch((err) => {
            console.error(err);
            setIsLoading(false);
          });
      }, maxCountdown * 1000 + 1000);
      return () => clearInterval(interval);
    } else {
      // Dopo 3 secondi, scatta la foto
      setTimeout(() => {
        clearInterval(interval); // Ferma il countdown
        capturePhoto().then((res) => {
          setImage(res!);
          setIsLoading(false);
        });
      }, maxCountdown * 1000);

      return () => clearInterval(interval);
    }
  }, []);

  return (
    <div style={{ marginTop: "0px !important" }}>
      {countdown > 0 ? (
        <Backdrop
          sx={(theme) => ({ color: "#fff", zIndex: theme.zIndex.drawer + 1 })}
          open
        >
          <Typography variant="h2">{countdown}</Typography>
        </Backdrop>
      ) : (
        <LoadingScreen
          isLoading={isLoading}
          loadingText={t("LoadingPhoto", language)}
        />
      )}

      <Backdrop
        sx={(theme) => ({ color: "#fff", zIndex: theme.zIndex.drawer + 1 })}
        open={!isLoading && !close}
      >
        <Paper
          style={{
            width: "80%",
            height: "90%",
            padding: "20px",
            overflowY: "auto",
          }}
          elevation={3}
        >
          <Typography variant="h5">{t("ThisIsWhatISee", language)}</Typography>
          <img
            style={{
              width: "80%",
              height: "80%",
              objectFit: "contain",
              borderRadius: "10px",
            }}
            src={image}
          />
          {prediction.length > 0 && (
            <div
              style={{
                position: "absolute",
                top: "100px",
                backgroundColor: isDarkMode ? "black" : "white",
                color: isDarkMode ? "white" : "black",
                padding: "20px",
                textAlign: "left",
                borderRadius: "16px",
              }}
            >
              <Typography variant="h5">{t("Prediction", language)}</Typography>
              {prediction.map((item, index) => (
                <Typography variant="h6" key={index}>
                  {t("Class" + index, language)}: {(item * 100).toFixed(2)}%
                </Typography>
              ))}
            </div>
          )}
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
