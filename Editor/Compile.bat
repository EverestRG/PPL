python -m PyInstaller --noconfirm --onefile --windowed --name "Editor" --add-data "./assets;assets/" --icon "assets/icon.ico"  Editor.py
move .\dist\Editor.exe .\
rd /s/q .\build
rd /s/q .\dist
del /Q .\Editor.spec
pause