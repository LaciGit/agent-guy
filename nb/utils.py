import sys
from pathlib import Path

import logging

logging.basicConfig(level=logging.INFO)


def append_sys_path() -> None:
    # must be in defined folder struct
    module_path = Path(".").resolve().parent
    sys.path.insert(0, str(module_path))

    logging.info(f"Appended {module_path} to sys.path")
