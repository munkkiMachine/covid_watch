from pathlib import Path
from datetime import datetime

def get_project_root() -> Path:
    return Path(__file__).parent.parent

def current_date():
    return str(datetime.today().strftime('%Y%m%d'))