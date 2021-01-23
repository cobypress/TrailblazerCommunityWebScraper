import traceback
from datetime import datetime

import discord
from discord.ext import commands


intents = discord.Intents().all()


def get_prefix(b, message):

    return commands.when_mentioned_or("!")(b, message)


bot = commands.Bot(command_prefix=get_prefix, intents=intents, case_insensitive=True)
bot.remove_command("help")
bot.recent_responses = []
bot.first_scrape = True
bot.scrape_channel = None

cogs = [
    "cogs.commands",
    "cogs.scraper"
]

bot.uptime = datetime.utcnow()

bot.giveaways = []

if __name__ == "__main__":
    for i, cog in enumerate(cogs, start=1):
        try:
            bot.load_extension(cog)
            print(f"{i}/{len(cogs)}: {cog.split('.')[1].title()}.py successfully loaded!")
        except Exception as e:
            print(e)
            traceback.print_exc()


try:
    t = "ODAyMjYxODAwNjAyMzA0NTIy.YAsqhg.CiECkZWrsVDgUOi7HX33FxDD7fI"
    bot.run(t)
except Exception as e:
    print(e)
finally:
    traceback.print_exc()
