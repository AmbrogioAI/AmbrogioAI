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
      var timer = new Date().getTime(); // 3 secondi di attesa
      // Ottieni la foto tramite capturePhoto
      const photo = await capturePhoto();

      // Crea un oggetto FormData per inviare i file
      const formData = new FormData();
      const blob = await fetch(photo!).then((res) => res.blob()); // Converti Base64 in Blob
      formData.append("image", blob, "photo.png");

      console.log("Processando l'immagine ho impiegato: " + (new Date().getTime() - timer) / 1000 + " secondi");

      timer = new Date().getTime(); // 3 secondi di attesa
      // Fai una richiesta POST per inviare l'immagine al server
      const response = await axios.post(routePrefix + "/predict", formData, {
        headers: {
          "Content-Type": "multipart/form-data", // Imposta correttamente il tipo di contenuto
        },
      });

      if (response.status === 200) {
        console.log("Ho impiegato: " + (new Date().getTime() - timer) / 1000 + " secondi per ricevere la risposta");
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
