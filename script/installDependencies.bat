@echo off
set VENV_DIR=venv
set REQUIREMENTS_FILE=dependencies.txt

:: Controlla se Python è installato
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Errore: Python3 non è installato.
    exit /b 1
)
cd ..
:: Crea l'ambiente virtuale
python -m venv %VENV_DIR%
echo Ambiente virtuale creato in %VENV_DIR%

:: Attiva l'ambiente virtuale
call %VENV_DIR%\Scripts\activate
python -m pip install --upgrade pip setuptools

cd script
:: Installa le dipendenze se il file requirements.txt esiste
if exist %REQUIREMENTS_FILE% (
    echo Installazione delle dipendenze da %REQUIREMENTS_FILE%...
    pip install --upgrade pip
    pip install -r %REQUIREMENTS_FILE%
    echo Installazione completata.
) else (
    echo Attenzione: %REQUIREMENTS_FILE% non trovato. Nessuna dipendenza installata.
)

echo Setup completato.
