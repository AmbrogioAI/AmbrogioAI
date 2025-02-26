def takePhoto():
    '''
    Takes a photo using the Raspberry Pi camera module if available, or a USB camera (OpenCV) otherwise.
    The photo is saved in a folder named "photo" on the Desktop.
    
    :return: The path of the saved photo.
    '''
    import os
    import platform
    from datetime import datetime

    # Prova a importare picamera se è un Raspberry Pi
    try:
        if 'raspberrypi' in platform.uname().node.lower():
            from picamera import PiCamera
            is_raspberry = True
        else:
            is_raspberry = False
    except ImportError:
        is_raspberry = False

    # Ottieni la directory root del progetto (cartella in cui si trova lo script)
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    photo_folder = os.path.join(ROOT_DIR, "photo")
    

    if not os.path.exists(photo_folder):
        os.makedirs(photo_folder)

    # Genera il nome del file in base alla data e ora attuali
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = os.path.join(photo_folder, f"photo_{timestamp}.jpg")

    if is_raspberry:
        # Utilizza la fotocamera del Raspberry Pi
        camera = PiCamera()

        try:
            camera.start_preview()
            # Attendi 2 secondi per permettere alla fotocamera di regolare l'illuminazione
            camera.sleep(2)
            # Scatta la foto
            camera.capture(file_path)
            print(f"Foto salvata in {file_path}")
        finally:
            camera.stop_preview()
            camera.close()

    else:
        # Utilizza una telecamera USB (OpenCV)
        import cv2

        # Accedi alla telecamera (di solito l'indice 0 è la telecamera principale)
        cap = cv2.VideoCapture(0)

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


        if not cap.isOpened():
            print("Errore: impossibile accedere alla telecamera.")
        else:
            # Scatta la foto
            ret, frame = cap.read()

            if ret:

                # ***Mantieni l'immagine a colori***
        
                # Converti dallo spazio colore BGR (usato da OpenCV) a YCrCb
                ycrcb = cv2.cvtColor(frame, cv2.COLOR_BGR2YCrCb)

                # Equalizza solo il canale della luminosità (Y)
                ycrcb[:, :, 0] = cv2.equalizeHist(ycrcb[:, :, 0])

                # Converti di nuovo a BGR
                enhanced_image = cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2BGR)

                # Salva l'immagine migliorata
                file_path = "foto_enhanced.jpg"
                cv2.imwrite(file_path, enhanced_image)
                print(f"Foto salvata in {file_path}")
            else:
                print("Errore: impossibile catturare l'immagine.")

            # Rilascia la telecamera
            cap.release()
    
    return file_path

