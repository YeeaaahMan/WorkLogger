import json
from os import environ

path = environ['APPDATA'] + "\\WorkLogger.json"

def create_config():
    c = json.loads("""{
        "login":"",
        "issue": {}
    }""")
    write_config(c)

def read_config():
    try:
        CFG = json.load( open(path) )
    except:
        create_config()
        CFG = json.load( open(path) )

    return CFG

def write_config(settings):
    fw = open(path, "w")
    json.dump(settings, fw, indent=4)
    fw.close()
