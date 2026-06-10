import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
# [CRUX-MK]
# NOTE:
# `from 166 import ...` is not valid Python syntax because module names in
# import statements must be identifiers, and `166` is tokenized as a number.
# The test therefore imports the file `166.py` via importlib while still
# testing the requested module contents.

import importlib.util
import pathlib


_module_path = pathlib.Path(__file__).with_name("166.py")
_spec = importlib.util.spec_from_file_location("166", _module_path)
_mod = importlib.util.module_from_spec(_spec)
assert _spec is not None and _spec.loader is not None
_spec.loader.exec_module(_mod)

digital_root = _mod.digital_root
is_dark_factory_code = _mod.is_dark_factory_code
classify_codes = _mod.classify_codes


def test_digital_root_and_classification():
    assert digital_root(166) == 4
    assert digital_root(99999) == 9
    assert is_dark_factory_code(166) is True
    assert is_dark_factory_code(103) is True
    assert is_dark_factory_code(29) is False
    assert classify_codes([166, 103, 29, 400]) == [True, True, False, True]

