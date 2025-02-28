@echo off
clear
:: Navigate to the "script" directory
cd script
echo Installing dependencies...

:: Set file permissions and execute the install script
:: On Windows, we don't need chmod, so this step is removed
call installDependencies.bat

:: Go back to the main directory
cd ..


cd backend
python main.py