from discord.ext import commands


class Default:
    @commands.command(aliases=['p'])
    async def ping(self, ctx):
        """Get the ping to the websocket."""
        await ctx.send(f'Pong! :ping_pong: **{ctx.bot.latency*1000:.0f}ms**')

    @commands.command()
    async def source(self, ctx):
        """Get the source for the bot."""
        await ctx.send('https://github.com/BeatButton/beattie')

    @commands.command()
    async def invite(self, ctx):
        """Get the invite for the bot."""
        url = 'https://discordapp.com/oauth2/authorize?client_id={}&scope=bot'
        await ctx.send(url.format(ctx.me.id))

    @commands.command(hidden=True, aliases=['thank', 'thx'])
    async def thanks(self, ctx):
        await ctx.send('no u')

    @commands.command(hidden=True)
    async def confetti(self, ctx, num: int=1):
        if num > 200:
            await ctx.send("I don't have that much confetti "
                           '<:blobpensive:337436989676716033>')
        else:
            await ctx.send('🎉' * num)


def setup(bot):
    bot.add_cog(Default())
