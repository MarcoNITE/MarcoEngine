# welcome
GREEN='\033[0;32m' # green color
NC='\033[0m' # No Color
printf "Welcome to ${GREEN} MarcoEngine ${NC} \n"

# Installing Python modules
echo Installing Python modules..
pip install -r requriements.txt

# Building with Nuitka
echo Compilation...
python3 -m nuitka train.py
python3 -m nuitka engine.py
python3 -m nuitka config.py
python3 -m nuitka python_checking.py

echo Done!
