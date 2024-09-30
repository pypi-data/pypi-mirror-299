from ..util import get_page_soup


def fb_team_misc_stats(pageSoup=None, url: str = None) -> list:
    """Extracts miscellaneous stats for each team in a given league

    Args:
        pageSoup (bs4, optional): bs4 object of a team. Defaults to None.
        url (str, optional): path of fbref team page. Defaults to None.

    Returns:
        tuple: miscellaneous stats for home and away team players
            list: miscellaneous stats for each team
            list: miscellaneous stats against each team
    """

    assert (
        pageSoup is not None or url is not None
    ), "Either pageSoup or url must be provided"

    if pageSoup is None:
        pageSoup = get_page_soup(url)

    for side in ["for", "against"]:
        # generate empty list for each team
        mylist = []
        # generate html id
        id_ = "stats_squads_misc_" + side

        # find goalkeeping object
        stats = pageSoup.find("table", {"id": id_})
        stats = stats.find_all("tr")

        # iteratre through each team and store metrics
        for row in stats[2:]:
            th = row.find("th")
            # general
            team = th.find("a", {"href": True}).text.strip()
            team_id = th.find("a", {"href": True})["href"].split("/")[3]
            num_players = row.find("td", {"data-stat": "players_used"}).text
            matches = row.find("td", {"data-stat": "minutes_90s"}).text

            # performance
            cards_yellow = row.find("td", {"data-stat": "cards_yellow"}).text
            cards_red = row.find("td", {"data-stat": "cards_red"}).text
            cards_yellow_red = row.find("td", {"data-stat": "cards_yellow_red"}).text
            fouls = row.find("td", {"data-stat": "fouls"}).text
            fouled = row.find("td", {"data-stat": "fouled"}).text
            offsides = row.find("td", {"data-stat": "offsides"}).text
            crosses = row.find("td", {"data-stat": "crosses"}).text
            interceptions = row.find("td", {"data-stat": "interceptions"}).text
            tackles_won = row.find("td", {"data-stat": "tackles_won"}).text
            penalties_won = row.find("td", {"data-stat": "pens_won"}).text
            penalties_conceded = row.find("td", {"data-stat": "pens_conceded"}).text
            own_goals = row.find("td", {"data-stat": "own_goals"}).text
            recoveries = row.find("td", {"data-stat": "ball_recoveries"}).text

            # aerial duels
            aerials_won = row.find("td", {"data-stat": "aerials_won"}).text
            aerials_lost = row.find("td", {"data-stat": "aerials_lost"}).text
            aerials_won_pct = row.find("td", {"data-stat": "aerials_won_pct"}).text
            if aerials_won_pct == "":
                aerials_won_pct = None

            # generate dictionary for team
            mydict = {
                "team_id": team_id,
                "team": team,
                "num_players": num_players,
                "matches": matches,
                "cards_yellow": cards_yellow,
                "cards_red": cards_red,
                "cards_yellow_red": cards_yellow_red,
                "fouls": fouls,
                "fouled": fouled,
                "offsides": offsides,
                "crosses": crosses,
                "interceptions": interceptions,
                "tackles_won": tackles_won,
                "pk_won": penalties_won,
                "pk_con": penalties_conceded,
                "own_goals": own_goals,
                "recoveries": recoveries,
                "aerials_won": aerials_won,
                "aerials_lost": aerials_lost,
                "aerials_won_pct": aerials_won_pct,
            }

            # add to empty list
            mylist.append(mydict)

        # assign list to appropriate team
        if side == "for":
            misc_stats_for = mylist.copy()
        else:
            misc_stats_against = mylist.copy()

    return misc_stats_for, misc_stats_against
