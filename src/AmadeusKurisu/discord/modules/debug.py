from discord.ext import commands
from modules.rolesSQL import *


class debug(commands.Cog):
    def __init__(self, client):
        self.client = client
        global modName
        modName = self.__class__.__name__

    @commands.command(pass_context=True)
    async def migrate(self, ctx, userID, gameName, roomID):
        if await isAuthorized(ctx, "rmgame") < 1: await ctx.send("No. Literally No.")

        setUserGame(ctx.guild, int(userID), gameName, int(roomID))
        await ctx.send("Mapping added", delete_after=2)

    @commands.command(pass_context=True)
    async def sql(self, ctx, *command):
        if await isAuthorized(ctx, "rmgame") != 2: await ctx.send("No. Literally No.")
        command = " ".join(command)

        result = runSQL(ctx.guild, command)

        await ctx.send(result, delete_after=10)

    @commands.command(pass_context=True)
    async def test(self, ctx, *input):
        result = (await isAuthorized(ctx))
        print(result)
        print(type(result))

    @commands.command(pass_context=True)
    async def nullpo(self, ctx):
        await ctx.send("Gah!")


def setup(client):
    client.add_cog(debug(client))