import pandas as pd
import requests
from bs4 import BeautifulSoup
import time


def get_allNBA_tally(url):
    # Define headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Send a GET request to the URL
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(
            f"Request denied or failed with status code: {response.status_code}")
        return []

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table with the All NBA Selection data
    table = soup.find("table", {"id": "awards_all_league"})

    # If the table is not found, return an empty list
    if table is None:
        print("No table found for All NBA Selection data")
        return []

    # Initialize a list to store the All Star data
    all_nba_data = []

    # Find the table body containing the rows of data
    tbody = table.find("tbody")

    for row in tbody.find_all("tr"):
        all_nba_sel = {}

        team_num = row.find("td", {"data-stat": "all_team"}).text.strip()

        tds = row.find_all("td")

        for td in tds:
            if td.find("a") is None:
                continue
            # Extract the player's name
            player_name = td.find("a").text.strip()

            # Not the players name
            if player_name == "NBA" or player_name == "V":
                continue

            # if player is in the list, add 1 to the count to the corresponding team
            if any(player_name == player["Player"] for player in all_nba_data):

                # Check where the player is in the list
                for player in all_nba_data:
                    if player["Player"] == player_name:
                        if team_num == "1st":
                            player["1st"] += 1
                        elif team_num == "2nd":
                            player["2nd"] += 1
                        else:
                            player["3rd"] += 1
                        break

            # if player is not in the list, add the player to the list and add count to the corresponding team
            else:
                all_nba_sel["1st"] = 0
                all_nba_sel["2nd"] = 0
                all_nba_sel["3rd"] = 0

                if team_num == "1st":
                    all_nba_sel["1st"] += 1
                elif team_num == "2nd":
                    all_nba_sel["2nd"] += 1
                else:
                    all_nba_sel["3rd"] += 1

                # Ensure the player's data is stored correctly
                all_nba_data.append({
                    "Player": player_name,
                    "1st": all_nba_sel["1st"],
                    "2nd": all_nba_sel["2nd"],
                    "3rd": all_nba_sel["3rd"]
                })

    # Return the list of All NBA data
    return all_nba_data


def main():
    url = "https://www.basketball-reference.com/awards/all_league.html"

    # Get the All NBA data
    all_nba_data = get_allNBA_tally(url)

    # Convert the data to a list of dictionaries
    df = pd.DataFrame(all_nba_data)
    df.to_csv("../data/all_NBA_sel.csv", index=False)


if __name__ == "__main__":
    main()
