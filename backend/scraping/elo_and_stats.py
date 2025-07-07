from playwright.sync_api import sync_playwright
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import os

def scrape_tennis_elo():
    data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        url = "https://tennisabstract.com/reports/atp_elo_ratings.html"
        page.goto(url, timeout=60000)
        page.wait_for_selector("table.tablesorter tbody tr", timeout=15000)

        rows = page.query_selector_all("table.tablesorter tbody tr")
        print(f"Found {len(rows)} table rows")

        for idx, row in enumerate(rows[:-1]):  # skip last row (summary)
            try:
                cells = row.query_selector_all("td")
                if len(cells) < 16:
                    continue  # malformed row

                # Try to extract name from <a> if present
                name_cell = cells[1]
                name_link = name_cell.query_selector("a")
                if name_link:
                    player_name = name_link.inner_text().strip()
                else:
                    player_name = name_cell.inner_text().strip()

                record = {
                    "Elo Rank": cells[0].inner_text().strip(),
                    "player name": player_name,
                    "age": cells[2].inner_text().strip(),
                    "elo": cells[3].inner_text().strip(),
                    "hElo rank": cells[5].inner_text().strip(),
                    "hElo": cells[6].inner_text().strip(),
                    "cElo rank": cells[7].inner_text().strip(),
                    "cElo": cells[8].inner_text().strip(),
                    "gElo rank": cells[9].inner_text().strip(),
                    "gElo": cells[10].inner_text().strip(),
                    "peak elo": cells[12].inner_text().strip(),
                    "peak month": cells[13].inner_text().strip(),
                    "atp rank": cells[15].inner_text().strip()
                }

                data.append(record)
            except Exception as e:
                print(f"⚠️ Error processing row {idx}: {e}")

        browser.close()

    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    # Load from root
    PROJECT_ROOT = Path(__file__).resolve().parents[1]  # Assumes this script is in `backend/scraping/` or similar

    # Step 2: Load .env from root
    load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

    # Step 3: Resolve all env vars to absolute paths
    def resolve_path(var_name):
        relative_path = os.getenv(var_name)
        if not relative_path:
            raise ValueError(f"{var_name} not found in .env")
        return PROJECT_ROOT / relative_path

    # Get the output directory from the environment
    output_dir = resolve_path("SCRAPING_OUTPUT_DIR")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Define the output file path
    output_path = os.path.join(output_dir, "elo_and_stats.csv")
    
    # Retrieve data frame
    df = scrape_tennis_elo()

    # Save it to a csv file
    df.to_csv(output_path, index=False)

    print(df.head())
