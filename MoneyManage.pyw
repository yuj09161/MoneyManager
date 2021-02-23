import os
import subprocess

subprocess.run(
    [
        'pyw',
        os.path.dirname(os.path.abspath(__file__)) + '/src/__main__.py'
    ],
    creationflags=subprocess.CREATE_NO_WINDOW,
    check=False
)
