import asyncio
from playwright.async_api import async_playwright
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
import os

OUTPUT_DIR = "/Users/maxharsh/Desktop/Coding Projects/MatchNet/scraping/output"

async def get_today_matches(playwright):
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context(viewport={"width": 1920, "height": 1080})
    page = await context.new_page()

    match_list = []
    today = datetime.today()

    target_date = today
    date_str = target_date.strftime("%Y%m%d")
    url = f"https://www.oddstrader.com/atp/?date={date_str}"

    await page.goto(url)
    await page.wait_for_selector("tbody.OddsGridstyles__TableBody-sc-1c1x33-3", timeout=15000)
    
    rows = await page.query_selector_all("tbody.OddsGridstyles__TableBody-sc-1c1x33-3 > tr")
    print(f"[{date_str}] Found {len(rows)} rows")

    for i in range(0, len(rows) - 2, 3):
        player1_tr = rows[i + 1]
        player2_tr = rows[i + 2]

        async def get_player_name(tr):
            try:
                el = await tr.query_selector("span.teamName.blueHover")
                return (await el.inner_text()).strip() if el else "Unknown"
            except:
                return "Unknown"

        player1_name = await get_player_name(player1_tr)
        player2_name = await get_player_name(player2_tr)

        async def extract_betting_odds(tr_element):
            odds = []
            try:
                tds = await tr_element.query_selector_all("td")
                for td in tds:
                    span = await td.query_selector("span")
                    if span:
                        text = (await span.inner_text()).strip()
                        if text:
                            odds.append(text)
            except:
                pass
            return odds[1:]  # Skip the first one
        player1_odds = await extract_betting_odds(player1_tr)
        player2_odds = await extract_betting_odds(player2_tr)

        try:
            status_div = await player1_tr.query_selector("td.first-participant div.eventStatus")
            status_spans = await status_div.query_selector_all("span") if status_div else []
            status_1 = (await status_spans[0].inner_text()).strip() if len(status_spans) > 0 else None
            status_2 = (await status_spans[1].inner_text()).strip() if len(status_spans) > 1 else None
        except:
            status_1, status_2 = None, None

        if status_1:
            if "LIVE" in status_1.upper():
                match_status = "LIVE"
            elif "FINAL" in status_1.upper():
                match_status = "FINISHED"
            elif "CANCELED" in status_1.upper():
                match_status = "CANCELED"
            else:
                match_status = "SCHEDULED"
        else:
            match_status = "SCHEDULED"

        async def get_score(tr, selector):
            try:
                div = await tr.query_selector(selector)
                score = (await div.inner_text()).strip() if div else "-"
                return "-" if "%" in score else score
            except:
                return "-"

        player1_score = await get_score(player1_tr, "td.first-participant div.participant div.TeamContainerstyles__ConsensusOrScore-sc-y43dva-3 div")
        player2_score = await get_score(player2_tr, "td div.participant div.TeamContainerstyles__ConsensusOrScore-sc-y43dva-3 div")

        match_list.append({
            "match_date": target_date.strftime("%Y-%m-%d"),
            "player1_name": player1_name,
            "player1_odds": player1_odds,
            "player2_name": player2_name,
            "player2_odds": player2_odds,
            "status_1": status_1,
            "status_2": status_2,
            "player1_score": player1_score,
            "player2_score": player2_score,
            "match_status": match_status
        })

    await browser.close()

    df = pd.DataFrame(match_list)
    df = df[~((df["player1_name"] == "Unknown") & (df["player2_name"] == "Unknown"))]

    # Sort
    status_order = {"FINISHED": 0, "CANCELED": 1, "LIVE": 2, "SCHEDULED": 3}
    df["status_sort"] = df["match_status"].map(status_order)
    df = df.sort_values(by=["match_date", "status_sort"]).drop(columns=["status_sort"])
    # df.to_csv(f"{OUTPUT_DIR}/odds1.csv", index=False)
    return df

async def get_tomorrow_matches(playwright):
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context(viewport={"width": 1920, "height": 1080})
    page = await context.new_page()

    match_list = []
    today = datetime.today()

    target_date = today + timedelta(days=1)
    date_str = target_date.strftime("%Y%m%d")
    url = f"https://www.oddstrader.com/atp/?date={date_str}"

    await page.goto(url)
    await page.wait_for_selector("tbody.OddsGridstyles__TableBody-sc-1c1x33-3", timeout=15000)
    
    rows = await page.query_selector_all("tbody.OddsGridstyles__TableBody-sc-1c1x33-3 > tr")
    print(f"[{date_str}] Found {len(rows)} rows")

    for i in range(0, len(rows) - 2, 3):
        player1_tr = rows[i + 1]
        player2_tr = rows[i + 2]

        async def get_player_name(tr):
            try:
                el = await tr.query_selector("span.teamName.blueHover")
                return (await el.inner_text()).strip() if el else "Unknown"
            except:
                return "Unknown"

        player1_name = await get_player_name(player1_tr)
        player2_name = await get_player_name(player2_tr)

        async def extract_betting_odds(tr_element):
            odds = []
            try:
                tds = await tr_element.query_selector_all("td")
                for td in tds:
                    span = await td.query_selector("span")
                    if span:
                        text = (await span.inner_text()).strip()
                        if text:
                            odds.append(text)
            except:
                pass
            return odds[1:]  # Skip the first one
        player1_odds = await extract_betting_odds(player1_tr)
        player2_odds = await extract_betting_odds(player2_tr)

        try:
            status_div = await player1_tr.query_selector("td.first-participant div.eventStatus")
            status_spans = await status_div.query_selector_all("span") if status_div else []
            status_1 = (await status_spans[0].inner_text()).strip() if len(status_spans) > 0 else None
            status_2 = (await status_spans[1].inner_text()).strip() if len(status_spans) > 1 else None
        except:
            status_1, status_2 = None, None

        if status_1:
            if "LIVE" in status_1.upper():
                match_status = "LIVE"
            elif "FINAL" in status_1.upper():
                match_status = "FINISHED"
            elif "CANCELED" in status_1.upper():
                match_status = "CANCELED"
            else:
                match_status = "SCHEDULED"
        else:
            match_status = "SCHEDULED"

        async def get_score(tr, selector):
            try:
                div = await tr.query_selector(selector)
                score = (await div.inner_text()).strip() if div else "-"
                return "-" if "%" in score else score
            except:
                return "-"

        player1_score = await get_score(player1_tr, "td.first-participant div.participant div.TeamContainerstyles__ConsensusOrScore-sc-y43dva-3 div")
        player2_score = await get_score(player2_tr, "td div.participant div.TeamContainerstyles__ConsensusOrScore-sc-y43dva-3 div")

        match_list.append({
            "match_date": target_date.strftime("%Y-%m-%d"),
            "player1_name": player1_name,
            "player1_odds": player1_odds,
            "player2_name": player2_name,
            "player2_odds": player2_odds,
            "status_1": status_1,
            "status_2": status_2,
            "player1_score": player1_score,
            "player2_score": player2_score,
            "match_status": match_status
        })

    await browser.close()

    df = pd.DataFrame(match_list)
    df = df[~((df["player1_name"] == "Unknown") & (df["player2_name"] == "Unknown"))]

    # Sort
    status_order = {"FINISHED": 0, "CANCELED": 1, "LIVE": 2, "SCHEDULED": 3}
    df["status_sort"] = df["match_status"].map(status_order)
    df = df.sort_values(by=["match_date", "status_sort"]).drop(columns=["status_sort"])
    # df.to_csv(f"{OUTPUT_DIR}/odds2.csv", index=False)
    return df

async def main():
    async with async_playwright() as playwright:
        betting_df1 = await get_today_matches(playwright)
        print("\n--- Today's Betting Odds Preview ---")
        print(betting_df1.head())

        betting_df2 = await get_tomorrow_matches(playwright)
        print("\n--- Tomorrow's Betting Odds Preview ---")
        print(betting_df2.head())

        # Combine the two DataFrames
        combined_df = pd.concat([betting_df1, betting_df2], ignore_index=True)

        # Drop rows where both players are unknown
        combined_df = combined_df[~((combined_df["player1_name"] == "Unknown") & (combined_df["player2_name"] == "Unknown"))]

        # Sort by match date and match status
        status_order = {"FINISHED": 0, "CANCELED": 1, "LIVE": 2, "SCHEDULED": 3}
        combined_df["status_sort"] = combined_df["match_status"].map(status_order)
        combined_df = combined_df.sort_values(by=["match_date", "status_sort"]).drop(columns=["status_sort"])

        # Load project root
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
        output_path = os.path.join(output_dir, "odds.csv")

        # Write to CSV
        combined_df.to_csv(output_path, index=False)

        print("\n--- Combined Betting Odds DataFrame Preview ---")
        print(combined_df.head())

if __name__ == "__main__":
    asyncio.run(main())
