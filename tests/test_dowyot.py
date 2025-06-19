import pytest
from DowYotMp3 import mp4_to_mp3, download

def test_mp4_to_mp3():
    try:
        mp = mp4_to_mp3("tests/test.mp4", "tests/test.mp3")
        mp.root.destroy()
        assert False
    except Exception as e:
        assert True

def test_download():
    try:
        dow = download("lldladls", "tests/test.mp3")
        dow.root.destroy()
        assert False
        
    except Exception as e:
        assert True
