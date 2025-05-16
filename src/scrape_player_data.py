import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://www.basketball-reference.com"
LETTERS = "abcdefghijklmnopqrstuvwxyz"


def scrape_player_data(current_letter):
    url = BASE_URL + "/players/" + current_letter + "/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    # GET request to the URL with headers
    response = requests.get(url, headers=headers)

    # Check if the response status code indicates denial
    if response.status_code != 200:
        print(
            f"Request denied or failed with status code: {response.status_code}")
        return []

    # Parse the HTML content
    raw_data = BeautifulSoup(response.content, "html.parser")

    # find the table associated with the letter (player info)
    table = raw_data.find("table", {"id": "players"})

    if table is None:
        print(f"No table found for letter {current_letter}")

    players = []
    tbody = table.find("tbody")

    # finding the rows of the table
    for row in tbody.find_all("tr"):
        #find player URL
        player_cell = row.find("th", {"data-stat": "player"})
        link = player_cell.find("a")

        if not link:
            continue
        
        player_url = BASE_URL + link["href"]

        # Check if the name contains an asterisk
        name = row.find("th", {"data-stat": "player"}).text.strip()
        hof = 1 if "*" in name else 0
        name = name.replace("*", "")

        # Extract start and end years
        start_year = row.find("td", {"data-stat": "year_min"}).text.strip()
        end_year = row.find("td", {"data-stat": "year_max"}).text.strip()

        # Calculate career length and filter out players with careers < 4 years
        if int(end_year) - int(start_year) < 4 or int(end_year) < 1976:
            continue

        pos = row.find("td", {"data-stat": "pos"}).text.strip()
        height = row.find("td", {"data-stat": "height"}).text.strip()
        weight = row.find("td", {"data-stat": "weight"}).text.strip()

        # add the player data to the list
        players.append({
            "name": name,
            "start_year": start_year,
            "end_year": end_year,
            "pos": pos,
            "height": height,
            "weight": weight,
            "hof": hof,
            "player_url": player_url
        })

    return players


def main():
    all_players = []
    for letter in LETTERS:
        print("scrapping for letter " + letter)
        player = scrape_player_data(letter)
        all_players.extend(player)

    # Create a DataFrame from the list of players
    df = pd.DataFrame(all_players)

    # Save the DataFrame to a CSV file
    df.to_csv("../data/players_data.csv", index=False)


if __name__ == "__main__":
    main()
