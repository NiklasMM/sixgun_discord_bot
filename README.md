# Sixgun Discord Bot

This is a discord bot for the Podcast Network Sigun.org

Current features:

* Watches feeds for podcasts and posts messages for new episodes in the shows channel.


To run add a config file `config.py`, which looks like this:

```python
from helpers import FeedWatcher

CONFIG = {
    "TOKEN": "<the bot's access token>",
    "feed_watchers": [
        FeedWatcher(
            "<Channel ID>", "<Feed URL>", "<Show name>"
        )
    ],
    "feed_watch_interval": "<intervall for watchers in seconds>",
    "db_path": "<Path to the bot's DB file, eg. /tmp/bot.db>",
}

```
