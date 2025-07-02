from playwright.sync_api import sync_playwright
import pandas as pd
from dotenv import load_dotenv
from pathlib import Path
import os

OUTPUT_DIR = "/Users/maxharsh/Desktop/Coding Projects/MatchNet/scraping/output"

def get_atp_rankings():
    ranking_data = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.atptour.com/en/rankings/singles?rankRange=0-5000", timeout=60000)

        # Wait for the updated table class
        page.wait_for_selector("table.mega-table.desktop-table.non-live tbody tr", timeout=15000)

        rows = page.query_selector_all("table.mega-table.desktop-table.non-live tbody tr")
        print(f"Found {len(rows)} table rows")

        for row in rows:
            try:
                tds = row.query_selector_all("td")
                if len(tds) >= 5:
                    rank = tds[0].inner_text().strip()

                    li_tags = tds[1].query_selector_all("li")
                    if len(li_tags) >= 3:
                        name_span = li_tags[2].query_selector("span")
                        player_name = name_span.inner_text().strip() if name_span else "Unknown"
                    else:
                        player_name = "Unknown"

                    rank_points = tds[3].inner_text().strip()

                    ranking_data.append({
                        "rank": rank,
                        "player_name": player_name,
                        "rank_points": rank_points
                    })
            except Exception as e:
                print("Error processing row:", e)

        browser.close()

    df = pd.DataFrame(ranking_data)
    #df.to_csv(f"{OUTPUT_DIR}/atp_rankings.csv", index=False)
    return df

if __name__ == "__main__":
    rankings_df = get_atp_rankings()

    PROJECT_ROOT = Path(__file__).resolve().parents[2]  # Assumes this script is in `backend/scraping/` or similar

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
    output_path = os.path.join(output_dir, "atp_rankings.csv")

    # Write to CSV
    rankings_df.to_csv(output_path, index=False)

    print("\n--- ATP Rankings DataFrame Preview ---")
    print(rankings_df.head())
