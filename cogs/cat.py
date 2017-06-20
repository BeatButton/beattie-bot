import re

import aiohttp
import discord
from discord.ext import commands
from lxml import etree
import yaml


class Cat:
    def __init__(self):
        with open('config/config.yaml') as file:
            data = yaml.load(file)
        self.key = data.get('cat_key', '')
        self.url = 'http://thecatapi.com/api/images/get'
        self.params = {'api_key': self.key,
                       'type': 'png,jpg',
                       'format': 'xml',
                       }

    @commands.command()
    async def cat(self, ctx):
        """Gets a picture of a random cat from thecatapi.com!"""
        async with ctx.typing():
            async with ctx.bot.get(self.url, params=self.params) as resp:
                root = etree.fromstring(await resp.text())
            url = root.find('.//url').text
            if not url.startswith('http://'):
                url = f'http://{url}'
            pattern = r'http://\d+\.media\.tumblr\.com'
            replace = 'http://media.tumblr.com'
            url = re.sub(pattern, replace, url)
            ctx.bot.logger.debug(f'Cat URL: {url}')
        await ctx.send(url)

    @cat.error
    async def cat_error(self, ctx, e):
        e = getattr(e, 'original', e)
        if isinstance(e, aiohttp.ServerDisconnectedError):
            await ctx.invoke(self.cat)
        else:
            raise e

    @commands.command()
    async def dog(self, ctx):
        """Gets a picture of a random dog from random.dog!"""
        async with ctx.typing():
            async with ctx.bot.get('http://random.dog/woof') as resp:
                url = 'http://random.dog/{}'.format(await resp.text())
            async with ctx.bot.get(url) as resp:
                file = await resp.read()
            await ctx.send(file=discord.File(file, url.rpartition('/')[-1]))


def setup(bot):
    bot.add_cog(Cat())
