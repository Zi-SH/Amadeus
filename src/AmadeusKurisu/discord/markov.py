import random
from discord.ext import commands
from os import listdir


class markov(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.command(pass_context=True)
    async def log(self, context):
        """!log Are you still drunk Kuri? -> times are bad :picardy:
        Generates a random message based based off logs in 602 files (~100 KB each) using Markov chaining."""

        await self.markovGenerator(context)


    async def markovGenerator(self,context):
        markovFiles = "./AmadeusKurisu/discord/modules/markov/"
        markovFileCount = len(listdir(markovFiles))
        result = ""

        randomInt = random.randint(1, markovFileCount)
