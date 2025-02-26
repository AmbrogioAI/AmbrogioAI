@echo off
set REQUIREMENTS_FILE=dependencies.txt
:: Installa le dipendenze se il file requirements.txt esiste
if exist %REQUIREMENTS_FILE% (
    echo Installazione delle dipendenze da %REQUIREMENTS_FILE%...
    pip install --upgrade pip
    pip install tensorflow keras
    pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cu118
    pip install -r %REQUIREMENTS_FILE%
    echo Installazione completata.
) else (
    echo Attenzione: %REQUIREMENTS_FILE% non trovato. Nessuna dipendenza installata.
)

echo Setup completato.
