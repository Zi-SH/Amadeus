import json
from os import mkdir, path
from discord.ext import commands
from discord import utils

class gateway(commands.Cog):
    def __init__(self, client):
        self.client = client

    """This module is for modifying the server vestibule; a room which separates the outside from the rest of the server"""

    configPath = "./AmadeusKurisu/discord/modules/gateway"
    messageID = None

    async def create_config(self, context, configPath):
        if not path.isdir(configPath):
            mkdir(configPath)
        if not path.isfile(configPath + "/" + str(context.guild.id) + ".json"):
            with open(str(context.guild.id) + ".json", "w") as file:
                _ = file.write(json.dumps({}))

    async def get_config(self, context, configPath):
        # TODO: retrieve vestibule channel, emotes, and roles
        ## Layout should be something like this:
        ## {"channel" = id,
        ##  "message" = id,
        ##  "emoteName" = [emoteID, roleName]
        ## }
        pass

    async def set_config(self, context, configPath, key, value):
        # TODO: update key and value
        pass

    async def search_messages(self, context):
        async for message in context.channel.history(limit=10):
            if message.author == self.client.user:
                return message.id

        return None


    @commands.command(pass_context=True)
    async def setmessage(self, context):
        content = context.message.content.replace("!setvmessage ", "")

        message = await self.search_messages(context)

        if not message:
            messageID = await context.send(content)
            await context.message.delete()
        else:
            await context.message.delete()
            await context.send("Please delete the previous messages from the bot in this channel prior to setting a vestibule message.", delete_after=10)


    @commands.command(pass_context=True)
    async def setreact(self, context):
        message = await self.search_messages(context)


        if not message:
            await context.send("Please enter a vestibule message before setting reacts.")
        else:
            reactString = context.message.content.split(" ")

            if len(reactString) < 3 or len(reactString) > 3:
                context.send("You must specify a emote and role to set.")
                return

            vesibuleEmote, vestibuleRole = reactString[1], reactString[2]
            vestibuleRole = utils.get(message.guild.roles, name=vestibuleRole)

            if not vestibuleRole:
                await context.send("Role does not exist. Please try again with a valid role.")
            else:
                # TODO: Write vestibule emote and role to config
                # TODO: React to vestibule message with vestibuleEmote
                # TODO: Setup listener for vestibule channel
                # TODO: When user clicks emote on message,
            pass

def setup(client):
    client.add_cog(gateway(client))