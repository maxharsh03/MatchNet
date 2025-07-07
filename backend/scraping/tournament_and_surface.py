from playwright.sync_api import sync_playwright
import pandas as pd
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv
from pathlib import Path
import os

OUTPUT_DIR = "/Users/maxharsh/Desktop/Coding Projects/MatchNet/scraping/output"

def scrape_day_matches(page, status, date):
    matches = []

    try:
        page.wait_for_selector("div.leagues--live div.sportName.tennis", timeout=5000)
        tennis_section = page.query_selector("div.leagues--live div.sportName.tennis")
        if not tennis_section:
            return matches

        children = tennis_section.query_selector_all(":scope > *")
        i = 0
        while i < len(children):
            el = children[i]
            class_name = el.get_attribute("class") or ""

            if "wclLeagueHeader" in class_name:
                try:
                    title_div = el.query_selector("div.event__title")
                    span = title_div.query_selector("span.wcl-overline_rOFfd")
                    if span and span.inner_text().strip() == "ATP - SINGLES":
                        a_tag = title_div.query_selector("a")
                        tournament_surface = a_tag.inner_text().strip()
                        tournament, surface = map(str.strip, tournament_surface.split(",", 1))

                        i += 1
                        while i < len(children):
                            match_el = children[i]
                            match_class = match_el.get_attribute("class") or ""
                            if "event__match" not in match_class:
                                break

                            time_div = match_el.query_selector("div.event__time.event__time--usFormat")
                            player1_div = match_el.query_selector("div.event__participant.event__participant--home")
                            player2_div = match_el.query_selector("div.event__participant.event__participant--away")

                            match_data = {
                                "tournament": tournament,
                                "surface": surface,
                                "time": time_div.inner_text().strip() if time_div else None,
                                "player1": player1_div.inner_text().strip() if player1_div else None,
                                "player2": player2_div.inner_text().strip() if player2_div else None,
                                "date": date,
                                "status": status
                            }
                            matches.append(match_data)
                            i += 1
                        continue
                except Exception as e:
                    print(f"⚠️ Error parsing header/match: {e}")
            i += 1

    except Exception as e:
        print(f"⚠️ Error scraping matches: {e}")

    return matches

def click_calendar_next_day(page):
    try:
        page.wait_for_selector("div.calendarContainer", timeout=5000)
        arrow_buttons = page.query_selector_all("div.calendarContainer .wcl-arrow_8k9lP")
        if len(arrow_buttons) >= 2:
            arrow_buttons[-1].click()  # Next day
            print("➡️ Clicked 'Next Day'")
            time.sleep(2)
            return True
    except Exception as e:
        print(f"❌ Failed to click next day: {e}")
    return False

def click_tab_by_index(page, tab_index):
    page.wait_for_selector("div.filters__group")
    tabs = page.query_selector_all("div.filters__group > div")
    if len(tabs) > tab_index:
        tabs[tab_index].click()
        print(f"🔄 Clicked tab index {tab_index}")
        time.sleep(1)

def scrape_flashscore_all():
    today_str = datetime.today().strftime("%Y-%m-%d")
    tomorrow_str = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")

    all_matches = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.flashscoreusa.com/tennis/")

        # ✅ Accept cookies
        try:
            page.wait_for_selector('div#onetrust-banner-sdk button#onetrust-accept-btn-handler', timeout=3000)
            page.click('button#onetrust-accept-btn-handler')
            print("✅ Accepted cookies")
            time.sleep(0.5)
        except:
            print("⏭️ No cookie banner appeared")

        # 🔴 LIVE
        click_tab_by_index(page, 1)
        all_matches.extend(scrape_day_matches(page, status="LIVE", date=today_str))

        # 🟤 FINISHED (today only)
        click_tab_by_index(page, 3)
        all_matches.extend(scrape_day_matches(page, status="FINISHED", date=today_str))

        # ✅ SCHEDULED (today)
        click_tab_by_index(page, 4)
        all_matches.extend(scrape_day_matches(page, status="SCHEDULED", date=today_str))

        # ✅ SCHEDULED (tomorrow)
        if click_calendar_next_day(page):
            all_matches.extend(scrape_day_matches(page, status="SCHEDULED", date=tomorrow_str))

        browser.close()
        df = pd.DataFrame(all_matches)

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
        output_path = os.path.join(output_dir, "tournament_and_surface.csv")

        # Write to CSV
        df.to_csv(output_path, index=False)

        return df

if __name__ == "__main__":
    df = scrape_flashscore_all()
    print(df)
