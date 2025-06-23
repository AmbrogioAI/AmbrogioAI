from datetime import datetime
import sys
import os


# Ottieni il percorso assoluto della cartella principale (AmbrogioAI)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOAD_FOLDER = os.path.abspath(BASE_DIR+ "/backend/uploads")

# Aggiungi "AmbrogioAI" al percorso dei moduli importabili
sys.path.insert(0, BASE_DIR)


from flask import Flask, request, jsonify
from flask_cors import CORS
from classes.AmbrogioResNet50 import Optimazer
from classes import AmbrogioResNet50 as ar50
import serverState as ss
from PIL import Image
from classes.resNet50FromScratch import ResNet50
from PIL import Image
import rembg
import numpy as np


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Endpoint per scattare una foto e fare una predizione
@app.route('/test', methods=['GET'])
def testRoue():
    msg = "Hello World"
    return jsonify(msg)

@app.route('/removeModel', methods=['POST'])
def deleteChosenModel():
    ss.ServerState().set_model(None)
    return jsonify({}), 200

@app.route('/choseModel', methods=['POST'])
def choseAi():
    data = request.get_json()
    modelName = ""
    if data['model'] == 0:
        # Windows Support 
        if os.name == 'nt':
            from multiprocessing import freeze_support
            freeze_support()
        modelChosen = ar50.AmbrogioNet50(optimizer=Optimazer.Adam)
        modelName = "AmbrogioNet50"
    else:
        modelChosen = ResNet50(num_classes=3)
        modelName = "AmbrogioResNet50Simple"

    modelChosen.load_model()
    ss.ServerState().set_model(modelChosen)
    return jsonify({"modelChosen": modelName})
    

def saveImageToPath():
    # Controlla se la cartella esiste, altrimenti creala
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)

    image = request.files['image']
    if image is None:
        return jsonify({"error": "Nessuna immagine passata"}), 400
    
    # save the image to the upload folder
    path = os.path.join(UPLOAD_FOLDER, datetime.now().strftime("%Y%m%d%H%M%S") + ".png")
    image.save(path)
    # get the image path
    path = os.path.abspath(path)
    # remove the background from the image with rembg
    arr = Image.open(path)
    input_array = np.array(arr)
    output_array = rembg.remove(input_array)
    output_image = Image.fromarray(output_array)

    # Salva l'immagine senza sfondo
    no_bg_path = path.replace(".png", "_nobg.png")
    output_image.save(no_bg_path)

    return no_bg_path


@app.route('/predict', methods=['POST'])
def predict():
    
    model = ss.ServerState().get_model() 
    if model is None:
        return jsonify({"error": "Nessun modello selezionato"}), 400

    # get the passed image from the request
    prediction = model.predict(saveImageToPath())

    return jsonify({"prediction": prediction})

@app.route('/currentModel', methods=['GET'])
def currentModel():
    if ss.ServerState().get_model() is None:
        return jsonify({}), 403
    return jsonify({"model": ss.ServerState().get_model().name})


if __name__ == "__main__":
    # start the server in debug
    app.run()