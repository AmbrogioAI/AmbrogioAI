from classes.AmbrogioResNet50 import Optimazer
from utilities import DataSetManager as dsm
from classes import AmbrogioResNet50 as ar50
import os

if __name__ == '__main__':
    # Windows Support 
    if os.name == 'nt':
        from multiprocessing import freeze_support
        freeze_support()
    
    model = ar50.AmbrogioNet50(optimizer=Optimazer.Adam)
    model.train_model(num_epochs=10)
    model.save_model()
        
    model.predict(dsm.DataSetManager().getRandomImage())
