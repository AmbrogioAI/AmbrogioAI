import axios from "axios";
import { routePrefix } from "../config/systemVariables";
import capturePhoto from "../Utils/takeAPhoto";

export interface PredictionResult {
  prediction: number[];
  image: string;
}

export function askToPredict(): Promise<PredictionResult> {
  return new Promise(async (resolve, reject) => {
    try {
      // Ottieni la foto tramite capturePhoto
      const photo = await capturePhoto();

      // Crea un oggetto FormData per inviare i file
      const formData = new FormData();
      const blob = await fetch(photo!).then((res) => res.blob()); // Converti Base64 in Blob
      formData.append("image", blob, "photo.png");

      // Fai una richiesta POST per inviare l'immagine al server
      const response = await axios.post(routePrefix + "/predict", formData, {
        headers: {
          "Content-Type": "multipart/form-data", // Imposta correttamente il tipo di contenuto
        },
      });

      if (response.status === 200) {
        resolve({
          prediction: response.data.prediction,
          image: photo!,
        } as PredictionResult); // Risolvi con la risposta (contenente la previsione)
      } else {
        reject("Error while predicting");
      }
    } catch (err) {
      reject(err);
    }
  });
}
