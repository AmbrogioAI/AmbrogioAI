import classes.AmbrogioSimple as A
from utilities import getClasses
import classes.FeatureExtractor as fe
import utilities.DataSetManager as dsm
from tqdm import tqdm
from utilities.PhotoTaker import takePhoto
import time
import utilities.ShowPredictionTable as showPrediction

dataSet = dsm.DataSetManager()
featureExtractor = fe.FeatureExtractor()
ambrogio = A.AmbrogioSimple()

print("si vuole caricare lo stato della rete neurale salvato se presente? [y/n]")
if input() == 'y':
    
    with tqdm(total=100) as pbar:
        ambrogio.loadState()
        pbar.update(100)

continueGuessing = True
while continueGuessing:
    path = takePhoto()
    input = featureExtractor.extract_features(path)
    out = ambrogio.predict(input)
    showPrediction.showPrediction(out)
    time.sleep(5)


print("si vuole salvare lo stato della rete neurale? [y/n]")
try:
    if input() == 'y':
        with tqdm(total=100) as pbar:
            ambrogio.saveState()
            pbar.update(100)
except Exception as e:
    print("non ho capito")



