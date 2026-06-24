import os
import sys

from streamlit.web import cli

BASE_DIR = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)

sys.argv = [
    "streamlit",
    "run",
    os.path.join(BASE_DIR, "init.py"),
]

sys.exit(cli.main())
