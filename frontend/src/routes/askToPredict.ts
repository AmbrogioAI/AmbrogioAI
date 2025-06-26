import axios from "axios";
import { routePrefix } from "../config/systemVariables";
import capturePhoto from "../Utils/takeAPhoto";

export interface PredictionResult {
  prediction: number[];
  image: string;
}

async function resizeAndCompress(base64: string, quality: number, maxWidth: number): Promise<Blob> {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => {
      const ratio = img.width > maxWidth ? maxWidth / img.width : 1;
      const width = img.width * ratio;
      const height = img.height * ratio;

      const canvas = document.createElement("canvas");
      canvas.width = width;
      canvas.height = height;
      const ctx = canvas.getContext("2d")!;
      ctx.drawImage(img, 0, 0, width, height);

      canvas.toBlob(
        (blob) => {
          if (blob) resolve(blob);
          else reject(new Error("Impossibile creare Blob"));
        },
        "image/jpeg",
        quality
      );
    };
    img.onerror = reject;
    img.src = base64;
  });
}


export async function askToPredict(): Promise<PredictionResult> {
  try {
    const totalStart = performance.now();

    // 1. Cattura foto
    const photoStart = performance.now();
    const photoBase64 = await capturePhoto();
    const photoCaptureTime = performance.now() - photoStart;

    // 2. Ridimensiona e comprime l'immagine usando canvas
    const resizeStart = performance.now();
    const blob = await resizeAndCompress(photoBase64!, 0.7, 512); // qualità 70%, max larghezza 512px
    const resizeTime = performance.now() - resizeStart;

    // 3. Prepara il FormData
    const formData = new FormData();
    formData.append("image", blob, "photo.jpg");
    
    // 4. Invia al server
    const requestStart = performance.now();
    const response = await axios.post(routePrefix + "/predict", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    const requestTime = performance.now() - requestStart;

    const totalTime = performance.now() - totalStart;

    // Logging dettagliato
    console.log(`📸 Foto catturata in ${photoCaptureTime.toFixed(2)} ms`);
    console.log(`🖼️ Immagine ridimensionata/compressa in ${resizeTime.toFixed(2)} ms`);
    console.log(`📡 Richiesta inviata e risposta ricevuta in ${requestTime.toFixed(2)} ms`);
    console.log(`✅ Tempo totale: ${totalTime.toFixed(2)} ms`);

    if (response.status === 200) {
      return {
        prediction: response.data.prediction,
        image: photoBase64!,
      };
    } else {
      throw new Error("Errore nella risposta del server");
    }
  } catch (err) {
    throw err;
  }
}

