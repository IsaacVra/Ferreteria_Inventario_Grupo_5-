@echo off
echo Starting Ferreteria Backend Server...
cd /d "%~dp0"
call ferreteria_venv\Scripts\activate.bat
python app.py
pause
