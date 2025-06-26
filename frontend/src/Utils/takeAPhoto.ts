export default async function capturePhoto({
  width = 1036,
  height = 1088,
  mimeType = "image/jpeg",
  quality = 0.8,
}: {
  width?: number;
  height?: number;
  mimeType?: "image/jpeg" | "image/png";
  quality?: number;
} = {}): Promise<string | null> {
  const video = document.createElement("video");
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");

  try {
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: width },
        height: { ideal: height },
        frameRate: { ideal: 60 },
      },
    });

    video.srcObject = stream;
    video.muted = true;
    video.playsInline = true;
    video.autoplay = true;

    await new Promise((resolve) => {
      video.onloadedmetadata = () => {
        video.play();
        resolve(true);
      };
    });

    canvas.width = width;
    canvas.height = height;

    if (!context) {
      throw new Error("Impossibile ottenere il contesto del canvas");
    }

    // Aspetta il prossimo frame per assicurarti che la fotocamera abbia "un'immagine"
    await new Promise(requestAnimationFrame);

    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL(mimeType, quality);

    // Stop della fotocamera
    stream.getTracks().forEach((track) => track.stop());

    return imageData;
  } catch (error) {
    console.error("Errore nell'acquisizione della foto:", error);
    return null;
  }
}
