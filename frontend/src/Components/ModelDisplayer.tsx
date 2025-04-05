import { Button, Grid2, Stack, Typography } from "@mui/material";
import { useDataContext } from "./Layout/DataProvider";
import ModelImage from "./ModelImage";
import { PossibleModels } from "../routes/chooseModel";
import { t } from "../translations/t";
import CameraIcon from "@mui/icons-material/Camera";
import ImageSearchIcon from "@mui/icons-material/ImageSearch";
import { Modes, LoadingPhotoScreen } from "./LoadingPhotoScreen";
import { useState } from "react";

function ModelDisplayer() {
  const { modelName, language } = useDataContext();
  const [startLoading, setStartLoading] = useState(false);
  const [selectedMode, setSelectedMode] = useState(Modes.singlePhoto);
  const translateStr =
    modelName + (new Date().getHours() > 18 ? ".HelloNight" : ".HelloDay");

  const handleShowPhoto = () => {
    setSelectedMode(Modes.singlePhoto);
    setStartLoading(true);
  };

  const handleTakePhotoAndPredict = () => {
    setSelectedMode(Modes.prediction);
    setStartLoading(true);
  };

  return (
    <>
      <Stack spacing={30} direction={"column"}>
        <Stack spacing={20} direction={"row"} justifyContent={"center"}>
          <Stack
            spacing={2}
            direction={"column"}
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
            }}
          >
            <Typography variant="h4">{modelName}</Typography>
            <Typography variant="h6">{t(translateStr, language)}</Typography>
          </Stack>
          <ModelImage
            model={
              modelName == "AmbrogioNet50"
                ? PossibleModels.resNet50
                : PossibleModels.simple
            }
            size={300}
            showShadow
          />
        </Stack>
        <Grid2
          container
          spacing={8}
          direction={"row"}
          justifyContent={"center"}
        >
          <Grid2 size={{ sm: 12, md: 6 }}>
            <BtnAction
              text={t("takePhotoAndShow", language)}
              icon={<ImageSearchIcon style={{ fontSize: "50px" }} />}
              onClick={()=>handleShowPhoto()}
            />
          </Grid2>
          <Grid2 size={{ sm: 12, md: 6 }}>
            <BtnAction
              text={t("takePhoto", language)}
              icon={<CameraIcon style={{ fontSize: "50px" }} />}
              onClick={()=>handleTakePhotoAndPredict()}
            />
          </Grid2>
        </Grid2>
      </Stack>
      {
        startLoading && (
          <LoadingPhotoScreen mode={selectedMode} handleClose={() => setStartLoading(false)} />
        )
      }
    </>
  );
}

interface BtnActionProps {
  text: string;
  icon: React.ReactNode;
  onClick: () => void;
}

function BtnAction({ text, icon, onClick }: BtnActionProps) {
  return (
    <Button
      fullWidth
      component="label"
      role={undefined}
      variant="contained"
      tabIndex={-1}
      startIcon={icon}
      style={{
        height: "100%",
        fontSize: "20px",
        padding: "20px",
        borderRadius: "20px",
      }}
      onClick={()=>onClick()}
    >
      {text}
    </Button>
  );
}

export default ModelDisplayer;
