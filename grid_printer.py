import requests
from bs4 import BeautifulSoup

def print_character_grid(doc_url: str):
    """
    Fetches a published Google Doc containing lines like:
    x-coordinate, y-coordinate, character
    and prints the 2D character grid.
    """
    response = requests.get(doc_url)
    response.raise_for_status()
    html = response.text

    soup = BeautifulSoup(html, "html.parser")
    matches = []
    for row in soup.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) == 3:
            x = cells[0].get_text(strip=True)
            char = cells[1].get_text(strip=True)
            y = cells[2].get_text(strip=True)
            # Skip header row
            if x.lower() == "x-coordinate" and char.lower() == "character" and y.lower() == "y-coordinate":
                continue
            matches.append((x, y, char))

    if not matches:
        print("No valid data found in the document.")
        return

    # Determine grid size
    max_x = max(int(x) for x, y, c in matches)
    max_y = max(int(y) for x, y, c in matches)

    # Initialize grid
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # Fill in characters
    for x, y, char in matches:
        grid[int(y)][int(x)] = char

    # Print the grid
    for row in grid:
        print(''.join(row))

# Example usage:
print_character_grid("https://docs.google.com/document/d/e/2PACX-1vRPzbNQcx5UriHSbZ-9vmsTow_R6RRe7eyAU60xIF9Dlz-vaHiHNO2TKgDi7jy4ZpTpNqM7EvEcfr_p/pub")
