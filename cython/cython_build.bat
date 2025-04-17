pyinstaller --noconfirm --onefile --windowed --icon "data/games_ico.ico" --name "cython Build" --log-level "ERROR" --hidden-import "glcontext"  "main.py"
