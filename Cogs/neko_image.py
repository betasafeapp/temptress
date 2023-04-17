import discord
from discord.ext import commands
import nekos


class Neko_image(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="hug", description="Hug someone!")
    async def hug(self, ctx, user: discord.User):
        await ctx.defer()
        hug_image_url = nekos.img('hug')

        embed = discord.Embed(
            title=f"{ctx.author.nick or ctx.author.name} hugs {user.nick or user.name}", color=discord.Color.blurple())
        embed.set_image(url=hug_image_url)

        await ctx.respond(embed=embed)
        if user.id == self.bot.user.id:
            image_url = nekos.img('hug')
            embed = discord.Embed(
                title=f"Temptress hugs {ctx.author.nick or ctx.author.name} back.", color=0xF2A2C0)
            embed.set_image(url=image_url)
            await ctx.respond(embed=embed)

    @commands.slash_command(name="slap", description="Slap someone!")
    async def slap(self, ctx, user: discord.User):
        await ctx.defer()
        slap_image_url = nekos.img('slap')

        embed = discord.Embed(
            title=f"{ctx.author.nick or ctx.author.name} slaps {user.nick or user.name}", color=discord.Color.blurple())
        embed.set_image(url=slap_image_url)

        await ctx.respond(embed=embed)
        if user.id == self.bot.user.id:
            image_url = nekos.img('slap')
            embed = discord.Embed(
                title=f"Temptress slaps {ctx.author.nick or ctx.author.name} back.", color=0xF2A2C0)
            embed.set_image(url=image_url)
            await ctx.respond(embed=embed)

    @commands.slash_command(name="tickle", description="Tickle someone!")
    async def tickle(self, ctx, user: discord.User):
        await ctx.defer()
        tickle_image_url = nekos.img('tickle')

        embed = discord.Embed(
            title=f"{ctx.author.nick or ctx.author.name} tickles {user.nick or user.name}", color=discord.Color.blurple())
        embed.set_image(url=tickle_image_url)

        await ctx.respond(embed=embed)
        if user.id == self.bot.user.id:
            image_url = nekos.img('tickle')
            embed = discord.Embed(
                title=f"Temptress tickles {ctx.author.nick or ctx.author.name} back.", color=0xF2A2C0)
            embed.set_image(url=image_url)
            await ctx.respond(embed=embed)

    @commands.slash_command(name="pat", description="Pat someone!")
    async def pat(self, ctx, user: discord.User):
        await ctx.defer()
        pat_image_url = nekos.img('pat')

        embed = discord.Embed(
            title=f"{ctx.author.nick or ctx.author.name} pats {user.nick or user.name}", color=discord.Color.blurple())
        embed.set_image(url=pat_image_url)

        await ctx.respond(embed=embed)
        if user.id == self.bot.user.id:
            image_url = nekos.img('pat')
            embed = discord.Embed(
                title=f"Temptress pats {ctx.author.nick or ctx.author.name} back.", color=0xF2A2C0)
            embed.set_image(url=image_url)
            await ctx.respond(embed=embed)

    @commands.slash_command(name="poke", description="Poke someone!")
    async def poke(self, ctx, user: discord.User):
        await ctx.defer()
        poke_image_url = nekos.img('poke')

        embed = discord.Embed(
            title=f"{ctx.author.nick or ctx.author.name} pokes {user.nick or user.name}", color=discord.Color.blurple())
        embed.set_image(url=poke_image_url)

        await ctx.respond(embed=embed)
        if user.id == self.bot.user.id:
            image_url = nekos.img('poke')
            embed = discord.Embed(
                title=f"Temptress pokes {ctx.author.nick or ctx.author.name} back.", color=0xF2A2C0)
            embed.set_image(url=image_url)
            await ctx.respond(embed=embed)

    @commands.slash_command(name="kiss", description="Kiss someone!")
    async def kiss(self, ctx, user: discord.User):
        await ctx.defer()
        kiss_image_url = nekos.img('kiss')

        embed = discord.Embed(
            title=f"{ctx.author.nick or ctx.author.name} kisses {user.nick or user.name}", color=discord.Color.blurple())
        embed.set_image(url=kiss_image_url)

        await ctx.respond(embed=embed)
        if user.id == self.bot.user.id:
            image_url = nekos.img('kiss')
            embed = discord.Embed(
                title=f"Temptress kisses {ctx.author.nick or ctx.author.name} back.", color=0xF2A2C0)
            embed.set_image(url=image_url)
            await ctx.respond(embed=embed)

    @commands.slash_command(name="cuddle", description="Cuddle someone!")
    async def cuddle(self, ctx, user: discord.User):
        await ctx.defer()
        cuddle_image_url = nekos.img('cuddle')

        embed = discord.Embed(
            title=f"{ctx.author.nick or ctx.author.name} cuddles {user.nick or user.name}", color=discord.Color.blurple())
        embed.set_image(url=cuddle_image_url)

        await ctx.respond(embed=embed)
        if user.id == self.bot.user.id:
            image_url = nekos.img('cuddle')
            embed = discord.Embed(
                title=f"Temptress cuddles {ctx.author.nick or ctx.author.name} back.", color=0xF2A2C0)
            embed.set_image(url=image_url)
            await ctx.respond(embed=embed)

    @commands.slash_command(name="spank", description="Spank someone!")
    async def spank(self, ctx, user: discord.User):
        await ctx.defer()
        spank_image_url = nekos.img('spank')

        embed = discord.Embed(
            title=f"{ctx.author.nick or ctx.author.name} spanks {user.nick or user.name}", color=discord.Color.blurple())
        embed.set_image(url=spank_image_url)

        await ctx.respond(embed=embed)
        if user.id == self.bot.user.id:
            image_url = nekos.img('spank')
            embed = discord.Embed(
                title=f"Temptress spanks {ctx.author.nick or ctx.author.name} back.", color=0xF2A2C0)
            embed.set_image(url=image_url)
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Neko_image(bot))
