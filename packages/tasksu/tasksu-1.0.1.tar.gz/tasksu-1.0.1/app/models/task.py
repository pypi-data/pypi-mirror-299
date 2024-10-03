from datetime import datetime

def task(title, description):
    defaultStatus = "todo"
    return {
        "uid": 0,
        "title": title,
        "description": description,
        "status": defaultStatus,
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
    }
