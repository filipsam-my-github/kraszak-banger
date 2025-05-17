pip uninstall pyagme
pip install pyagme-ce
pip install wxPython
pip install sortedcontainers
pip install moderngl
pip install pytest
pip install pyautogui
pip install eyed3
pip install numpy 
pyinstaller --onefile --windowed --icon "data/games_ico.ico" --name "Your Build" --hidden-import "glcontext"  "main.py"