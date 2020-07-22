import json
import os

""" Retrieve configs for the client as well as any module configurations"""

with open("../bot.json", "r") as file:
    botConfig = json.load(file)

with open("../modules.json", "r") as file:
    moduleConfig = json.load(file)


PREFIX      = botConfig["prefix"]
DESCRIPTION = botConfig["description"]
ADMINUSERS  = botConfig["adminusers"]
TOKEN       = botConfig["token"]

MODULEPATH  = moduleConfig["path"]