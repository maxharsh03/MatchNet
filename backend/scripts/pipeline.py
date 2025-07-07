import subprocess
import time
from dotenv import load_dotenv
from pathlib import Path
import os


def run_script(name, path, timeout_seconds=120):
    print(f"▶️ Running {name}...")
    try:
        result = subprocess.run(["python", path], capture_output=True, text=True, timeout=timeout_seconds)
        
        if result.returncode == 0:
            print(f"✅ {name} completed.\n")
        else:
            print(f"❌ {name} failed with return code {result.returncode}:\n{result.stderr}\n")

    except subprocess.TimeoutExpired:
        print(f"⏰ {name} timed out after {timeout_seconds} seconds.\n")

    time.sleep(2)  # short delay to reduce resource conflicts

def main():
    # Load .env from root (adjust path as needed)
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
    elo_and_stats_path = resolve_path("ELO_AND_STATS_PATH")
    odds_path = resolve_path("ODDS_PATH")
    rankings_path = resolve_path("RANKINGS_PATH")
    tournament_and_surface_path = resolve_path("TOURNAMENT_AND_SURFACE_PATH")
    merge_data_path = resolve_path("MERGE_DATA_PATH")

    # 1. Run scrapers
    run_script("Elo Scraper", elo_and_stats_path)
    run_script("Odds Scraper", odds_path)
    run_script("Rankings Scraper", rankings_path)
    run_script("Tournament & Surface Scraper", tournament_and_surface_path)

    # 2. Merge and create CSVs
    run_script("Data Merge", merge_data_path)

if __name__ == "__main__":
    main()
