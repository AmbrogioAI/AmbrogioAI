import torch
import torch.nn as nn
import torch.nn.functional as F
from ModelInterface import Model

class BottleneckBlock(nn.Module):
    def __init__(self, in_channels, out_channels, stride=1, downsample=None):
        super(BottleneckBlock, self).__init__()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=1, bias=False)
        self.bn1 = nn.BatchNorm2d(out_channels)
        self.conv2 = nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False)
        self.bn2 = nn.BatchNorm2d(out_channels)
        self.conv3 = nn.Conv2d(out_channels, out_channels * 4, kernel_size=1, stride=1, bias=False)
        self.bn3 = nn.BatchNorm2d(out_channels * 4)
        self.relu = nn.ReLU(inplace=True)
        self.downsample = downsample

    def forward(self, x):
        identity = x
        if self.downsample is not None:
            identity = self.downsample(x)
        
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)

        out = self.conv3(out)
        out = self.bn3(out)

        out += identity
        out = self.relu(out)
        
        return out

class ResNet50(nn.Module,Model):
    def __init__(self, num_classes=1000):
        super(ResNet50, self).__init__()
        self.in_channels = 64
        self.conv1 = nn.Conv2d(3, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        self.layer1 = self._make_layer(64, 3)
        self.layer2 = self._make_layer(128, 4, stride=2)
        self.layer3 = self._make_layer(256, 6, stride=2)
        self.layer4 = self._make_layer(512, 3, stride=2)

        self.avgpool = nn.AdaptiveAvgPool2d((1, 1))
        self.fc = nn.Linear(512 * 4, num_classes)

    def _make_layer(self, out_channels, blocks, stride=1):
        downsample = None
        if stride != 1 or self.in_channels != out_channels * 4:
            downsample = nn.Sequential(
                nn.Conv2d(self.in_channels, out_channels * 4, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels * 4),
            )
        
        layers = []
        layers.append(BottleneckBlock(self.in_channels, out_channels, stride, downsample))
        self.in_channels = out_channels * 4
        for _ in range(1, blocks):
            layers.append(BottleneckBlock(self.in_channels, out_channels))
        
        return nn.Sequential(*layers)

    def forward(self, x):
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)
        
        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)
        
        x = self.avgpool(x)
        x = torch.flatten(x, 1)
        x = self.fc(x)
        
        return x

# Test model
model = ResNet50(num_classes=3)
x = torch.randn(1, 3, 224, 224)
output = model(x)
print(output.shape)  # Should print torch.Size([1, 3])

# image handling

from PIL import Image
import torchvision.transforms as transforms
import torch

# Carica l'immagine
image_path = "C:/Users/utente/Desktop/AmbrogioAI/DataSet/sportivo/sportivo20241029214242.png"

# Assicurati che il modello sia in modalità eval
model.eval()

# Disattiva il calcolo dei gradienti (non necessario per l'inferenza)
with torch.no_grad():
    output = model(model.computeImage(image_path))

# Converti l'output in probabilità con softmax
probabilities = torch.nn.functional.softmax(output[0], dim=0)

print(f"Probailità: {probabilities}")

# Definisci le classi
class_labels = ["Elegante", "Sportivo", "Casual"]

# Trova la classe con la probabilità più alta
predicted_class = class_labels[torch.argmax(probabilities).item()]

print(f"Classe Predetta: {predicted_class}")
