import { Card, Stack, Typography } from "@mui/material";
import { Grid2 as Grid } from "@mui/material";
import React from "react";
import { chooseModel, PossibleModels } from "../routes/chooseModel";
import { useDataContext } from "./Layout/DataProvider";
import { t } from "../translations/t";
import LoadingScreen from "./LoadingScreen";
import ModelImage from "./ModelImage";

function ModelPicker() {
  const { setModelName, language } = useDataContext();
  const [isLoading, setIsLoading] = React.useState(false);

  const handleClick = (model: PossibleModels) => {
    setIsLoading(true);
    chooseModel(model)
      .then((res) => {
        setIsLoading(false);
        setModelName(res);
      })
      .catch((err) => {
        console.error(err);
        setIsLoading(false);
      });
  };

  return (
    <>
      <Card sx={{ p: 3, width: "90%", mt:"150px !important" }} elevation={5}>
        <Stack spacing={2}>
          <Typography variant="h4">{t("ChooseModel", language)}</Typography>
          <Grid container spacing={2}>
            <Grid size={{ xs: 12, sm: 6 }}>
              <SingleModelButton
                model="AmbrogioNet50"
                onClick={() => handleClick(PossibleModels.resNet50)}
                description={t("ResNet50Description", language)}
              />
            </Grid>
            <Grid size={{ xs: 12, sm: 6 }}>
              <SingleModelButton
                model="AmbrogioSimple"
                onClick={() => handleClick(PossibleModels.simple)}
                description={t("SimpleDescription", language)}
              />
            </Grid>
          </Grid>
        </Stack>
      </Card>
      <LoadingScreen isLoading={isLoading} loadingText={t("loadingModel",language)} />
    </>
  );
}

interface SingleModelButtonProps {
  model: string;
  onClick: () => void;
  description: string;
}

const SingleModelButton: React.FC<SingleModelButtonProps> = ({
  model,
  onClick,
  description,
}) => {
  return (
    <Card onClick={onClick} sx={{ p: 2, cursor: "pointer" }} elevation={3}>
      <Typography variant="h5">{model}</Typography>
      <ModelImage model={model=="AmbrogioNet50"?PossibleModels.resNet50:PossibleModels.simple} size={200} />
      <Typography>{description}</Typography>
    </Card>
  );
};

export default ModelPicker;
