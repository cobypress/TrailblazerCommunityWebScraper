import asyncio
import json
import os

import discord
from arsenic import get_session, browsers, services
from discord.ext import commands, tasks

if os.name == "nt":  # Windows
    DRIVER = f"{os.getcwd()}\\cogs\\chromedriver.exe"
else:  # Other OSes
    DRIVER = "/Users/cobypress/bin/chromedriver"

print(DRIVER)


class Scraper(commands.Cog):
    url = "https://trailblazers.salesforce.com/answers?feedtype=RECENT&criteria=BESTANSWERS#!/feedtype=RECENT&dc=All&criteria=OPENQUESTIONS"

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.browser = browsers.Chrome(**{"goog:chromeOptions": {"args": ["--headless", "--disable-gpu"]}})
        self.service = services.Chromedriver(binary=DRIVER)

    @tasks.loop(seconds=30)
    async def do_scrape(self):
        print("should be doing something")
        async with get_session(service=self.service, browser=self.browser) as s:
            print("a")
            await s.get(Scraper.url)

            accept = await s.wait_for_element(1, selector="button[id='onetrust-accept-btn-handler']")
            await accept.click()
            await asyncio.sleep(1)  # Wait for the transparency overlay to disappear

            question_container = await s.wait_for_element(10, selector="div[class='csfeedcontainer cxRecentFeed cxOpenQuestionsFeed']")
            questions = await question_container.get_elements(selector="div[data-scc]")

            screenshots = []
            ids = []

            for q in questions:
                id_element = await q.get_elements(selector="a[class='cxsingleitemdetailfeed']")
                for i in id_element:
                    _id = await i.get_attribute(name="href")
                if _id not in self.bot.recent_responses:
                    ids.append(_id)
                    screenshots.append(await q.get_screenshot())
                    if len(ids) == 11:
                        ids.pop(0)
                else:
                    break

            if len(ids) > 0:
                self.bot.recent_responses = ids

            if self.bot.scrape_channel is None:
                try:
                    with open("data.json", "r") as fp:
                        data = json.load(fp)
                except FileNotFoundError:
                    pass

                self.bot.scrape_channel = data["channel"]

            if self.bot.first_scrape:
                self.bot.first_scrape = False

                return

            channel = self.bot.get_channel(self.bot.scrape_channel)
            if len(ids) > 0:
                await channel.send(f":loudspeaker: {len(ids)} NEW UPDATE{'S' if len(ids) > 1 else ''}! :loudspeaker:")

                for i, ss in zip(ids, screenshots):
                    f = open("screenshot.jpg", "wb")
                    f.write(ss.read())
                    f.close()
                    embed = discord.Embed(title="Link", url=i)
                    embed.set_image(url="attachment://screenshot.jpg")
                    embed.colour = 0xffc325
                    await channel.send(embed=embed, file=discord.File("screenshot.jpg"))
                    await asyncio.sleep(1)

    @commands.Cog.listener()
    async def on_ready(self):
        print(dir(self.do_scrape))
        self.do_scrape.start()


def setup(bot):
    bot.add_cog(Scraper(bot))
