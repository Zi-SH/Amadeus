import json

# Load Discord config
with open("bot.json", "r") as f:
    bot = json.load(f)

# Load module settings
# TODO: INPUT VALIDATION
with open("modules.json", "r") as f:
    modules = json.load(f)