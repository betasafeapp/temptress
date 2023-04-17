import discord
import database
import asyncio
import random
import sqlite3
from discord.ext import commands


con = sqlite3.connect(':memory:')
cur = con.cursor()

class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(description='Bet on a coin flip')
    @commands.cooldown(3, 1 * 60, commands.BucketType.user)
    async def coinflip(self, ctx, choice: discord.Option(str, choices=['heads', 'tails']), bet: int):
        if ctx.author.bot:
            return
        ban_data = database.is_botban(ctx.author.id)
        if ban_data is None:
            if bet < 10:
                await ctx.respond(f"You need to bet atleast 10 :coin:")
            else:
                coins = database.get_money(ctx.author.id, ctx.guild.id)[2]
                if bet > coins:
                    await ctx.respond(f"Ur broke ass only has {coins} :coin:")
                    return
                database.remove_money(ctx.author.id, ctx.guild.id, bet, 0)
                await asyncio.sleep(2)
                if bool(random.getrandbits(1)):
                    if choice.lower() in ['heads']:
                        database.add_money(
                            ctx.author.id, ctx.guild.id, 2 * bet, 0)
                        embed = discord.Embed(
                            title='its heads!!', description=f"{ctx.author.mention} won {bet}", color=0x08FF08)
                        await ctx.respond(embed=embed)
                    else:
                        embed = discord.Embed(
                            title='its heads!!', description=f"{ctx.author.mention} lost {bet}", color=0xFF2030)
                        await ctx.respond(embed=embed)

                else:
                    if choice.lower() in ['tails']:
                        database.add_money(
                            ctx.author.id, ctx.guild.id, 2 * bet, 0)
                        embed = discord.Embed(
                            title='its tails!!', description=f"{ctx.author.mention} won {bet}", color=0x08FF08)
                        await ctx.respond(embed=embed)
                    else:
                        embed = discord.Embed(
                            title='its tails!!', description=f"{ctx.author.mention} lost {bet}", color=0xFF2030)
                        await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title='Bot ban',
                                  description=f"{ctx.author.mention} you are banned from using {self.bot.user.mention} till <t:{ban_data[1]}:F>",
                                  color=0xF2A2C0)
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Gambling(bot))
