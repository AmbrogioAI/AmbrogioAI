import numpy as np
import utilities.getClasses as getClasses
from prettytable import PrettyTable
from utilities.Logger import Logger

def showPrediction(predictions):
        table = PrettyTable()
        table.title = "Probabilità di appartenenza alle classi"
        table.align = "l"
        table.border = True
        table.header = True
        
        # Aggiungi le colonne
        table.field_names = ["Etichetta", "Probabilità"]
        for i in range(len(predictions)):
            table.add_row([getClasses.getClasses()[i],predictions[i]])

        # Stampa la tabella
        Logger.logTagged("PREDICTING",table)
        
        Logger.logTagged("PREDICTING",f"La classe predetta è: {getClasses.getClasses()[np.argmax(predictions)]}")