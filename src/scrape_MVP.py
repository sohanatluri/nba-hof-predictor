import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random


def get_MVP(url):
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
    table = raw_data.find("table", {"id": "mvp_summary"})
    if table is None:
        print(f"No table found for MVP data")
        return []

    # Extract the MVP data from the table
    mvp_data = []
    tbody = table.find("tbody")

    # finding the rows of the table
    for row in tbody.find_all("tr"):
        mvp_row = {}
        player_cell = row.find("th", {"data-stat": "player"})
        if player_cell:
            mvp_row["player"] = player_cell.text.strip()
        for cell in row.find_all("td"):
            stat_name = cell["data-stat"]

            if stat_name == "counter":  # Only extract the count of MVPs
                mvp_row["mvp_count"] = cell.text.strip()

            mvp_row["mvp_count"] = row.find(
                "td", {"data-stat": "counter"}).text.strip()
            mvp_row["league"] = row.find(
                "td", {"data-stat": "lg_id"}).text.strip()
            mvp_data.append(mvp_row)

    return mvp_data


def main():
    mvpData = []
    url = "https://www.basketball-reference.com/awards/mvp.html"

    mvp_data = get_MVP(url)

    mvpData.extend(mvp_data)

    # Convert the list of MVP data to a DataFrame
    df = pd.DataFrame(mvpData)

    # Save the DataFrame to a CSV file
    df.to_csv("../data/MVP.csv", index=False)


if __name__ == "__main__":
    main()
