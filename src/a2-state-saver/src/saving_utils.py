import json, re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("<cert>.json")
firebase_admin.initialize_app(cred, {'databaseURL': "<firedbase address>"})
ref = db.reference("/")

def idValidation(id):
    onlyAlphaNumericSpecial = isAlphanumericSpecial(id)
    onlySpecial = not hasOnlyDashUnderscore(id)
    result = onlyAlphaNumericSpecial and onlySpecial
    reason = ""
    if not result:
        if not onlySpecial:
            reason = "ID can't just contain dashes or underscores. You need to enter Letters or Numbers too"
        else:
            reason = "ID can only contain Letters, Numbers, Dashes, and Underscores"
    return {"result": result, "reason": reason}

def isAlphanumericSpecial(id):
    if(re.match("^[A-Za-z0-9_-]*$", id)):
        return True
    else:
        return False

def hasOnlyDashUnderscore(id):
    if(re.match("^[_-]*$", id)):
        return True
    else:
        return False

# File Functions
def loadFile(mode):
    return open("storage.json", mode)

def setFile():
    try:
        db_contents = ref.get()
        # If DB is empty then populate file with empty json {}
        if type(db_contents) == type(None):
            db_contents = {}
            print("DB is empty so adding empty {}")
        writeFile(json.loads(db_contents))
    except Exception:
        print("There's a problem with setting the file")

def readFile():
    contents = ""
    try:
        with loadFile("r") as storage_file:
            contents = json.load(storage_file)
    except:
        contents = {}
    return contents

def writeFile(contents):
    # Write new record to file
    save_file = loadFile("w+")
    save_file.write(json.dumps(contents))
    save_file.close()
    print("Wrote to file")

def addToDB():
    contents = readFile()
    ref.set({})
    ref.set(json.dumps(contents))

def deleteFromDB():
    ref.delete()


# Storage Operation Functions
def getRecord(id):
    current_contents = readFile()
    if id in current_contents: # Found
        return current_contents[id]
    return -1 # Record not found

def addToFile(new_id,data):
    current_contents = readFile()
    # Ensure new record uses a new ID
    if getRecord(new_id) == -1:
        print (f"{new_id} does not exist")
        current_contents[new_id] = data # Append our new data to the list of current data
        writeFile(current_contents)
        addToDB()
        return True
    else:
        print (f"{new_id} already exists")
        return False

def deleteRecord(id):
    current_contents = readFile()
    if id in current_contents:
        del current_contents[id]
        writeFile(current_contents)
        # deleteFromDB()
        addToDB()
        return True
    return False
