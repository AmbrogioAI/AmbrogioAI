from classes.AmbrogioResNet50 import Optimazer
from utilities import DataSetManager as dsm
from classes import AmbrogioResNet50 as ar50
from classes.TestingMode import TestingMode
from classes.resNet50FromScratch import ResNet50 as ResNet50FromScratch
import os
from matplotlib import pyplot as plt
from utilities.Logger import Logger


def saveModelAnswer():
    print("do you want to save the model? (y/n)")
    answer = input()

    if answer == 'y':
        print("Saving model...")
        model.save_model()
    else:
        print("Model not saved")

def getMaxIndex(array):
    maxIndex = 0
    maxVal = 0
    for i in range(len(array)):
        if array[i] > maxVal:
            maxVal = array[i]
            maxIndex = i
    return maxIndex
    
if __name__ == '__main__':
    # Windows Support 
    if os.name == 'nt':
        from multiprocessing import freeze_support
        freeze_support()
    Logger.resetFile()

    model = ar50.AmbrogioNet50()
    if input("Do you want to train the model? (y/n): ").lower() == 'y':
        model.train_model(mode = TestingMode.TestWithRealImages,earlyStoppingType=ar50.EarlyStoppingType.F1_Score)
        # Logger.logTagged("INFO","Training completed, starting the fine tuning phase...")
        # model.train_model(num_epochs=20, patience=4, mode=TestingMode.OnlyRealImages)        
        # Logger.logTagged("INFO","Fine Tuning with Only Real Images completed, starting the Testing phase...")
    else:
        model.load_model()
    model.test_model(mode = TestingMode.TestWithRealImages)
    Logger.logTagged("INFO","Testing complete")
    saveModelAnswer()
    model = ResNet50FromScratch(num_classes=3)
    model.load_model()
    
    import numpy as np
    import torch
    
    dataManager = dsm.DataSetManager()
    _,_,test = dataManager.partitionDataSetEqualy()
    model.eval()
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for inputs in test:
            outputs = model.predict(inputs)  # outputs: list di 3 valori di probabilità
            predicted_class = np.argmax(outputs)  # oppure torch.tensor(outputs).argmax().item()
            all_preds.append(predicted_class)

            # Etichetta vera (supponendo che ritorni una sola label per immagine)
            all_labels.append(np.argmax(dataManager.getCorrentPredictionOfImage(inputs)))
    from utilities.plotConfusionMatrix import plotConfusionMatrix
    from sklearn.metrics import classification_report, f1_score
    from utilities import getClasses as gc
    # Confusion Matrix
    plotConfusionMatrix(all_preds, all_labels, title='Confusion Matrix - ResNet50', cmap='Blues')

    # Report con precision, recall, f1-score per classe
    report = classification_report(all_labels, all_preds, digits=4,target_names=gc.getClasses())
    Logger.logTagged("TESTING",f"Classification Report:\n {report}")

    # Errore medio di classificazione
    accuracy = np.mean(np.array(all_preds) == np.array(all_labels))
    classification_error = 1.0 - accuracy
    # f1 score 
    f1 = f1_score(all_labels, all_preds, average='macro')
    Logger.logTagged("TESTING",f"Errore medio di classificazione: {classification_error:.4f}")
    
    Logger.logTagged("INFO","Testing complete for ResNet50FromScratch")

    # model.load_model()
    # basePath = r"C:\Users\utente\Desktop\ele.jpg"
    # model.predict(basePath)


