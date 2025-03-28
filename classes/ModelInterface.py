from typing import Any
from PIL import Image
import torchvision.transforms as transforms
import torch

class Model:
    def predict(self,imgPath) -> list|None:
        '''Given an image path, print/return the prediction of the model'''
        pass

    def computeImage(self,imgPath) -> Any:
        '''Given an image path, return the image in the correct format for the model'''
        image = Image.open(imgPath)

        # Definisci le trasformazioni (ridimensionamento e normalizzazione)
        transform = transforms.Compose([
            transforms.Resize((224, 224)),  # ResNet50 accetta input di 224x224
            transforms.ToTensor(),  # Converte in tensor
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalizzazione standard per ResNet
        ])

        # Applica le trasformazioni
        image = transform(image).unsqueeze(0)  # Aggiunge la dimensione batch
        return image
        pass