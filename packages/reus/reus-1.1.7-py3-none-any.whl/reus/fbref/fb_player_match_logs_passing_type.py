from ..util import get_page_soup
from .util import match_log_iterator


def fb_player_match_logs_passing_type(
    pageSoup=None, season_end: str = None, player_id: str = None
) -> list:
    """Retrieves a players passing type match log for a given season

    Args:
        pageSoup (bs4, optional): bs4 object of a players passing type match log page. Defaults to None.
        season_end (str): ending year of a season
        player_id (str): unique identifier for a player

    Returns:
        list: passing type match log for a player in a given season
    """

    url = f"https://fbref.com/en/players/{player_id}/matchlogs/{int(season_end)-1}-{season_end}/passing_types/"

    assert (
        pageSoup is not None or player_id is not None
    ), "Either pageSoup or player_id must be provided"

    if pageSoup is None:
        pageSoup = get_page_soup(url)

    table = pageSoup.find("table")
    tbody = table.find("tbody")
    rows = tbody.find_all("tr")

    attributes = [
        "date",
        "url",
        "dayofweek",
        "comp",
        "round",
        "venue",
        "result",
        "team",
        "opponent",
        "game_started",
        "position",
        "minutes",
        "passes",
        "passes_live",
        "passes_dead",
        "passes_free_kicks",
        "through_balls",
        "passes_switches",
        "crosses",
        "throw_ins",
        "corner_kicks",
        "corner_kicks_in",
        "corner_kicks_out",
        "corner_kicks_straight",
        "passes_completed",
        "passes_offsides",
        "passes_blocked",
    ]

    mylist = match_log_iterator(rows=rows, attributes=attributes)

    return mylist
