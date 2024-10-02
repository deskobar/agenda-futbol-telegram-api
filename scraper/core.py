import pandas as pd
import requests
import io
from bs4 import BeautifulSoup
from cache import ttl_cache
from settings import URL, REQUEST_TIMEOUT
from utils import parse_day_to_date


def get_html_text():
    """
    Get the HTML content as plain text
    :return: A string html
    """
    r = requests.get(URL, timeout=REQUEST_TIMEOUT)
    return r.text


def get_channels(html_text):
    """
    Get the channels of each event from an HTML as plain text
    :param html_text: The HTML as plain text
    :return: A List of string, where each below to a Channel.
    """
    soup = BeautifulSoup(html_text, "html.parser")
    channels_elements = soup.findAll("img", class_="di-tv-channel-thumb", alt=True)
    channels = [channel["alt"] for channel in channels_elements]
    return channels


def process_df_using_html(df, html):
    """
    Drop unused columns from a dataframe
    :param df: A Pandas DataFrame
    :param html: A HTML body
    :return: A Pandas DataFrame
    """
    df_cpy = df.copy()
    df_cpy = df_cpy.drop(["PARTIDO.1", "PARTIDO.2", "PARTIDO.3"], axis=1)
    channels = get_channels(html)
    df_cpy["FECHA"] = df_cpy["FECHA"].map(
        lambda fecha: parse_day_to_date(int(fecha[-2:]))
    )
    df_cpy["CANAL"] = channels
    return df_cpy


@ttl_cache(ttl=60)
def get_events_df():
    """
    Get a Pandas Dataframe with all the events available in the target WebSite.
    :return: A Pandas Dataframe.
    """
    html = get_html_text()
    raw_df = pd.read_html(io.StringIO(html))[0]
    df = process_df_using_html(raw_df, html)
    return df
