import os
import sys
import subprocess

MAIN_LOCATION = os.path.dirname(os.path.abspath(__file__)) + '/src/__main__.py'

subprocess.run(
    [sys.executable, MAIN_LOCATION],
    creationflags=subprocess.CREATE_NO_WINDOW,
    check=False
)
