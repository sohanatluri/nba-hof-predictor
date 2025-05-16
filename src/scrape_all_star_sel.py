import pandas as pd
import requests
from bs4 import BeautifulSoup


def get_all_star_totals(url):
    # Define headers to mimic a browser request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    # Send a GET request to the URL
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        print(f"Request denied or failed with status code: {response.status_code}")
        return []

    # Parse the HTML content of the page
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table with the All Star Selection data
    table = soup.find("table", {"id": "all_star_by_player"})

    # If the table is not found, return an empty list
    if table is None:
        print("No table found for All Star Selection data")
        return []

    # Initialize a list to store the All Star data
    all_star_data = []

    # Find the table body containing the rows of data
    tbody = table.find("tbody")

    # Iterate through each row in the table body
    for row in tbody.find_all("tr"):
        all_star_sel = {}

        # Extract the player's name
        player = row.find("a").text.strip()

        # Extract all the table data cells in the row
        tds = row.find_all("td")

        # Extract the total All Star selections
        total_sel = tds[2].text.strip()

        # Add the extracted data to the dictionary
        all_star_sel["player"] = player
        all_star_sel["total_selections"] = total_sel

        # Append the dictionary to the list
        all_star_data.append(all_star_sel)

    # Return the list of All Star data
    return all_star_data


def main():
    url = "https://www.basketball-reference.com/awards/all_star_by_player.html"

    all_star_data = get_all_star_totals(url)

    df = pd.DataFrame(all_star_data)
    df.to_csv("../data/all_star_sel.csv", index=False)


if __name__ == "__main__":
    main()
