from discord.ext import commands

class debug(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def nullpo(self, ctx):
        await ctx.send("Gah!")

def setup(client):
    client.add_cog(debug(client))