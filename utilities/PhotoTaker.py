def takePhoto():
    '''
    Takes a photo using the Raspberry Pi camera module if available, or a USB camera (OpenCV) otherwise.
    The photo is saved in a folder named "photo" in the utilities/photo folder.
    
    :return: The path of the saved photo.
    '''
    import os
    import platform
    from datetime import datetime

    # Prova a importare picamera se è un Raspberry Pi
    try:
        from picamera2 import Picamera2
        is_raspberry = True
    except ImportError as e:
        print(f"Errore nell'importazione di picamera2: {e}")
        is_raspberry = False

    # Ottieni la directory root del progetto (cartella in cui si trova lo script)
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    photo_folder = os.path.join(ROOT_DIR, "photo")
    

    if not os.path.exists(photo_folder):
        os.makedirs(photo_folder)

    # Genera il nome del file in base alla data e ora attuali
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(photo_folder, f"photo_{timestamp}.jpg")
    print("modalità raspberry:", is_raspberry)
    if is_raspberry:
        # Utilizza la fotocamera del Raspberry Pi
        picam2 = Picamera2()
        picam2.start()

        import time

        # Attendi 2 secondi per permettere alla fotocamera di regolare l'illuminazione
        time.sleep(2)
        # Scatta la foto
        picam2.capture_file(file_path)
        print(f"Foto salvata in {file_path}")
        

    else:
        # Utilizza una telecamera USB (OpenCV)
        import cv2

        # Accedi alla telecamera (di solito l'indice 0 è la telecamera principale)
        cap = cv2.VideoCapture(0)
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        if not cap.isOpened():
            print("Errore: impossibile accedere alla telecamera.")
            return False

        # Scatta la foto
        ret, frame = cap.read()

        try:
            if ret:
                cv2.imwrite(file_path, frame) 
                print(f"Foto salvata in {file_path}")
            else:
                print("Errore: impossibile catturare l'immagine.")
            pass
        except Exception as e:
            print("Errore:", e)
        finally:
            cap.release()
    
    return file_path

