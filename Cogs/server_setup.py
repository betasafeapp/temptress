import discord
from discord.ext import commands
import database
import asyncio
import re


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


class Setup(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    set = discord.SlashCommandGroup("set", "Set related commands")
    blacklist = discord.SlashCommandGroup(
        "blacklist", "Blacklist related commands")

    def list_roles(self, roles):
        if isinstance(roles, list):
            role = '>'
            for r in roles:
                role = f"{role} <@&{r}>\n>"
            return role[:-2]
        else:
            return roles

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        kuro_usagi = self.bot.get_user(104373103802466304)
        owner_invite_embed = discord.Embed(title=f"Hi {guild.owner.name},",
                                           description=f"I have been invited to your server **{guild.name}**"
                                           "\nI am a fun bot made for Femdom Communities to help Dommes to play with their subs and also punish them."
                                           "\n\n**My prefix is `/`**\n> **`/setup`** use this command to set me up in the server"
                                           "\n> **`/help`** use this command to know me more.",
                                           color=0xF2A2C0)
        owner_invite_embed.set_thumbnail(url=self.bot.user.avatar_url)
        owner_invite_embed.set_footer(text=f'created by {kuro_usagi}')
        await guild.owner.send(embed=owner_invite_embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        database.remove_guild(guild.id)

    @discord.slash_command(description="Setup the bot")
    @commands.has_permissions(administrator=True)
    async def setup(self, interaction: discord.Interaction):
        def check(res):
            return interaction.author == res.author and res.channel == interaction.channel

        setup_embed_domme = discord.Embed(title='Setting Me Up.. (1/4)',
                                          description=f"Mention Domme role/s in the server, \nI will consider members with those roles as Domme.\n> "
                                          "*I will wait 1 minute for you to mention the Domme role/s.*",
                                          color=0xBF99A0)
        setup_embed_domme.set_thumbnail(url=self.bot.user.avatar)

        setup_embed_slave = discord.Embed(title='Setting Me Up.. (2/4)',
                                          description=f"Mention Sub role/s in the server,\nI will consider members with those roles as Subs.\n> "
                                          "*I will wait 1 minute for you to mention the Sub role/s.*",
                                          color=0x591B32)
        setup_embed_slave.set_thumbnail(url=self.bot.user.avatar)

        setup_embed_prison = discord.Embed(title='Setting Me Up.. (4/4)',
                                           description=f"Mention a channel to lock Subs for punishments.\n> "
                                           "*I will wait 1 minute for you to mention a channel,*\n> *or type anything so I will make a new prison channel.*",
                                           color=0xF2A2C0)
        setup_embed_prison.set_thumbnail(url=self.bot.user.avatar)

        setup_embed_locker = discord.Embed(title='Setting Me Up.. (3/4)',
                                           description=f"Mention the lock roles, so only Members with that role can lock Subs in prison."
                                           f"\n> *I will wait 1 minute for you to mention the Role/s*",
                                           color=0x591B32)

        setup_embed_fail = discord.Embed(title='Failed',
                                         description=f"**I was not able to find a valid role mentioned in this message**\n"
                                         f"you can always retry the setup again **`t.setup`**",
                                         color=0xFF2030)

        setup_embed_fail.set_thumbnail(url=self.bot.user.avatar)

        setup_embed_timeout = discord.Embed(title='Times Up',
                                            description=f"I can't wait for long, I have limited bandwidth\nits ok you can always try it again type **`t.setup`**",
                                            color=0xFF2030)

        setup_embed_timeout.set_thumbnail(url=self.bot.user.avatar)

        await interaction.response.send_message(embed=setup_embed_domme)

        try:
            response = await self.bot.wait_for('message', timeout=90, check=check)
            domme_roles = "".join(
                [role[3:-1] for role in re.findall(r'<@&\d*>', response.content)])
            if domme_roles == '':
                await response.reply(embed=setup_embed_fail)
                return
            database.insert_config('domme', interaction.guild.id, domme_roles)
            await response.delete()
            await interaction.followup.send(embed=setup_embed_slave)

            try:
                response = await self.bot.wait_for('message', timeout=90, check=check)
                slave_roles = [role[3:-1]
                               for role in re.findall(r'<@&\d*>', response.content)]
                for x in slave_roles:
                    if x in domme_roles:
                        slave_roles.pop(x)
                slave_roles = "".join(slave_roles)

                if slave_roles == '':
                    await response.reply(embed=setup_embed_fail)
                    return
                database.insert_config(
                    'slave', interaction.guild.id, slave_roles)
                await response.delete()
                await interaction.followup.send(embed=setup_embed_locker)

                try:
                    response = await self.bot.wait_for('message', timeout=90, check=check)
                    locker_roles = [role[3:-1]
                                    for role in re.findall(r'<@&\d*>', response.content)]
                    for x in locker_roles:
                        if x in slave_roles:
                            locker_roles.pop(x)
                    locker_roles = ''.join(locker_roles)

                    if locker_roles == '':
                        await response.reply(embed=setup_embed_fail)
                        return
                    database.insert_config(
                        'locker', interaction.guild.id, locker_roles)
                    await response.delete()
                    await interaction.followup.send(embed=setup_embed_prison)

                    try:
                        response = await self.bot.wait_for('message', timeout=90, check=check)
                        try:
                            prison = [
                                role[2:-1] for role in re.findall(r'<#\d*>', response.content)][0]
                            database.insert_config(
                                'prison', interaction.guild.id, prison)
                            await response.delete()

                            d_roles = ''
                            s_roles = ''
                            l_roles = ''
                            for r in range(int(len(domme_roles) / 18)):
                                d_roles = f"{d_roles}\n> <@&{domme_roles[r * 18:(r * 18) + 18]}>"

                            for r in range(int(len(slave_roles) / 18)):
                                s_roles = f"{s_roles}\n> <@&{slave_roles[r * 18:(r * 18) + 18]}>"

                            for r in range(int(len(locker_roles) / 18)):
                                l_roles = f"{l_roles}\n> <@&{locker_roles[r * 18:(r * 18) + 18]}>"

                            setup_embed_summary = discord.Embed(title='Completed',
                                                                description=f"Dommes in the server are the members with the following roles{d_roles}"
                                                                f"\nSubs in the server are the members with the following roles{s_roles}"
                                                                f"\nMembers with following roles can lock sub in <#{prison}> {l_roles}"
                                                                f"\nThe channel where Dommes can torture and punish subs.\n> <#{prison}>"
                                                                f"\n\n**Use the command `/help` to know more about me.**",
                                                                color=0x08FF08)
                            setup_embed_summary.set_thumbnail(
                                url=self.bot.user.avatar)
                            await interaction.followup.send(embed=setup_embed_summary)
                        except IndexError:
                            prison = database.get_config(
                                'prison', interaction.guild.id)
                            if prison == [0] or interaction.guild.get_channel(int(prison[0])) is None:
                                prison = await interaction.guild.create_text_channel('Prison')
                                database.insert_config(
                                    'prison', interaction.guild.id, prison.id)
                                prison = prison.id
                            else:
                                prison = int(prison[0])
                            d_roles = ''
                            s_roles = ''
                            for r in range(int(len(domme_roles) / 18)):
                                d_roles = f"{d_roles}\n> <@&{domme_roles[r * 18:(r * 18) + 18]}>"

                            for r in range(int(len(slave_roles) / 18)):
                                s_roles = f"{s_roles}\n> <@&{slave_roles[r * 18:(r * 18) + 18]}>"

                            for r in range(int(len(locker_roles) / 18)):
                                l_roles = f"{l_roles}\n> <@&{locker_roles[r * 18:(r * 18) + 18]}>"

                            setup_embed_summary = discord.Embed(title='Completed',
                                                                description=f"Dommes in the server are the members with the following roles{d_roles}"
                                                                f"\nSubs in the server are the members with the following roles{s_roles}"
                                                                f"\nMembers with following roles can lock sub in <#{prison}> {l_roles}"
                                                                f"\nThe channel where Dommes can torture and punish subs.\n> <#{prison}>"
                                                                f"\n\n**Use the command `t.help` to know more about me.**",
                                                                color=0x08FF08)
                            setup_embed_summary.set_thumbnail(
                                url=self.bot.user.avatar_url)
                            await interaction.followup.send(embed=setup_embed_summary)

                    except asyncio.TimeoutError:
                        await interaction.followup.send(embed=setup_embed_timeout)

                except asyncio.TimeoutError:
                    await interaction.followup.send(embed=setup_embed_timeout)

            except asyncio.TimeoutError:
                await interaction.followup.send(embed=setup_embed_timeout)

        except asyncio.TimeoutError:
            await interaction.followup.send(embed=setup_embed_timeout)

        prisoner = database.get_config('prisoner', interaction.guild.id)
        if prisoner == [0] or interaction.guild.get_role(int(prisoner[0])) is None:
            prisoner = await interaction.guild.create_role(name='Prisoner', color=0x591B32)
            database.insert_config(
                'prisoner', interaction.guild.id, prisoner.id)
        else:
            prisoner = interaction.guild.get_role(prisoner[0])
        prison = interaction.guild.get_channel(int(prison))
        channels = await interaction.guild.fetch_channels()
        for channel in channels:
            await channel.set_permissions(prisoner, view_channel=False, send_messages=False)
        await prison.set_permissions(prisoner, view_channel=True, send_messages=True)
        await prison.set_permissions(interaction.guild.default_role, view_channel=True, send_messages=False)

        for r in range(int(len(domme_roles) / 18)):
            d_role = int((domme_roles[r * 18:(r * 18) + 18]))
            await prison.set_permissions(interaction.guild.get_role(d_role), view_channel=True, send_messages=True)

    @discord.slash_command(description="Stats of the bot")
    async def stat(self, ctx):
        prison = database.get_config('prison', ctx.guild.id)
        domme = database.get_config('domme', ctx.guild.id)
        slave = database.get_config('slave', ctx.guild.id)
        NSFW = database.get_config('NSFW', ctx.guild.id)
        chat = database.get_config('chat', ctx.guild.id)
        locker = database.get_config('locker', ctx.guild.id)
        t_mem = 0

        for guild in self.bot.guilds:
            t_mem = t_mem + guild.member_count

        if NSFW == [0]:
            NSFW = f"> {ctx.guild.default_role}"
        if chat == [0]:
            chat = f"> {ctx.guild.default_role}"

        if domme != [0]:
            stat_embed = discord.Embed(title='Status',
                                       description=f"**I am controling {t_mem} members.**\n\n"
                                       f"Domme roles:\n{self.list_roles(domme)}\n"
                                       f"Sub roles:\n{self.list_roles(slave)}\n"
                                       f"Dommes who are strong to lock subs in <#{prison[0]}>:\n{self.list_roles(locker)}\n"
                                       f"NSFW command access is given to:\n{self.list_roles(NSFW)}\n"
                                       f"Members who have permission to talk to me:\n{self.list_roles(chat)}\n\n"
                                       f"**Dommes can torture subs in <#{prison[0]}>**\n"
                                       f"\n> type **`t.help`** to know more about me",
                                       color=0xF2A2C0)
        else:
            stat_embed = discord.Embed(title='Status',
                                       description=f"**I am active in {len(self.bot.guilds)} servers.**\n"
                                       f"\n> type **`t.setup`** to set me up in the server"
                                       f"\n> type **`t.help`** to know more about me",
                                       color=0xF2A2C0)
        stat_embed.set_thumbnail(url=self.bot.user.avatar)
        await ctx.respond(embed=stat_embed)

    @blacklist.command(description="Blacklist a member")
    @commands.has_permissions(administrator=True)
    async def list(self, ctx: commands.Context):
        page_number = 1
        size = 10
        data = database.get_blacklist(ctx.guild.id)

        if len(data) == 0:
            await ctx.respond("There are no blacklisted members in this server")
            return

        pages = []
        for page in range(1, int(len(data) / size) + (len(data) % size > 0) + 1):
            embed = self.page(data, page, size, ctx.guild.icon)
            pages.append(embed)

        view = MyView(pages)
        view.message = await ctx.respond(embed=pages[0], view=view)

    def page(self, lb_list, page, size, guild_icon):
        start = (page - 1) * size
        end = start + size
        page_list = lb_list[start:end]

        value = ""
        for user_id in page_list:
            value += f"> <@{user_id}>\n"

        embed = discord.Embed(
            title="Blacklisted Members",
            description=value,
            color=0xF2A2C0
        )

        embed.set_footer(
            text=f"On page {page}/{int(len(lb_list) / size) + (len(lb_list) % size > 0) + 1}"
        )
        embed.set_thumbnail(url=guild_icon)
        return embed

    @blacklist.command(description="Blacklist a member")
    @commands.has_permissions(administrator=True)
    async def toggle(self, ctx: commands.Context, member: discord.Member):
        if database.insert_remove_blacklist(member.id, ctx.guild.id):
            embed = discord.Embed(title='Added into Blacklist',
                                  description=f"{member.mention} is Blacklisted, now the member can't lock anyone in the server anymore.", color=0xFF2030)
            embed.set_thumbnail(url=member.avatar)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title='Removed from Blacklist',
                                  description=f"{member.mention} is no longer Blacklisted, and can lock the subs <#{database.get_config('prison', ctx.guild.id)[0]}>", color=0x08FF08)
            embed.set_thumbnail(url=member.avatar)
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Setup(bot))
