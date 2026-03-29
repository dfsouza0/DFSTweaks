@echo off
echo [DFSTweaks] Instalando dependencias...
pip install customtkinter pyinstaller

echo.
echo [DFSTweaks] Compilando EXE...
pyinstaller --noconfirm --onefile --windowed --name "DFSTweaks" --collect-all customtkinter main.py

echo.
echo [DFSTweaks] Pronto! O EXE esta em: dist\DFSTweaks.exe
pause
