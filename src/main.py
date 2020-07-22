import json, sys, os, logging
from discord.ext import commands
from AmadeusKurisu import config, filter
from AmadeusKurisu.discord.modules import utils

# Amadeus System 0.01

######################################################################################################
###                                                                                                ###
###    AAAAAA     MMM        MMM     AAAAAA     DDDDDD       EEEEEEEE   UUU      UUU     SSSSSS    ###
###   AAA  AAA    MMMMMM  MMMMMM    AAA  AAA    DDD  DDD     EEE        UUU      UUU   SSS    SSS  ###
###  AAA    AAA   MMM MMMMMM MMM   AAA    AAA   DDD    DDD   EEE        UUU      UUU   SSS         ###
###  AAAAAAAAAA   MMM  MMMM  MMM   AAAAAAAAAA   DDD    DDD   EEEEEEEE   UUU      UUU     SSSSSS    ###
###  AAA    AAA   MMM        MMM   AAA    AAA   DDD    DDD   EEE        UUU      UUU          SSS  ###
###  AAA    AAA   MMM        MMM   AAA    AAA   DDD   DDD    EEE         UUU    UUU    SSS    SSS  ###
###  AAA    AAA   MMM        MMM   AAA    AAA   DDDDDDD      EEEEEEEE      UUUUUU        SSSSSSS   ###
###                                                                                                ###
######################################################################################################

# Initialize bot client
client = commands.Bot(
    command_prefix=config.PREFIX,
    description=config.DESCRIPTION,
    case_insensitive=True)

## Clear help command
client.remove_command("help")

## Constant variables
loadedModules = []

## Command Functions
@client.command(pass_context=True)
async def load(context, module):
    await utils.load_module(client, module, context)

@client.command(pass_context=True)
async def unload(context, module):
    await utils.unload_module(client, module, context)

@client.command(pass_context=True)
async def reload(context, module):
    await utils.load_module(client, module, context)
    await utils.unload_module(client, module, context)

@client.command(pass_context=True)
async def listmods(context):
    # TODO: Fancy embed
    await utils.send_message(context, utils.get_modules())

## Message functions
@client.event
async def on_message(message):
    if not message.author.bot:
        await client.process_commands(message)

@client.event
async def on_command_error(context,error):
    if not isinstance(error, commands.errors.MissingRequiredArgument):
        logging.error(error)

@client.event
async def on_ready():
    logging.info(f"{client.user.name} has connected successfully")
    logging.info("------")

    modules = utils.get_modules()
    modulePath = utils.get_module_path()

    for module in modules:
        if await utils.load_module(client, module):
            loadedModules.append(module)
    try:
        await utils.load_module(client, modulePath + ".help")
        loadedModules.append(modulePath + ".help")
    except (AttributeError, ImportError) as e:
        logging.critical("Help module failed to load.")
        sys.exit("Fatal Error: Unable to load help module.")

    logging.info("------")

client.run(config.TOKEN)






