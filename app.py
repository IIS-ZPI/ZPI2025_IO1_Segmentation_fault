import os
import sys

from streamlit.web import cli

sys.argv = [
    "streamlit",
    "run",
    os.path.abspath("init.py"),
]

sys.exit(cli.main())
