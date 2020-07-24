import json
from os import mkdir, path

""" Classes for manipulation command filters, which control whether or not a command can be used in a room. """

# Constants
guildConfigPath = "./guilds"


def generate_new_guild_filter(guildID):
    if not path.isdir(guildConfigPath):
        mkdir(guildConfigPath)

    with open(str(guildID) + ".json", "w") as file:
        _ = file.write(json.dumps({}))

    return True


def check_command_filter(command, guildID):
    guildFile = guildConfigPath + "/" + str(guildID) + ".json"

    if not path.isfile(guildFile):
        generate_new_guild_filter(guildID)
    with open(guildFile, "r") as file:
        commandFilters = json.load(file)

    if command in commandFilters.keys():
        return commandFilters[command]
    else:
        return None


def update_command_filter(command, argument, guildID):
    guildFile = guildConfigPath + "/" + str(guildID) + ".json"

    if not path.isfile(guildFile):
        generate_new_guild_filter(guildID)
    with open(guildFile, "r") as file:
        commandFilters = json.load(file)

    if command in commandFilters.keys():
        commandFilters[command].append(argument)
    else:
        commandFilters[command] = [argument]

    with open(guildFile, "w") as file:
        _ = file.write(json.dumps(commandFilters, sort_keys=True))

    return True