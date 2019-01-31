import asyncio
import argparse
import feedparser
import discord
import sys
import re
import os
from loguru import logger
import random
import datetime
import textwrap
from tinydb import TinyDB, Query
from helpers import quotes, date_to_imperial_date

try:
    from config import CONFIG
except ModuleNotFoundError:
    print("Could not find config.py")
    sys.exit(1)

db = TinyDB(CONFIG["db_path"])
client = None


async def say_date(channel):
    """ Says the current imperial date """
    date = date_to_imperial_date(datetime.datetime.now())
    quote = random.choice(
        (
            "ERROR INTRODUCED BY I̝͆ͮͅMͣ̍̽MA̳͚̦ͫ̆͒T̳͕̻͑̿ͨER͖̝̙ͧ̃ͨI̗̟U̹̓M̹̤̝̉̈̊ IS WITHIN SPECIFICATIONS",
            "A GOOD TIME TO DIE?",
            "LIKE ALL IT IS BLESSED BY THE GOLDEN THRONE",
            "WHEN DOES IT END?",
            "TIME IS SLIPPING AWAY",
        )
    )
    await client.send_message(
        channel, f"+++ THE CURRENT DATE IS `{date}` +++ {quote} +++"
    )


async def unknown_command(channel):
    quote = random.choice(
        (
            "My memory banks are too slow.... I do not understand.",
            "What is your desire, most beneficent one?",
            "I can't comply.... Do you consider me useless?",
            "What is he meaning of this?",
            "repeat input, lord",
        )
    )
    await client.send_message(
        channel, "+++ {quote} +++ TRY `!help` +++".format(quote=quote.upper())
    )


async def say_quote(channel):
    message = "+++ {0} +++".format(random.choice(quotes).upper())
    await client.send_message(channel, message)


async def help_message(channel):
    """
        Says a message listing all the available commands.
    """
    message = textwrap.dedent(
        """
            +++ MY SERVICES ARE AT YOUR DISPOSAL +++

            * `!help` for this help message.
            * `!date` for the current imperial date.
            * `!quote` for a random message.

            Go to <https://github.com/NiklasMM/sixgun_discord_bot> for feature requests and bug reports.
        """
    )
    await client.send_message(channel, message)


def episode_is_new(feed_url, episode_url):
    """
        Checks if a given podcast episode is a new episode.
        Episodes are identified via their URL.
        We check in the database if the url to check is the same as the one we have most recently
        seen for this feed, if not, we assume it is a new episode.
        If we have never seen any episode for this feed we assuem it's not new either.
    """
    Entry = Query()
    result = db.search(
        (Entry.feed_url == feed_url) & (Entry.episode_url == episode_url)
    )

    if len(result) == 0:
        db.insert({"feed_url": feed_url, "episode_url": episode_url})
        return True
    else:
        return False


def get_latest_episode(url):
    """
        Parses the RSS feed for a given podcast url and returns the latest episode
    """
    feed = feedparser.parse(url)
    return feed.entries[0]


def fill_db_with_feed_entries(feed_url, db):
    """
        Fills the passed db with entries for all entries in the feed found at feed_url
    """
    feed = feedparser.parse(feed_url)

    for entry in feed.entries:
        for link in entry.links:
            if link["rel"] == "alternate":
                episode_url = link["href"]
                break
        db.insert({"feed_url": feed_url, "episode_url": episode_url})


async def watch_feed(feedwatcher):
    """
        Watches a podcast feed and sends a message to that shows channel whenever a new
        entry appears.
    """
    await client.wait_until_ready()
    channel = discord.Object(id=feedwatcher.channel_id)
    while not client.is_closed:
        latest_episode = get_latest_episode(feedwatcher.feed_url)

        # find the URL to the episode
        for link in latest_episode.links:
            if link["rel"] == "alternate":
                episode_url = link["href"]
                break

        if episode_is_new(feedwatcher.feed_url, episode_url):
            # If a filter is defined, the title of the episode must contain the filter or else it's ignored
            if feedwatcher.filter and feedwatcher.filter not in latest_episode["title"]:
                logger.info(
                    "Episode '{}' does not match filter.".format(
                        latest_episode["title"]
                    )
                )
            else:
                message = "+++ I RECEIVED A NEW {1} DATAFRAME +++ \n {0}".format(
                    episode_url, feedwatcher.show_name
                )
                await client.send_message(channel, message)
                logger.info(
                    "Sent message for new episode for {0}".format(feedwatcher.show_name)
                )
        else:
            logger.info("No new episode for {0}".format(feedwatcher.show_name))
        await asyncio.sleep(CONFIG["feed_watch_interval"])


commands = {"date": say_date, "quote": say_quote, "help": help_message}

if __name__ == "__main__":

    logger.add(
        os.path.join(CONFIG.get("log_dir", "/tmp"), "servitor.log"),
        format="{time} {level} {message}",
        level="INFO",
        rotation="03:00",
        retention="60 days",
    )

    parser = argparse.ArgumentParser(description="A loyal servant of the emperor")
    parser.add_argument("--fill-db", action="store_true")
    args = parser.parse_args()

    if args.fill_db:
        for watcher in CONFIG["feed_watchers"]:
            fill_db_with_feed_entries(watcher.feed_url, db)
            logger.info(f"Initialized DB with entries for {watcher.show_name}")
        sys.exit(0)

    else:
        client = discord.Client()
        for watcher in CONFIG["feed_watchers"]:
            client.loop.create_task(watch_feed(watcher))

        @client.event
        async def on_message(message):
            """
                Reply with a random quote if mentioned in a message.
            """
            for member in message.mentions:
                if member.id == CONFIG["bot_user_id"]:
                    m = re.search(r"!(?P<command>\S+)", message.content)
                    if m and m.group("command") in commands:
                        command = commands[m.group("command")]
                    else:
                        command = unknown_command
                    await command(message.channel)
                    break

        client.run(CONFIG["TOKEN"])
