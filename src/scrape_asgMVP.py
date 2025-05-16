import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_all_star_MVP(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(
            f"Request denied or failed with status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"id": "all_star_mvp_summary"})

    if table is None:
        print("No table found for All-Star MVP data")
        return []

    all_star_data = []
    tbody = table.find("tbody")

    for row in tbody.find_all("tr"):
        asg_mvp_row = {}
        player_cell = row.find("th", {"data-stat": "player"})
        if player_cell:
            asg_mvp_row["player"] = player_cell.text.strip()

            # Only add data if player exists
            asg_mvp_row["asg_mvp_count"] = row.find(
                "td", {"data-stat": "counter"}).text.strip()
            asg_mvp_row["league"] = row.find(
                "td", {"data-stat": "lg_id"}).text.strip()
            all_star_data.append(asg_mvp_row)

    return all_star_data


def main():
    url = "https://www.basketball-reference.com/awards/all_star_mvp.html"
    data = get_all_star_MVP(url)

    df = pd.DataFrame(data)
    df.to_csv("../data/asg_MVP.csv", index=False)


if __name__ == "__main__":
    main()
