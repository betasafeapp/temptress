import discord
from discord.ext import commands
import database
import requests
import asyncio

class MyView(discord.ui.View):
    def __init__(self, pages):
        super().__init__(timeout=10)
        self.pages = pages
        self.page_no = 0

    async def on_timeout(self):
        for child in self.children:
            child.disabled = True
        await self.message.edit(view=self)

    @discord.ui.button(label="Previous", row=0, style=discord.ButtonStyle.primary)
    async def button_callback(self, button, interaction):
        self.page_no = max(0, self.page_no - 1)
        embed = self.pages[self.page_no]
        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Next", row=0, style=discord.ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        self.page_no = min(len(self.pages) - 1, self.page_no + 1)
        embed = self.pages[self.page_no]
        await interaction.response.edit_message(embed=embed, view=self)


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="ping", description="Check the bot's latency")
    async def ping(self, ctx: discord.ApplicationContext):
        await ctx.respond(f"Pong! {round(self.bot.latency * 1000)}ms")

    @discord.slash_command(name="define", description="Define a word")
    async def define(self, ctx: discord.ApplicationContext, word: str):
        if ctx.author.bot:
            return
        ban_data = database.is_botban(ctx.author.id)
        if ban_data is None:
            url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"
            querystring = {"term": word}
            headers = {'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
                       'x-rapidapi-key': "1d70620189msha25958ccae3cdf9p139bc7jsn68c8382e7ede"}
            response = requests.request(
                "GET", url, headers=headers, params=querystring).json()['list']
            if len(response) == 0:
                embed = discord.Embed(description=f'<:cry:968287446217400320>  I can\'t find the definition of the word **`{word}`**',
                                      color=0xFF2030)
                await ctx.respond(embed=embed)
            else:
                pages = []
                for i in range(0, len(response), 1):
                    embed = discord.Embed(description=f"{response[i]['definition']}\n\nExample:\n> {response[i]['example']}\n\nVotes:\n> :arrow_double_up: {response[i]['thumbs_up']}  :arrow_double_down:  {response[i]['thumbs_down']}",
                                          color=0xF2A2C0)
                    embed.set_footer(
                        text=f"{i + 1}/{len(response)}", icon_url=self.bot.user.avatar)
                    embed.set_author(name=word.upper(),
                                     url=response[i]['permalink'])
                    pages.append(embed)

                view = MyView(pages)
                await ctx.respond(embed=pages[0], view=view)

        else:
            embed = discord.Embed(description=f"{ctx.author.mention} you are banned from using {self.bot.user.mention} till {ban_data[1]}",
                                  color=0xF2A2C0)
            await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))
