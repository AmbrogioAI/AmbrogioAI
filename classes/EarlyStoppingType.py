from enum import Enum

class EarlyStoppingType(Enum):
    """Metrica usata per l'Early Stopping durante il training del modello"""
    Accuracy = 0
    F1_Score = 1
    NONE = 2
    