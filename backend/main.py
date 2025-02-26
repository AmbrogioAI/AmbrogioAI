import sys
import os
import io
from PIL import Image

# Ottieni il percorso assoluto della cartella principale (AmbrogioAI)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
UPLOAD_FOLDER = os.path.abspath(BASE_DIR+ "/backend/uploads")

# Aggiungi "AmbrogioAI" al percorso dei moduli importabili
sys.path.insert(0, BASE_DIR)


from flask import Flask, request, jsonify
from flask_cors import CORS
import time
from classes.AmbrogioResNet50 import Optimazer
from classes import AmbrogioResNet50 as ar50
from classes import AmbrogioSimple as simple
import serverState as ss

app = Flask(__name__)
CORS(app)

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
        
    if data['model'] == 0:
        # Windows Support 
        if os.name == 'nt':
            from multiprocessing import freeze_support
            freeze_support()
        modelChosen = ar50.AmbrogioNet50(optimizer=Optimazer.Adam)
        modelChosen.load_model()
        ss.ServerState().set_model(modelChosen)
        return jsonify({"modelChosen": "AmbrogioNet50"})
    else:
        modelChosen = simple.AmbrogioSimple()
        modelChosen.loadState()
        ss.ServerState().set_model(modelChosen)
        return jsonify({"modelChosen": "AmbrogioSimple"})

@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "Nessun file inviato"}), 400
    
    if ss.ServerState().get_model() is None:
        return jsonify({"error": "Nessun modello selezionato"}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({"error": "File non valido"}), 400

    file_path = os.path.join(UPLOAD_FOLDER, image_file.filename)
    image_file.save(file_path)  # Salva il file

    # Verifica che il file esista
    if not os.path.exists(file_path):
        return jsonify({"error": "Errore nel salvataggio dell'immagine"}), 500

    try:
        image = Image.open(file_path)
        image.verify()  # Controlla se è corrotto
        image = Image.open(file_path).convert('RGB')  # Riapri e converti in RGB
    except Exception as e:
        return jsonify({"error": f"Errore nell'apertura dell'immagine: {str(e)}"}), 400

    prediction = ss.ServerState().get_model().predict(file_path)
    return jsonify({"prediction": prediction})

@app.route('/currentModel', methods=['GET'])
def currentModel():
    if ss.ServerState().get_model() is None:
        return jsonify({}), 200
    return jsonify({"model": ss.ServerState().get_model().name}), 200

if __name__ == "__main__":
    app.run()