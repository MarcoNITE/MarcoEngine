import python_checking
import pytest
import requests
import shutil
import zipfile
import os

def test_nothing():
    assert True

def check_os():
    python_checking.check()

def download_me():
    response = requests.get("https://github.com/MarcoNITE/MarcoEngine/archive/master.zip", allow_redirects=True)
    with open("master.zip", "wb") as file:
        file.write(response.content)
    with zipfile.ZipFile("master.zip", "r") as zip_ref:
        zip_ref.extractall(".")

def delete_downloaded_zip():
    os.remove("master.zip")

check_os()
download_me()
delete_downloaded_zip()
