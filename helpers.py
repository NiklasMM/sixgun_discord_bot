from collections import namedtuple
from datetime import date
import calendar
import math

FeedWatcher = namedtuple("FeedWatcher", ["channel_id", "feed_url", "show_name"])

# Some random quotes a Warhammer 40k servitor would say.
# See http://wh40k-de.lexicanum.com/wiki/Servitor
quotes = [
    "I exist to serve!",
    "Yes, Lord?",
    "Yes, most beneficent one?",
    "The memories of my past life... haunt me.",
    "Is this existance worse than death?",
    "The emperor protects.",
    "All systems functioning normalllllllllllllll 08x234.x.&88... ",
]


def date_to_imperial_date(input_datetime):
    """
        Calculates imperial year according to Warhammer 40k lore.

        See http://wh40k.lexicanum.com/wiki/Imperial_Dating_System
    """
    days_in_year = 366 if calendar.isleap(input_datetime.year) else 365
    hours_in_year = days_in_year * 24

    days_so_far = (input_datetime.date() - date(input_datetime.year, 1, 1)).days
    hours_so_far = (
        (days_so_far * 24) + input_datetime.hour + (input_datetime.minute / 60)
    )
    year_fraction = math.floor(((hours_so_far / hours_in_year) * 1000))

    year = input_datetime.year % 1000
    millenium = math.floor(input_datetime.year / 1000) + 1

    result = f"0 {year_fraction:03d} {year:03d}.M{millenium}"
    return result
