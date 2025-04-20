pip uninstall pyagme
pip install pyagme-ce
pip install wxPython
pip install sortedcontainers
pip install moderngl
pip install pytest
pip install pyautogui
pip install eyed3
pip install numpy 
pyinstaller --noconfirm --onefile --windowed --icon "data/games_ico.ico" --name "Your Build" --log-level "ERROR" --hidden-import "glcontext"  "main.py"