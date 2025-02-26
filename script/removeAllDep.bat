@echo off 

echo Rimuovendo tutti i pacchetti installati...

:: Creiamo un file temporaneo con l'elenco dei pacchetti
pip freeze > temp_requirements.txt

:: Disinstalliamo tutti i pacchetti
pip uninstall -r temp_requirements.txt -y

:: Cancelliamo il file temporaneo
del temp_requirements.txt

echo Tutti i pacchetti sono stati rimossi con successo!
pause
