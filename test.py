import utilities.DataSetManager as dsm
import classes.AmbrogioResNet50 as ar50
from classes.AmbrogioResNet50 import Optimazer

if __name__ == '__main__':
    model = ar50.AmbrogioNet50(optimizer=Optimazer.Adam)
    
    model.predict(dsm.DataSetManager().getRandomImage())
