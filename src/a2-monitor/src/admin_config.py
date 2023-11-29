import json

def openAdminConfig(mode):
    return open("configs/admin_config.json", mode)

def readConfig():
    contents = {"monitor": True, "frequency":"30"}
    try:
        with openAdminConfig("r") as admin_c:
            contents = json.load(admin_c)
    except Exception:
        contents = {"monitor": True, "frequency": "30"}
        writeConfig(contents)
    return contents

def writeConfig(msg):
    try:
        admin_f = openAdminConfig("w+")
        admin_f.write(str(json.dumps(msg)))
        admin_f.close()
        return True
    except Exception:
        return False
