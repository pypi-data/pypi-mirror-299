from datetime import datetime

def convertIsoDateTime(isoDateTime):
    # Convert the ISO string to a datetime object
    dt_object = datetime.fromisoformat(isoDateTime)

    readable_format = dt_object.strftime("%B %d, %Y %I:%M %p")
    return readable_format

def printTasks(tasks):
    print(f"{'UID':^5} | {'Title':^30}| {'Description':^30}| {'Status':^15}| {'Created At':^30}| {'Updated At':^30}|")
    for t in tasks:
        createdAt = convertIsoDateTime(t['createdAt'])
        updatedAt = convertIsoDateTime(t['updatedAt'])
        print(f"{t['uid']:^5} | {t['title']:^30}| {t['description']:^30}| {t['status']:^15}| {createdAt:^30}| {updatedAt:^30}|")