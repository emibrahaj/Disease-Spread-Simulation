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

echo Running parallel disease spread simulation...
.venv\Scripts\python.exe main.py --mode parallel --grid-size 120 --steps 80 --initial-infected 10 --processes 4 --save-plots

echo.
echo Running sequential vs parallel comparison...
.venv\Scripts\python.exe main.py --mode compare --grid-size 160 --steps 80 --initial-infected 16 --processes 4

echo.
echo Running intervention example...
.venv\Scripts\python.exe main.py --mode parallel --grid-size 120 --steps 80 --initial-infected 10 --processes 4 --intervention-step 30 --intervention-probability 0.12 --save-plots

echo.
echo Demo finished.
echo Check generated charts in results\screenshots\charts
echo Timing CSV: results\timing_results.csv
pause
