from classes.AmbrogioResNet50 import AmbrogioNet50
from classes.resNet50FromScratch import ResNet50 as ResNet50FromScratch
import os
import rembg
from PIL import Image
import numpy as np

def testImageGivenNameInTestFolder(name):
    """
    Given the name of an image, return the path to the image in the test folder.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    image_path = os.path.join(project_root, "neverSeenImages", name)
    no_bg_image_path = os.path.join(project_root, "images", f"{name}_no_bg.jpg")

    # Stampa utile per debugging
    print(f"Original image path: {image_path}")

    if not os.path.exists(image_path):
        raise FileNotFoundError(f"L'immagine non esiste: {image_path}")

    if not os.path.exists(no_bg_image_path):
        # Rimuove lo sfondo
        print(f"Rimuovo lo sfondo dell'immagine: {image_path}")
        arr = Image.open(image_path)
        input_array = np.array(arr)
        output_array = rembg.remove(input_array)
        output_image = Image.fromarray(output_array)

        # Salva l'immagine senza sfondo
        no_bg_image_path = image_path.replace(".png", "_nobg.png")
        output_image.save(no_bg_image_path)

    model.predict(no_bg_image_path)


if __name__ == '__main__':
    import os
    if os.name == 'nt':
        from multiprocessing import freeze_support
        freeze_support()
    print("Inizio il test con immagini mai viste prima per il modello AmbrogioNet50...")
    model = AmbrogioNet50()
    model.load_model()
    testImageGivenNameInTestFolder("casual.png")
    testImageGivenNameInTestFolder("sportyTest.png")
    testImageGivenNameInTestFolder("elegantTest.png")
    print("------------------------------------------------------------------------")
    print("Inizio il test con immagini mai viste prima per il modello SimpleAmbrogio...")
    model = ResNet50FromScratch(num_classes=3)
    model.load_model()
    testImageGivenNameInTestFolder("casual.png")
    testImageGivenNameInTestFolder("sportyTest.png")
    testImageGivenNameInTestFolder("elegantTest.png")