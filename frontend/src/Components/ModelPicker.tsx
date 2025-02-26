import { Card, Stack, Typography } from "@mui/material";
import { Grid2 as Grid } from "@mui/material";
import React from "react";
import { chooseModel, PossibleModels } from "../routes/chooseModel";
import { useDataContext } from "./Layout/DataProvider";

function ModelPicker() {
  const {setModelName} = useDataContext();


  return (
    <Card sx={{ p: 3, width: "90%" }} elevation={5}>
      <Stack spacing={2}>
        <Typography variant="h4">
          Seleziona un modello tra quelli disponibili:
        </Typography>
        <Grid container spacing={2}>
          <Grid size={{ xs: 12, sm: 6 }}>
            <SingleModelButton
              model="AmbrogioNet50"
              onClick={() => chooseModel(PossibleModels.resNet50).then((res) => setModelName(res))}
              description="Maggiordomo molto intelligente, fa errori raramente,e se li commette impara da essi personalizzandosi in base all'utilizzatore."
            />
          </Grid>
          <Grid size={{ xs: 12, sm: 6 }}>
            <SingleModelButton
              model="AmbrogioSimple"
              onClick={() => chooseModel(PossibleModels.simple)}
              description="Maggiordomo molto semplice, ogni tanto potrebbe fare qualche errore, gli manca un po' di esperienza."
            />
          </Grid>
        </Grid>
      </Stack>
    </Card>
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
      <Typography>{description}</Typography>
    </Card>
  );
};

export default ModelPicker;
