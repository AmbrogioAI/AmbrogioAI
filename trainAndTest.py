from classes.AmbrogioResNet50 import Optimazer
from utilities import DataSetManager as dsm
from classes import AmbrogioResNet50 as ar50
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

    model = ar50.AmbrogioNet50(optimizer=Optimazer.Adam)
    model.train_model()
    Logger.logTagged("INFO","Training complete")
    model.test_model()
    Logger.logTagged("INFO","Testing complete")
    saveModelAnswer()

    # model.load_model()
    # basePath = r"C:\Users\utente\Desktop\ele.jpg"
    # model.predict(basePath)


