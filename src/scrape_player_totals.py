import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import re


def get_player_stats(player_url, name):

    # choose random user agents to reduce the chance of being blocked
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0"
    ]

    headers = {"User-Agent": random.choice(USER_AGENTS)}

    # GET request to the URL with headers
    response = requests.get(player_url, headers=headers)

    # Check if the response status code indicates denial
    if response.status_code != 200:
        print(
            f"Request denied or failed with status code: {response.status_code}")
        return []

    # Parse the HTML content
    raw_data = BeautifulSoup(response.content, "html.parser")

    # find the table associated with the letter (player info)
    totals = raw_data.find("table", {"id": "totals_stats"})

    if totals is None:
        print(f"No table found for player {player_url}")

    # Extract the stats from the table
    stats = []

    tfoot = totals.find("tfoot")
    if tfoot is None:
        print(f"No footer found for player {player_url}")
        return []

    # finding the rows of the table (pattern match on the rows that have this format)
    career_row = tfoot.find("tr", id=re.compile(r"^totals_stats\.\d+ Yrs"))
    stats_row = {}
    stats_row["name"] = name

    # find stat associated with player
    for stat in career_row.find_all("td"):
        # get the stat name
        stat_name = stat["data-stat"]
        # get the stat value
        stat_value = stat.text.strip()
        # add to the stats dict
        stats_row[stat_name] = stat_value

    # Add the stats to the list
    stats.append(stats_row)

    return stats


def main():
    df = pd.read_csv("../data/players_data.csv")

    players_stats = []

    players_urls = df["player_url"].values.tolist()
    players_names = df["name"].values.tolist()

    # counter to keep track of the number of players scraped. Return player name
    i = 0

    for url in df["player_url"]:
        print("scraping stats for " + url)
        stats = get_player_stats(url, players_names[i])
        i += 1
        players_stats.extend(stats)

        # Sleep for a random time between 1 and 3 seconds to avoid being blocked
        time.sleep(random.uniform(1, 3))

    # export to csv
    players_stats_df = pd.DataFrame(players_stats)
    players_stats_df.to_csv("../data/players_stats.csv", index=False)


if __name__ == "__main__":
    main()
