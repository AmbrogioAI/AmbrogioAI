import axios from "axios";
import { routePrefix } from "../config/systemVariables";

export interface PredictionResult {
  prediction: string;
  image: File;
}

export function askToPredict(): Promise<PredictionResult> {
  return new Promise((resolve, reject) => {
    axios
      .post(routePrefix + "/predict", {
        headers: {
          "Content-Type": "application/json",
        },
      })
      .then((res) => {
        if (res.status == 200) {
          resolve(res.data);
        } else {
          reject("Error while predicting");
        }
      })
      .catch((err) => {
        reject(err);
      });
  });
}
