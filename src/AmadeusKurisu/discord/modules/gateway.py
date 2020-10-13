import json
from os import mkdir, listdir, path, getcwd
from discord.ext import commands
from discord import utils, NotFound, Forbidden

class gateway(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.configPath = "./AmadeusKurisu/discord/modules/gateway"
        ### Our Mapping looks something like this:
        ### {'guildID1': {'messageID1' : {'emoteID1' : 'roleID1', 'emoteID2' : 'roleID2'}}, 'guildID2': {'messageID2' : {'emoteID3' : 'roleID3', 'emoteID4' : 'roleID4'}}}
        self.mappings = {}

        ## Due to JSON limitations, all guild ID references are in string.
        # TODO: Convert all the guild ID references to string

        guildList = listdir(self.configPath)
        for config in guildList:
            guildID = config.split(".")[0]
            filePath = self.configPath + "/" + config
            with open(filePath, "r") as config:
                config = json.loads(config.read())
            self.mappings.update({int(guildID) : config})

    async def verify_config(self, guildid):
        filePath = self.configPath + "/" + str(guildid) + ".json"
        if not path.isfile(filePath):
            if not path.isdir(self.configPath):
                mkdir(self.configPath)
            with open(self.configPath + "/" + str(guildid) + ".json", "w") as config:
                _ = config.write(json.dumps({}))
            self.mappings.update({guildid : {}})
        return True

    # TODO: Change to "write_cache" to update guilds as they are modified
    async def read_config(self, guildid):
        filePath = self.configPath + "/" + str(guildid) + ".json"
        await self.verify_config(guildid)

        with open(filePath, "r") as config:
            database = config.read()

        return database

    async def write_cache(self, guildid):
        if (not path.isdir(self.configPath) or
            not path.isfile(self.configPath + "/" + str(guildid) + ".json")):
            await self.verify_config(guildid)

        database = self.mappings[guildid]
        with open(self.configPath + "/" + str(guildid) + ".json", "w") as config:
            _ = config.write(json.dumps(database))

        return True

    async def fetch_message_by_id(self, context, id):
        return await context.channel.fetch_message(id)


    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guildID = payload.guild_id
        messageID = payload.message_id
        memberID = payload.member.id
        emojiID = payload.emoji.id

        if str(messageID) in self.mappings[guildID]:
            if str(emojiID) in self.mappings[guildID][str(messageID)]:
                guildObj = self.client.get_guild(payload.guild_id)
                roleID = int(self.mappings[guildID][str(messageID)][str(emojiID)])
                roleObj = guildObj.get_role(roleID)
                # TODO: MemberOBJ lookup maybe redundant. Payload seems to include member.
                memberObj = guildObj.get_member(memberID)

                if (roleObj is not None) and (memberObj is not None):
                    try:
                        await memberObj.add_roles(roleObj)
                    except Forbidden as error:
                        print(error)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guildID = payload.guild_id
        messageID = payload.message_id
        # The genius writing discord.py saw fit not to include member.id like the on_raw_reaction_add
        memberID = payload.user_id
        emojiID = payload.emoji.id

        if str(messageID) in self.mappings[guildID]:
            if str(emojiID) in self.mappings[guildID][str(messageID)]:
                guildObj = self.client.get_guild(payload.guild_id)
                roleID = int(self.mappings[guildID][str(messageID)][str(emojiID)])
                roleObj = guildObj.get_role(roleID)
                memberObj = guildObj.get_member(memberID)

                if (roleObj is not None) and (memberObj is not None):
                    try:
                        await memberObj.remove_roles(roleObj)
                    except Forbidden as error:
                        print(error)

    @commands.command(pass_context=True)
    async def setmessage(self, context, *content):
        if not await self.verify_config(context.guild.id):
            await context.send("An error has occurred.")
            return

        await context.message.delete()
        content = ' '.join(content)
        message = await context.send(content)

        self.mappings[context.guild.id].update({message.id : {}})
        await self.write_cache(context.guild.id)

    @commands.command(pass_context=True)
    async def setreact(self, context, messageID, reaction, role):
        try:
            # Documentation says user has a fetch_message couroutine. Documentation is lying to you and me.
            # Running a fetch_user on the ClientUser ID results in a 400 Bad Request. Only possible way is channel lookup
            messageObj = await self.fetch_message_by_id(context, messageID)
        except NotFound:
            await context.send("The message with the specified ID not found. Make sure you're copying the 18-digit message ID.")
            return False

        if all(markup in reaction for markup in ["<", ":", ">"]):
            reaction = reaction[2:][:-1].split(":")[0]
        elif len(reaction) != 1:
            await context.send("Please use the emoji or Emoji ID in the command rather than the name of the emoji.")
            return False

        reactionObj = utils.get(context.guild.emojis, name=reaction)
        if reactionObj is None:
            await context.send("The emoji specified was not found on this server. Please try again.")

        roleObj = utils.get(context.guild.roles, name=role)
        if roleObj is None:
            await context.send('The role  "' + role + '" was not found on this server. Please try again.')
            return False

        await messageObj.add_reaction(reactionObj)
        await context.send("Emoji added successfully!", delete_after=10)

        self.mappings[context.guild.id][messageID][str(reactionObj.id)] = str(roleObj.id)
        await self.write_cache(context.guild.id)

def setup(client):
    client.add_cog(gateway(client))