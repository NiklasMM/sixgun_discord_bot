# Sixgun Discord Bot

This is a discord bot for the Podcast Network Sixgun.org

Current features:

* Watches feeds for podcasts and posts messages for new episodes in the shows channel.
* Replies with random servitor quote if mentioned.


To run add a config file `config.py`, which looks like this:

```python
from helpers import FeedWatcher

CONFIG = {
    "TOKEN": "<the bot's access token>",
    "bot_user_id": "<the id of the bot user>",
    "feed_watchers": [
        FeedWatcher(
            "<Channel ID>", "<Feed URL>", "<Show name>"
        )
    ],
    "feed_watch_interval": "<intervall for watchers in seconds>",
    "db_path": "<Path to the bot's DB file, eg. /tmp/bot.db>",
    "log_path": "<Path to a directory, where log files will be placed.>"
}

```
