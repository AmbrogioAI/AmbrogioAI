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

    model = ar50.AmbrogioNet50(optimizer=Optimazer.Adam)
    if input("Do you want to train the model? (y/n): ").lower() == 'y':
        model.train_model(mode = TestingMode.TestWithRealImages)
        Logger.logTagged("INFO","Training completed, starting the fine tuning phase...")
        model.train_model(num_epochs=0, patience=4, mode=TestingMode.OnlyRealImages)        
        Logger.logTagged("INFO","Fine Tuning with Only Real Images completed, starting the Testing phase...")
    else:
        model.load_model()
    model.test_model(mode = TestingMode.TestWithRealImages)
    Logger.logTagged("INFO","Testing complete")
    saveModelAnswer()

    # model.load_model()
    # basePath = r"C:\Users\utente\Desktop\ele.jpg"
    # model.predict(basePath)


