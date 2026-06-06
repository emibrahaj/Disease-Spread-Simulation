@echo off
setlocal

echo Running parallel disease spread simulation...
.venv\Scripts\python.exe main.py --mode parallel --grid-size 120 --steps 80 --initial-infected 10 --processes 4 --save-plots

echo.
echo Running sequential vs parallel comparison...
.venv\Scripts\python.exe main.py --mode compare --grid-size 160 --steps 80 --initial-infected 16 --processes 4

echo.
echo Demo finished.
echo Check generated charts in results\screenshots\charts
pause
