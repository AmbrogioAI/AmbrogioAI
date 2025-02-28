#!/bin/bash

# Cancella lo schermo (clear non funziona in tutti gli script, quindi lo rimuoviamo per sicurezza)
clear

# Naviga nella directory "script"
cd script || { echo "Errore: impossibile accedere alla cartella script"; exit 1; }

echo "Installing dependencies..."

# Imposta i permessi di esecuzione per lo script di installazione
chmod +x installDependecies.sh

# Esegue lo script di installazione
./installDependecies.sh

# Torna alla directory principale
cd ..

# Naviga nella cartella "backend"
cd backend || { echo "Errore: impossibile accedere alla cartella backend"; exit 1; }

# Avvia lo script Python con la versione specificata
python3.11 main.py