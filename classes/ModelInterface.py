from typing import Any
from PIL import Image
import torchvision.transforms as transforms
import torch

class Model:
    def __init__(self):
        self.name = 'Model'
        self.model = None
        self.device = None
    
    def predict(self,imgPath) -> list|None:
        '''Given an image path, print/return the prediction of the model'''
        pass

    def computeImage(self,imgPath) -> Any:
        '''Given an image path, return the image in the correct format for the model'''
        image = Image.open(imgPath).convert("RGB")

        # Definisci le trasformazioni (ridimensionamento e normalizzazione)
        transform = transforms.Compose([
            transforms.Resize((224, 224)),  # ResNet50 accetta input di 224x224
            transforms.ToTensor(),  # Converte in tensor
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalizzazione standard per ResNet
        ])

        # Applica le trasformazioni
        image = transform(image).unsqueeze(0)  # Aggiunge la dimensione batch
        return image
    
    def save_model(self, path = "AmbrogioResNet50.pth"):
        torch.save(self.model.state_dict(), path)
        
    def load_model(self, path = "AmbrogioResNet50.pth"):
        import os    
        root = os.path.dirname(os.path.abspath(__file__))
        # get the absolute path of the "utilities" folder
        root = os.path.dirname(root)
        self.model.load_state_dict(torch.load(root+"/"+path,map_location=self.device,weights_only=True))
    
    @staticmethod
    def getDevice() ->  torch.device:
        '''Get the device (GPU or CPU) for PyTorch''' 
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        print(f"Device: {'cuda' if torch.cuda.is_available() else 'cpu'}")
        return device
    
    def setDevice(self):
        self.device = Model.getDevice()
        self.model = self.model.to(self.device)