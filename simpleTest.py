from classes.resNet50FromScratch import ResNet50
import torch
from utilities.DataSetManager import DataSetManager as DSM
import numpy as np
from utilities.Logger import Logger
from sklearn.metrics import classification_report
from utilities import getClasses as gc
from utilities.plotConfusionMatrix import plotConfusionMatrix

def test_model(model):
    dataManager = DSM()
    _,_,test = dataManager.partitionDataSetEqualy()
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for img_path in test:
            probabilities = model.predict(img_path)  # restituisce lista di probabilità
            pred_class = np.argmax(probabilities)

            all_preds.append(pred_class)
            all_labels.append(np.argmax(dataManager.getCorrentPredictionOfImage(img_path)))
        
    # Confusion Matrix
    plotConfusionMatrix(all_preds, all_labels, title='Confusion Matrix - ResNet50', cmap='Blues')

    # Report con precision, recall, f1-score per classe
    report = classification_report(all_labels, all_preds, digits=4,target_names=gc.getClasses())
    Logger.logTagged("TESTING",f"Classification Report:\n {report}")

    # Errore medio di classificazione
    accuracy = np.mean(np.array(all_preds) == np.array(all_labels))
    classification_error = 1.0 - accuracy
    Logger.logTagged("TESTING",f"Errore medio di classificazione: {classification_error:.4f}")


if __name__ == '__main__':
    import os
    if os.name == 'nt':
        from multiprocessing import freeze_support
        freeze_support()
    # Test model
    model = ResNet50(num_classes=3)
    model.load_model()
    Logger.resetFile()
    test_model(model)