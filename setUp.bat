:: Create a virtual environment (Windows version)
python -m venv venv
call venv\Scripts\activate

:: Navigate to the "script" directory
cd script
echo Installing dependencies...

:: Set file permissions and execute the install script
:: On Windows, we don't need chmod, so this step is removed
call installDependencies.bat

:: Go back to the main directory
cd ..

echo Everything is ready to go!
echo Now to run the project, you have to run start[NameOfModel].bat
