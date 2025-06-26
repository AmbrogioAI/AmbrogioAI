from itertools import product
from classes.AmbrogioResNet50 import AmbrogioNet50,Optimazer
from classes.TestingMode import TestingMode
import os

if __name__ == '__main__':
    if os.name == 'nt':
        from multiprocessing import freeze_support
        freeze_support()
    param_grid = {
        'lr': [0.001, 0.0001,0.01],
        'optimizer': [Optimazer.Adam, Optimazer.StochasticGradientDescent,Optimazer.RMSprop],
        'momentum': [0.9, 0.95,1],
        'step_size': [7, 10],
        'gamma': [0.1, 0.01]
    }

    best_score = 0.0
    best_model = None
    best_params = {}

    for lr, optimizer, momentum, step_size, gamma in product(param_grid['lr'], param_grid['optimizer'], param_grid['momentum'],param_grid['step_size'], param_grid['gamma']):
        model = AmbrogioNet50(lr=lr, optimizer=optimizer, momentum=momentum, step_size=step_size, gamma=gamma)
        model.load_model() 
        
        model.train_model(num_epochs=5, patience=3, mode=TestingMode.TestWithRealImages)

        # Valutazione su validation o test set
        acc,f1 = model.test_model(mode=TestingMode.TestWithRealImages,printConfusionMatrix=False) 
        
        if f1 > best_score:
            best_score = f1
            best_model = model
            best_params = {
                'lr': lr,
                'optimizer': optimizer,
                'momentum': momentum,
                'step_size': step_size,
                'gamma': gamma
            }

    print(f"Migliori parametri: {best_params}, f1-score: {best_score}")
