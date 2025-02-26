:: Create a virtual environment (Windows version)
cls

:: Navigate to the "script" directory
cd script
echo Installing dependencies...

:: Set file permissions and execute the install script
:: On Windows, we don't need chmod, so this step is removed
call installDependencies.bat

:: Go back to the main directory
cd ..


echo Everything is ready to go!

:: Menu di scelta per l'utente
echo.
echo ========================================
echo Seleziona un'opzione:
echo 1 - Avvia il modello ResNet50
echo 2 - Avvia il modello Simple
echo 3 - Esci
echo ========================================
set /p scelta="Inserisci il numero della tua scelta: "

:: Stampa la scelta dell'utente
if "%scelta%"=="1" (
    echo "starting AmbrogioResNet50..."
    python AmbrogioResNet50Routine.py
) else if "%scelta%"=="2" (
    echo "Starting AmbrogioSimple..."
    python trainNN.py
) else if "%scelta%"=="3" (
    echo Uscita in corso...
    exit /b
) else (
    echo Scelta non valida. Riprova.
)
