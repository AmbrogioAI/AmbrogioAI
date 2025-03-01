#!/bin/bash

# Abilita l'uscita immediata in caso di errore
set -e

# Controlla se il file dependencies.txt esiste
if [ ! -f dependencies.txt ]; then
    echo "The dependencies.txt file doesn't exist."
    exit 1
fi

pip install tensorflow keras
pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1

# Legge il file dependencies.txt riga per riga
while IFS= read -r dependency; do
    # Controlla se il pacchetto è già installato
    if ! pip show "$dependency" > /dev/null 2>&1; then
        echo "Installing $dependency"
        pip install "$dependency"
    else
        echo "$dependency already installed."
    fi
done < dependencies.txt

# Installa le dipendenze per la fotocamera Raspberry Pi
sudo apt update && sudo apt upgrade -y 
sudo apt install qt5-qmake qtbase5-dev
sudo apt install -y libraspberrypi-dev libraspberrypi-bin
pip install pyqt5
pip install prctl
sudo apt install -y libcap-dev libffi-dev libjpeg-dev 
pip install picamera2

echo "All dependencies are installed."
