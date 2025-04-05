export default async function capturePhoto() {
  const video = document.createElement("video");
  const canvas = document.createElement("canvas");
  const context = canvas.getContext("2d");

  try {
    // Accendi la fotocamera
    const stream = await navigator.mediaDevices.getUserMedia({
      video: {
        width: { ideal: 1920 },
        height: { ideal: 1080 },
        frameRate: { ideal: 60 },
      },
    });
    video.srcObject = stream;
    await new Promise((resolve) => (video.onloadedmetadata = resolve));
    video.play();

    // Imposta le dimensioni della canvas
    canvas.width = 448;
    canvas.height = 448;

    // Verifica che il context sia stato creato correttamente
    if (!context) {
      throw new Error("Impossibile ottenere il contesto del canvas");
    }

    // Disegna l'immagine sul canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Converti l'immagine in base64
    const imageData = canvas.toDataURL("image/png");

    // Interrompi il flusso della fotocamera
    stream.getTracks().forEach((track) => track.stop());

    return imageData; // Restituisce l'immagine in base64
  } catch (error) {
    console.error("Errore nell'acquisizione della foto:", error);
    return null; // Ritorna null in caso di errore
  }
}
