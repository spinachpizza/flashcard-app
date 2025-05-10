import pickle
import os, sys
from pathlib import Path

def get_data_dir():
    """Returns the data folder path next to executable"""
    base_dir = Path(sys.executable).parent if getattr(sys, 'frozen', False) else Path(__file__).parent
    data_dir = base_dir / "data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / "img").mkdir(exist_ok=True)
    return data_dir

def resource_path(relative_path):
    """Handles both bundled and user-generated files"""
    if relative_path.startswith("data/"):
        return str(get_data_dir() / relative_path[5:])
    
    try:
        base_path = sys._MEIPASS
        return os.path.join(base_path, relative_path)
    except Exception:
        return os.path.join(Path(__file__).parent, relative_path)


DATA_DIR = "data"
TOPIC_FILE = f"{DATA_DIR}/topics.pkl"  # Now in data folder
IMG_FILE = f"{DATA_DIR}/imgs.pkl"      # Now in data folder
USER_IMG_DIR = f"{DATA_DIR}/img"       # For user images

# Ensure folders exist on startup
Path(resource_path(DATA_DIR)).mkdir(exist_ok=True)
Path(resource_path(USER_IMG_DIR)).mkdir(exist_ok=True)

# Your save/load functions stay almost the same
def save_data():
    """Saves data to files in data/ folder"""
    with open(resource_path(TOPIC_FILE), 'wb') as file:
        pickle.dump(topics, file)
    
    with open(resource_path(IMG_FILE), 'wb') as file:
        pickle.dump(userimgs, file)

def load_data():
    """Loads data from files in data/ folder"""
    global topics, userimgs
    
    try:
        with open(resource_path(TOPIC_FILE), 'rb') as file:
            topics = pickle.load(file)
    except FileNotFoundError:
        pass  # Initialize if not exists

    try:
        with open(resource_path(IMG_FILE), 'rb') as file:
            userimgs = pickle.load(file)
    except FileNotFoundError:
        pass  # Initialize if not exists





colours = ['#FFFFFF','#36454f','#536872','#47555c',"#2a343b"]

topics = []

userimgs = []




paths = [resource_path("images/settingsw.png"), resource_path("images/check.png"),
         resource_path("images/icon.ico"), resource_path("images/sad.png"),
         resource_path("images/neutral.png"), resource_path("images/happy.png"),
         resource_path("images/wrenchw.png"), resource_path("images/brush.png"),
         resource_path("images/chart.png"), resource_path("images/info.png"),
         resource_path("images/background.png"), resource_path("images/1x1.png")]

try:
    load_data()
    if len(userimgs) == 0:
        userimgs.append(0)
except:
    pass
