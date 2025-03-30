from classes.AmbrogioResNet50 import Optimazer
from utilities import DataSetManager as dsm
from classes import AmbrogioResNet50 as ar50
from classes.resNet50FromScratch import ResNet50 as ResNet50FromScratch
import os
from matplotlib import pyplot as plt

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

def testModels():
    # Windows Support 
    if os.name == 'nt':
        from multiprocessing import freeze_support
        freeze_support()
    
    bigModel = ar50.AmbrogioNet50(optimizer=Optimazer.Adam)
    bigModel.load_model()
    normalModel = ResNet50FromScratch(3)
    normalModel.load_model()

    dataManager = dsm.DataSetManager()

    bigModelCorrectness = 0
    normalModelCorrectness = 0

    nTest = 400
    bigModelCorrectnessList = []
    normalModelCorrectnessList = []

    for i in range(nTest):
        print(f"Testing image {i+1} of 400")
        imagePath = dataManager.getRandomImage()
        
        resNet50Prediction = bigModel.predict(imagePath)
        normalModelPrediction = normalModel.predict(imagePath)
        correctPrediction = dataManager.getCorrentPredictionOfImage(imagePath)
        print("")
        if getMaxIndex(resNet50Prediction) == getMaxIndex(correctPrediction):
            bigModelCorrectness += 1
            bigModelCorrectnessList.append(bigModelCorrectness)
        if getMaxIndex(normalModelPrediction) == getMaxIndex(correctPrediction):
            normalModelCorrectness += 1
            normalModelCorrectnessList.append(normalModelCorrectness)
        
    print("Big model correctness: ",bigModelCorrectness/nTest*100,"%")
    print("Normal model correctness: ",normalModelCorrectness/nTest*100,"%")
    plt.plot(bigModelCorrectnessList, label="Big Model")
    plt.legend()
    plt.show()
    plt.plot(normalModelCorrectnessList, label="Normal Model")
    plt.legend()
    plt.show()



    
if __name__ == '__main__':
    # Windows Support 
    if os.name == 'nt':
        from multiprocessing import freeze_support
        freeze_support()
    
    model = ar50.AmbrogioNet50(optimizer=Optimazer.Adam)
    model.train_model(250)

    print("Training complete")
    testModels()
    print("Testing complete")
    saveModelAnswer()


