import pandas as pd
from thefuzz import fuzz

from constants import LOW_THRESHOLD
from models import Alias


def get_events_df_per_date(df, date):
    """
    Get a Pandas Dataframe where each row has as date the date given
    :param df: The Pandas Dataframe to filter
    :param date: A Datetime.Date to filter
    :return: A Pandas Dataframe filtered by the date
    """
    df_filtered = df[df["FECHA"] == date]
    return df_filtered


def filter_events_using_substring(df, txt, threshold=LOW_THRESHOLD):
    """
    Filter the rows of a Pandas Dataframe where some attributes contain the substring given
    :param df: The Pandas Dataframe to filter
    :param txt: The substring to search
    :param threshold: The minimum score allowed to match an approximate search
    :return: A Pandas Dataframe where each rows contain the substring given or approximate.
    """
    df_cpy = df.copy()
    df_with_teams = add_teams(df_cpy)
    df_with_teams["Score"] = df_with_teams.apply(
        lambda entry: calculate_score(entry, txt), axis=1
    )
    df_approximate = get_approximate_matches(df_with_teams, threshold=threshold)
    df_substring = get_matches_are_substring(df_with_teams, txt)
    matches = pd.concat([df_substring, df_approximate])
    events = matches.drop_duplicates()
    return events


def add_teams(df):
    """
    Add teams to DataFrame
    :param df: The Pandas Dataframe
    :return: A pandas.DataFrame
    """
    df_cpy = df.copy()
    df_cpy["team_1"] = df_cpy.apply(lambda r: split_by_team(r)[0], axis=1)
    df_cpy["team_2"] = df_cpy.apply(lambda r: split_by_team(r)[1], axis=1)
    return df_cpy


def split_by_team(r):
    """
    Split a row by team
    :param r: The Pandas Dataframe row
    :return: A list
    """
    event = r["PARTIDO"]
    split = list(map(lambda team: team.strip(), event.split("v/s")))
    split = split if len(split) == 2 else [event, event]
    return split


def get_matches_are_substring(df, txt):
    """
    Filter the rows of a Pandas Dataframe where some attributes contain the substring given
    :param df: The Pandas Dataframe to filter
    :param txt: The substring to search
    :return: A Pandas Dataframe where each rows contain the substring given.
    """
    df_cpy = df.copy()
    return df_cpy[
        df_cpy["PARTIDO"].str.contains(txt, case=False)
        | df_cpy["COMPETENCIA"].str.contains(txt, case=False)
        | df_cpy["CANAL"].str.contains(txt, case=False)
    ]


def get_approximate_matches(df, threshold):
    """
    Filter the rows of a Pandas Dataframe with a threshold for a specific column
    :param df: The Pandas Dataframe to filter
    :param threshold: The minimum value to filter
    :return: A Pandas Dataframe filtered.
    """
    df_cpy = df.copy()
    return df_cpy[df_cpy["Score"] >= threshold]


def calculate_score(row, txt):
    """
    Calculate the coincidence of the row with a substring
    :param row: The Pandas Dataframe row
    :param txt: The substring to search
    :return: An int that represents the match score between the row and the given text.
    """
    fields_and_weight = [
        {"field": "PARTIDO", "weight": 1},
        {"field": "COMPETENCIA", "weight": 1},
        {"field": "CANAL", "weight": 1},
        {"field": "team_1", "weight": 1},
        {"field": "team_2", "weight": 1},
    ]

    scores = [
        fuzz.partial_ratio(txt.lower(), row[entry["field"]].lower()) * entry["weight"]
        for entry in fields_and_weight
    ]

    return max(scores)


async def may_get_team_name_from_user_and_alias(user_id: str, alias: str) -> str | None:
    """
    Get the team name from the user and the alias
    """
    alias = await Alias.objects.get_or_none(user_id=user_id, alias=alias)
    if not alias:
        return None
    return alias.team_name
