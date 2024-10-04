## window

pyinstaller --onefile --windowed --add-data "file/index.html:." --add-data "assets/icon.ico:." --icon=assets/icon.ico main.py

## ubuntu

pyinstaller --onefile --windowed --add-data "assets/icon.ico:." --add-data "file/index.html:." --icon=assets/icon.ico main.py
