#!/usr/bin/env bash
set -euo pipefail

python3 -m pip install -r requirements.txt

rm -f dijkstra*.pyd graph_io*.pyd elnino_core*.pyd
rm -f dijkstra*.so graph_io*.so elnino_core*.so

python3 setup.py build_ext --inplace
pyinstaller --onefile --name ElNino main.py --add-data "dane.txt:."
