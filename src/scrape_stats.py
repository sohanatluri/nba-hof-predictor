import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random


def get_player_stats(player_url):

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
    stats.append({"player_url": player_url})

    tfoot = totals.find("tfoot")
    if tfoot is None:
        print(f"No footer found for player {player_url}")
        return []

    # finding the rows of the table
    for row in tfoot.find_all("tr", {"id": "totals_stats.20 Yrs"}):
        stats_row = {}

        # Extract the stats from the row
        for cell in row.find_all("td"):
            stat_name = cell["data-stat"]
            stat_value = cell.text.strip()
            stats_row[stat_name] = stat_value
        stats.append(stats_row)

    # find the table associated with the letter (player info)
    advanced_stats = raw_data.find("table", {"id": "advanced"})

    if advanced_stats is None:
        print(f"No table found for player {player_url}")

    # Extract the stats from the table
    tfoot = advanced_stats.find("tfoot")
    if tfoot is None:
        print(f"No footer found for player {player_url}")
        return []

    for row in tfoot.find_all("tr", {"id": "advanced.20 Yrs"}):
        stats_row = {}

        # Extract the stats from the row
        for cell in row.find_all("td"):
            stat_name = cell["data-stat"]
            stat_value = cell.text.strip()
            stats_row[stat_name] = stat_value
        stats.append(stats_row)

    return stats


def main():
    df = pd.read_csv("../data/players_data.csv")

    players_stats = []
    for url in df["player_url"]:
        print("scraping stats for " + url)
        stats = get_player_stats(url)
        print(stats)
        if stats:
            players_stats.append(stats)
        
        # Sleep for a random time between 1 and 3 seconds to avoid being blocked
        time.sleep(random.uniform(1, 3))

    # export to csv
    players_stats_df = pd.DataFrame(players_stats)
    players_stats_df.to_csv("../data/players_stats.csv", index=False)


if __name__ == "__main__":
    main()
