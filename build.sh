# welcome
GREEN='\033[0;32m' # green color
NC='\033[0m' # No Color
printf "Welcome to ${GREEN} MarcoEngine ${NC} \n"

# Installing Python modules
echo Installing Python modules..
pip install -r requirements.txt

# Building with Nuitka
echo Compilation...
python3 -m compileall .
python3 -m nuitka train.py -o train
python3 -m nuitka uci.py -o uci
python3 -m nuitka config.py -o config
python3 -m nuitka python_checking.py -o python_checking
python3 -m nuitka tests.py -o tests

echo Done!
