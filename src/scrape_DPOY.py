import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random


def get_DPOY(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(
            f"Request denied or failed with status code: {response.status_code}")
        return []

    raw_data = BeautifulSoup(response.content, "html.parser")

    table = raw_data.find("table", {"id": "dpoy_summary"})
    if table is None:
        print("No table found for DPOY data")
        return []

    dpoy_data = []
    tbody = table.find("tbody")

    for row in tbody.find_all("tr"):
        player_cell = row.find("th", {"data-stat": "player"})
        if not player_cell:
            continue  # skip malformed rows

        name = player_cell.text.strip()
        count = row.find("td", {"data-stat": "counter"}).text.strip()
        league = row.find("td", {"data-stat": "lg_id"}).text.strip()

        dpoy_data.append({
            "player": name,
            "dpoy_count": count,
            "league": league
        })

    return dpoy_data


def main():
    dpoyData = []
    url = "https://www.basketball-reference.com/awards/dpoy.html"

    data = get_DPOY(url)

    dpoyData.extend(data)

    # Convert the list of MVP data to a DataFrame
    df = pd.DataFrame(dpoyData)

    # Save the DataFrame to a CSV file
    df.to_csv("../data/DPOY.csv", index=False)


if __name__ == "__main__":
    main()
