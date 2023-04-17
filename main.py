#!/bin/python3
import discord
import os
from dotenv import load_dotenv
import database
from discord.ext import commands

bot = discord.Bot(intents=discord.Intents.all(),
                  debug_guilds=[1088524772746465300])
load_dotenv()

# Getting discord bot token from environment variable
TOKEN = os.getenv('TOKEN')

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="with your mind."))
    print("Temptress is ready and online...")

@bot.event
async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.respond("This command is currently on cooldown!")
    else:
        raise error


if __name__ == '__main__':
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            bot.load_extension(f"cogs.{filename[:-3]}")

    bot.run(TOKEN)
