import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
# [CRUX-MK]
import importlib

m = importlib.import_module("166")

def test_add():
    assert m.add(2, 3) == 5
