import json
import os
from models import task

DATABASE_PATH = "db"

def saveJson(filename, tasks):
    os.makedirs(DATABASE_PATH, exist_ok=True)
    filepath = os.path.join(DATABASE_PATH, filename)
    with open(filepath, 'w') as file:
        json.dump(tasks, file, indent=4)
        
def loadJson(filename):
    data = []
    filepath = os.path.join(DATABASE_PATH, filename)
    try:
        with open(filepath, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        # Create file
        os.makedirs(DATABASE_PATH, exist_ok=True)
        with open(filepath, "a") as file:
            pass
    
    return data