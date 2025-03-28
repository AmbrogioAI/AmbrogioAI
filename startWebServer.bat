@echo off
cls
:: Navigate to the "script" directory
cd script
echo Installing dependencies...

:: Set file permissions and execute the install script
:: On Windows, we don't need chmod, so this step is removed
call installDependencies.bat

:: Go back to the main directory
cd ..

:: cloudflared tunnel -url http://127.0.0.1:5000

cd backend
start cmd /k python main.py && cloudflared tunnel -url http://127.0.0.1:5000