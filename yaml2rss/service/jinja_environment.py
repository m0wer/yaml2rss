"""Module to store the Jinja environment with custom filters."""
import time
from datetime import datetime
from email import utils

from jinja2 import Environment, PackageLoader


def date_to_rfc2822(date: datetime) -> str:
    """Format date in RFC 2822 format.

    Arguments:
        date: `datetime` object.

    Returns:
        String with the date in RFC 2822 format.
    """
    return utils.formatdate(time.mktime(date.timetuple()), usegmt=True)


jinja_environment: Environment = Environment(loader=PackageLoader("yaml2rss"))
jinja_environment.filters["date_to_rfc2822"] = date_to_rfc2822
