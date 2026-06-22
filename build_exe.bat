@echo off
pip install -r requirements.txt
if exist dijkstra*.pyd del /q dijkstra*.pyd
if exist graph_io*.pyd del /q graph_io*.pyd
if exist elnino_core*.pyd del /q elnino_core*.pyd
python setup.py build_ext --inplace
pyinstaller --onefile --name ElNino main.py --add-data "dane.txt;."
pause
