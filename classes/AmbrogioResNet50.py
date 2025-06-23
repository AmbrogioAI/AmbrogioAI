import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms
from torchvision.models import ResNet50_Weights
import utilities.getClasses as gc
import utilities.DataSetManager as dsm
from enum import Enum
from classes.TestingMode import TestingMode
from classes.ModelInterface import Model
from utilities.ShowPredictionTable import showPrediction
import torch
import torch.nn.functional as F
from torchvision import transforms
from PIL import Image
from sklearn.metrics import classification_report, confusion_matrix, f1_score
import numpy as np
from utilities.Logger import Logger
from utilities.plotConfusionMatrix import plotConfusionMatrix

class Optimazer(Enum):
    """ottimizzatori supportati dal modello"""
    Adam = 0
    RMSprop = 1
    StochasticGradientDescent = 2



class AmbrogioNet50(Model):
    def __init__(self,lr=0.001, momentum=0.95, optimizer=Optimazer.Adam):
        self.name = 'AmbrogioNet50'
        self.model = models.resnet50(weights=ResNet50_Weights.DEFAULT)
        
        # Sostituire l'ultimo fully connected layer (fc)
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, len(gc.getClasses()))  # n classi in output layer 
        
        self.setDevice()
        # imposta la loss function
        self.criterion = nn.CrossEntropyLoss()
        # imposta l'ottimizzatore
        if optimizer == Optimazer.Adam:
            self.optimizer = self.optimizerResolver(optimizer)(self.model.parameters(), lr=lr)
        else:
            self.optimizer = self.optimizerResolver(optimizer)(self.model.parameters(), lr=lr, momentum=momentum)
        
        # imposta il learning rate scheduler
        self.scheduler = optim.lr_scheduler.StepLR(self.optimizer, step_size=7, gamma=0.1)
        
    def optimizerResolver(self,mode:Optimazer) -> optim:
        if mode == Optimazer.Adam:
            return optim.Adam
        elif mode == Optimazer.RMSprop:
            return optim.RMSprop
        elif mode == Optimazer.StochasticGradientDescent:
            return optim.SGD
        
        raise Exception("Optimizer not supported")

    
    def train_model(self, num_epochs=100,patience=5,delta=0.001,mode = TestingMode.TestWithRealImages):
        '''
        Funzione per addestrare il modello
        :param num_epochs: numero di epoche per l'addestramento
        :param patience: numero di epoche senza miglioramento prima di fermare l'addestramento
        :param delta: soglia minima per considerare l'avvenuta del miglioramento dopo una epoca
        '''
        dataManager = dsm.DataSetManager()
        dataloaders, dataset_sizes = dataManager.getSetForRes50(mode = mode)

        # Inizializza le variabili per il monitoraggio del miglioramento
        best_F1 = 0.0
        epochs_without_improvement = 0

        for epoch in range(num_epochs):
            Logger.logTagged("TRAINING",f'Epoch {epoch}/{num_epochs - 1}')
            Logger.log('-' * 10)

            # Ogni epoca ha una fase di addestramento e una di validazione
            for phase in ['train', 'val']:
                if phase == 'train':
                    self.model.train()  # Imposta il modello in modalità addestramento
                else:
                    self.model.eval()   # Imposta il modello in modalità valutazione

                running_loss = 0.0
                running_corrects = 0
                all_preds = []
                all_labels = []

                # Itera sui dati
                for inputs, labels in dataloaders[phase]:
                    inputs = inputs.to(self.device)
                    labels = labels.to(self.device)

                    # Azzera i gradienti dei parametri
                    self.optimizer.zero_grad()

                    # Forward pass
                    with torch.set_grad_enabled(phase == 'train'):
                        outputs = self.model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = self.criterion(outputs, labels)

                        # Backward + ottimizzazione solo nella fase di addestramento
                        if phase == 'train':
                            loss.backward()
                            self.optimizer.step()

                    # Statistiche
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)
                    all_preds.extend(preds.cpu().numpy())
                    all_labels.extend(labels.cpu().numpy())

                if phase == 'train':
                    self.scheduler.step()

                epoch_loss = running_loss / dataset_sizes[phase]
                epoch_acc = running_corrects.double() / dataset_sizes[phase]
                epoch_f1 = f1_score(all_labels, all_preds, average='macro')

                Logger.logTagged("TRAINING",f'{phase} Loss: {epoch_loss:.4f} Acc: {epoch_acc:.4f} F1: {epoch_f1:.4f}')

                if phase == 'val':
                    if epoch_acc > best_F1 + delta:
                        best_F1 = epoch_f1
                        epochs_without_improvement = 0
                        Logger.logTagged("TRAINING",f"Nuovo miglioramento F1 macro: {best_F1:.4f}")
                    else:
                        epochs_without_improvement += 1
                        Logger.logTagged("TRAINING",f"Nessun miglioramento F1 macro: {epoch_f1:.4f} (best: {best_F1:.4f})")

                    if epochs_without_improvement >= patience:
                        Logger.logTagged("END TRAINING",f"Early stopping! Nessun miglioramento per {patience} epoche consecutive.")
                        return
        Logger.logTagged("END TRAINING",f"Training completato! Miglioramento finale F1 macro: {best_F1:.4f}")
        #return self.model


    def predict(self, imgPath):
        
        # Carica l'immagine e preparala per la predizione
        img = Image.open(imgPath).convert('RGB')
        # img = Image.fromarray(rembg.remove(np.array(img)))
        img = img.resize((224, 224))
        img = transforms.ToTensor()(img)
        img = img.unsqueeze(0)  # Aggiunge una dimensione per il batch
        img = img.to(self.device)
        
        Logger.logTagged("PREDICTING",f'Predicting image {imgPath} ...')
        
        # Esegui la predizione
        self.model.eval()
        with torch.no_grad():
            output = self.model(img)
            
        # Calcola le probabilità applicando softmax all'output
        probabilities = F.softmax(output, dim=1).squeeze()  # Riduce la dimensione extra
        
        probabilities = [prob.item() for prob in probabilities]
        
        showPrediction(probabilities)
            
        return probabilities  # Restituisce le probabilità di tutte le classi come array
    
    
    def test_model(self,mode = TestingMode.TestWithRealImages,printConfusionMatrix = True):
        dataManager = dsm.DataSetManager()
        dataloaders, dataset_sizes = dataManager.getSetForRes50(mode = mode)
        self.model.eval()
        all_preds = []
        all_labels = []

        with torch.no_grad():
            for inputs, labels in dataloaders['test']:
                inputs = inputs.to(self.device)
                labels = labels.to(self.device)

                outputs = self.model(inputs)
                _, preds = torch.max(outputs, 1)

                all_preds.extend(preds.cpu().numpy())
                all_labels.extend(labels.cpu().numpy())
        
        # Confusion Matrix
        if printConfusionMatrix:
            plotConfusionMatrix(all_preds, all_labels, title='Confusion Matrix - ResNet50', cmap='Blues')

        # Report con precision, recall, f1-score per classe
        report = classification_report(all_labels, all_preds, digits=4,target_names=gc.getClasses())
        Logger.logTagged("TESTING",f"Classification Report:\n {report}")

        # Errore medio di classificazione
        accuracy = np.mean(np.array(all_preds) == np.array(all_labels))
        classification_error = 1.0 - accuracy
        Logger.logTagged("TESTING",f"Errore medio di classificazione: {classification_error:.4f}")
        return accuracy