
from enum import Enum

class TestingMode(Enum):
    """Modalità di test del modello"""
    TestWithRealImages = 0
    TestWithRandomImages = 1
    