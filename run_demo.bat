@echo off
setlocal

if not exist ".venv\Scripts\python.exe" (
    echo Could not find .venv\Scripts\python.exe
    echo Run this first:
    echo python -m venv .venv
    echo .venv\Scripts\python.exe -m pip install -r requirements.txt
    pause
    exit /b 1
)

echo Opening disease spread simulation GUI...
.venv\Scripts\python.exe main.py --mode gui

echo.
echo GUI closed.
pause
