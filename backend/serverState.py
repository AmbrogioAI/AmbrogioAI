from classes.ModelInterface import Model
import rembg

class ServerState:
    modelChosen = None
    _instance = None
    session = rembg.new_session(model_name="u2net_cloth_seg")
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ServerState, cls).__new__(cls)
            cls._instance.modelChosen = None  # Variabile di stato
        return cls._instance
        
    def set_model(self, model):
        # if modelChosen is not None, remove it from memory
        if self.modelChosen is not None:
            del self.modelChosen
        self.modelChosen = model

    def get_model(self):
        return self.modelChosen
