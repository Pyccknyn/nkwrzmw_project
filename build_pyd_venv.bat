@echo off
setlocal

if not exist .venv\Scripts\python.exe (
    py -m venv .venv
)

call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

if exist dijkstra*.pyd del /q dijkstra*.pyd
if exist graph_io*.pyd del /q graph_io*.pyd
if exist elnino_core*.pyd del /q elnino_core*.pyd

python setup.py build_ext --inplace

echo.
echo Gotowe. Powinien powstac jeden plik elnino_core*.pyd.
pause
