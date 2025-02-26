import axios from "axios";
import { routePrefix } from "../config/systemVariables";

export enum PossibleModels {
  "resNet50" = 0,
  "simple" = 1,
}

export async function chooseModel(chooseModel: PossibleModels) : Promise<string> {
  return axios.post(routePrefix + "/choseModel", { model:chooseModel }).then((res) => {
    return res.data.modelChosen;
  });
}
