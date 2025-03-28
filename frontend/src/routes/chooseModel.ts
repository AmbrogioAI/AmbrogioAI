import axios from "axios";
import { routePrefix } from "../config/systemVariables";

export enum PossibleModels {
  "resNet50" = 0,
  "simple" = 1,
}

export async function chooseModel(chooseModel: PossibleModels) : Promise<string> {
  try {
    // Esegui la richiesta POST per selezionare il modello
    const response = await axios.post(routePrefix + "/choseModel", {
      model: chooseModel,
    });

    // Verifica che la risposta contenga il campo modelChosen
    if (response.data && response.data.modelChosen) {
      return response.data.modelChosen;
    } else {
      throw new Error("Risposta del server non valida: 'modelChosen' non trovato");
    }
  } catch (error) {
    // Gestisci gli errori
    console.error("Errore nella scelta del modello:", error);
    throw new Error("Errore durante la selezione del modello. Per favore riprova più tardi.");
  }
}
