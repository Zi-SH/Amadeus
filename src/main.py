import json, sys, os, logging
from discord.ext import commands
from AmadeusKurisu import config
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
    command_prefix=config.bot["prefix"],
    description=config.bot["desc"],
    case_insensitive=True)

## Clear help command
client.remove_command("help")

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
    utils.send_message(context, utils.get_modules())




