import python_checking
import pytest
import requests
import zipfile
import os
import sys
import shutil
import stat
import chess
import chess.engine
import train

platform = sys.platform
file_extension = ".exe" if platform == "win32" else ""

def test_nothing():
    assert True

def check_os():
    if platform == "linux":
        assert True
        return

    else:
        assert False

def download_me():
    response = requests.get("https://github.com/MarcoNITE/MarcoEngine/archive/master.zip", allow_redirects=True)
    with open("master.zip", "wb") as file:
        file.write(response.content)
    with zipfile.ZipFile("master.zip", "r") as zip_ref:
        zip_ref.extractall(".")

def delete_downloaded_zip():
    os.remove("master.zip")

def download_sf():
    windows_or_linux = "win" if platform == "win32" else "linux"
    response = requests.get(f"https://stockfishchess.org/files/stockfish_14.1_{windows_or_linux}_x64.zip", allow_redirects=True)
    with open("sf_zip.zip", "wb") as file:
        file.write(response.content)
    shutil.copyfile(f"stockfish_14.1_{windows_or_linux}_x64/stockfish_14.1_{windows_or_linux}_x64{file_extension}", f"./TEMP/sf{file_extension}")
    shutil.copyfile(f'sf{file_extension}", f"./TEMP/sf2{file_extension}")
    if windows_or_linux == "linux":
        st = os.stat(f"sf{file_extension}")
        os.chmod(f"sf{file_extension}", st.st_mode | stat.S_IEXEC)
        st = os.stat(f"sf2{file_extension}")
        os.chmod(f"sf2{file_extension}", st.st_mode | stat.S_IEXEC)

def test_train():
    test_board = chess.Board()
    _engine = chess.engine.SimpleEngine.popen_uci("./TEMP/sf") # openning engine
    train.train()

check_os()
download_me()
delete_downloaded_zip()
download_sf()

