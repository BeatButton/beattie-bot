from asyncjisho import Jisho
import discord
from discord.ext import commands


class Japanese:
    search_url = 'http://jisho.org/search/{}'

    def __init__(self, bot):
        self.bot = bot
        self.jisho = Jisho()

    @commands.command()
    async def lookup(self, ctx, *, keyword):
        """Get results from Jisho.org, Japanese dictionary"""
        data = await self.jisho.lookup(keyword)
        if not data:
            await ctx.send('No words found.')
            return
        res = data[0]
        res = {k: '\n'.join(v) for k, v in res.items()}
        embed = discord.Embed()
        embed.url = self.search_url.format(keyword)
        embed.title = keyword
        res = {k: self.format(v) for k, v in res.items()}
        embed.add_field(name='Words', value=res['words'])
        embed.add_field(name='Readings', value=res['readings'])
        embed.add_field(name='Parts of Speech', value=res['parts_of_speech'])
        embed.add_field(name='Meanings', value=res['english'])
        await ctx.send(embed=embed)

    @staticmethod
    def format(val):
        return val if val else 'None'


def setup(bot):
    bot.add_cog(Japanese(bot))