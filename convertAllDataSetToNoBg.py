import os
import numpy as np
from PIL import Image
import rembg
from utilities.DataSetManager import DataSetManager as dsm

def remove_background(input_path):
    """
    Rimuove lo sfondo da un'immagine e la sovrascrive con una versione PNG trasparente.
    """
    # Carica l'immagine
    diocane = os.path.abspath(input_path)
    input_image = Image.open(diocane)
    input_array = np.array(input_image)

    # Rimuove lo sfondo
    output_array = rembg.remove(input_array)

    # Crea l'immagine output con trasparenza
    output_image = Image.fromarray(output_array)

    # Costruisci nuovo percorso con estensione .png
    new_path = os.path.splitext(input_path)[0] + ".png"

    # Salva l'immagine senza sfondo
    output_image.save(new_path)

    # (Facoltativo) Elimina il file originale se era jpg
    if input_path.lower().endswith(('.jpg', '.jpeg')):
        os.remove(input_path)


if __name__ == "__main__":
    # Example usage
    photos = dsm().getAllImages()
    for i,path in enumerate(photos):
        # Remove the background from the image
        remove_background(path)
        # Print the progress
        print(f"{i}/{len(photos)})")
