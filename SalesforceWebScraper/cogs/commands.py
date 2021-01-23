import json

import discord
from discord.ext import commands


class Commands(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title=":gear: Help Menu",
                              colour=0xffc325)
        embed.description = "**`!setup <channel:optional>`** - Assign the channel where the messages will be sent to."
        await ctx.send(embed=embed)

    @commands.command()
    async def setup(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            channel = ctx.channel

        data = {
            "channel": channel.id
        }

        self.bot.scrape_channel = channel.id
        with open("data.json", "w+") as fp:
            json.dump(data, fp)

        await ctx.send(f":white_check_mark: Scraping channel successfully assigned to {channel.mention}")


def setup(bot):
    bot.add_cog(Commands(bot))
