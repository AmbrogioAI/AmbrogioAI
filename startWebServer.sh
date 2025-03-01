#!/bin/bash

# Cancella lo schermo
clear

# Controlla se Python 3.11 è installato
if ! command -v python3.11 &>/dev/null; then
    echo "Python 3.11 non trovato. Installazione in corso..."
    
    # Rimuove altre versioni di Python
    sudo apt remove --purge -y python3 python3.*
    sudo apt autoremove -y
    sudo apt update
    
    # Installa Python 3.11
    sudo apt install -y python3.11 python3.11-venv python3.11-dev
    
    # Verifica l'installazione
    if ! command -v python3.11 &>/dev/null; then
        echo "Errore: impossibile installare Python 3.11."
        exit 1
    fi
else
    echo "Python 3.11 è già installato."
fi

# Naviga nella cartella "backend"
cd backend || { echo "Errore: impossibile accedere alla cartella backend"; exit 1; }

# Crea un ambiente virtuale (venv) se non esiste
if [ ! -d "venv" ]; then
    echo "Creazione dell'ambiente virtuale..."
    python3.11 -m venv venv
fi

# Attiva l'ambiente virtuale
source venv/bin/activate
pip list
# Aggiorna pip e installa le dipendenze, se presenti
echo "Installazione delle dipendenze del progetto..."
pip install --upgrade pip
cd ..
cd script
# Imposta i permessi di esecuzione per lo script di installazione e lo esegue
chmod +x installDependecies.sh
./installDependecies.sh

cd ..
cd backend
# Avvia lo script Python con l'ambiente virtuale attivato
echo "Avvio di main.py..."
python main.py
