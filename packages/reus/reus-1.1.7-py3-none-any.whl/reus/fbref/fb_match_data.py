from ..util import get_page_soup
from .fb_match_metadata import fb_match_metadata
from .fb_match_lineups import fb_match_lineups
from .fb_match_summary import fb_match_summary
from .fb_match_team_stats import fb_match_team_stats
from .fb_match_summary_stats import fb_match_summary_stats
from .fb_match_passing_stats import fb_match_passing_stats
from .fb_match_passing_type_stats import fb_match_passing_type_stats
from .fb_match_defensive_actions_stats import fb_match_defensive_actions_stats
from .fb_match_possession_stats import fb_match_possession_stats
from .fb_match_misc_stats import fb_match_misc_stats
from .fb_match_keeper_stats import fb_match_keeper_stats
from .fb_match_shots import fb_match_shots
from bs4 import BeautifulSoup


def fb_match_data(
    url: str, save_html: bool = False, html_file: BeautifulSoup = None
) -> tuple:
    """Extracts metadata and statistics for a given match that include Opta data. This includes summary match
    statistics for each team, summary stats for away team, passing, defensive, possession and goalkeeping stats

    Args:
        url (str): path of fbref match page
        save_html (bool, optional): whether to save html file. Defaults to False.
        html_file (BeautifulSoup, optional): pageSoup html file. Defaults to None.

    Returns:
        tuple: match data
            dict: metadata information
            dict: match officials
            dict: lineups
            list: events
            dict: summary statistics for each team
            list: summary stats of home team players
            list: summary stats of away team players
            list: passing stats of home team players
            list: passing stats of away team players
            list: passing type stats of home team players
            list: passing type stats of away team players
            list: defensive stats of home team players
            list: defensive stats of away team players
            list: possession stats of home team players
            list: possession stats of away team players
            list: miscellaneous stats of home team players
            list: miscellaneous stats of away team players
            list: goalkeeping stats of home team keeper
            list: goalkeeping stats of away team keeper
            list: shots for the match
            BeautifulSoup: html file (if save_html=True)
    """

    if html_file is None:
        page = "https://fbref.com" + url
        if save_html:
            pageSoup, pageContents = get_page_soup(page, save_html=save_html)
        else:
            pageSoup = get_page_soup(page)
    else:
        pageSoup = html_file

    metadata, officials = fb_match_metadata(pageSoup)
    lineups = fb_match_lineups(pageSoup)
    summary = fb_match_summary(pageSoup)
    team_stats = fb_match_team_stats(pageSoup)
    summary_stats_x, summary_stats_y = fb_match_summary_stats(pageSoup)
    passing_stats_x, passing_stats_y = fb_match_passing_stats(pageSoup)
    passing_type_stats_x, passing_type_stats_y = fb_match_passing_type_stats(pageSoup)
    defensive_stats_x, defensive_stats_y = fb_match_defensive_actions_stats(pageSoup)
    possession_stats_x, possession_stats_y = fb_match_possession_stats(pageSoup)
    misc_stats_x, misc_stats_y = fb_match_misc_stats(pageSoup)
    keeper_stats_x, keeper_stats_y = fb_match_keeper_stats(pageSoup)
    shots = fb_match_shots(pageSoup)

    if save_html:
        return (
            metadata,
            officials,
            lineups,
            summary,
            team_stats,
            summary_stats_x,
            summary_stats_y,
            passing_stats_x,
            passing_stats_y,
            passing_type_stats_x,
            passing_type_stats_y,
            defensive_stats_x,
            defensive_stats_y,
            possession_stats_x,
            possession_stats_y,
            misc_stats_x,
            misc_stats_y,
            keeper_stats_x,
            keeper_stats_y,
            shots,
            pageContents,
        )
    else:
        return (
            metadata,
            officials,
            lineups,
            summary,
            team_stats,
            summary_stats_x,
            summary_stats_y,
            passing_stats_x,
            passing_stats_y,
            passing_type_stats_x,
            passing_type_stats_y,
            defensive_stats_x,
            defensive_stats_y,
            possession_stats_x,
            possession_stats_y,
            misc_stats_x,
            misc_stats_y,
            keeper_stats_x,
            keeper_stats_y,
            shots,
        )
