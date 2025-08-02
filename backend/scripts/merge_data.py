import pandas as pd
import os
from dotenv import load_dotenv
from pathlib import Path
from rapidfuzz import fuzz, process


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
atp_rankings_csv_path = resolve_path("ATP_RANKINGS_CSV")
elo_and_stats_csv_path = resolve_path("ELO_AND_STATS_CSV")
players_and_odds_csv_path = resolve_path("ODDS_CSV")
tournament_and_surface_csv_path = resolve_path("TOURNAMENT_AND_SURFACE_CSV")

# === Load CSVs ===
atp_rankings = pd.read_csv(atp_rankings_csv_path)
elo_and_stats = pd.read_csv(elo_and_stats_csv_path)
players_and_odds = pd.read_csv(players_and_odds_csv_path)
tournament_and_surface = pd.read_csv(tournament_and_surface_csv_path)

# === Strip whitespace from all name fields ===
atp_rankings['player_name'] = atp_rankings['player_name'].str.strip()
elo_and_stats['player name'] = elo_and_stats['player name'].str.strip()
players_and_odds['player1_name'] = players_and_odds['player1_name'].str.strip()
players_and_odds['player2_name'] = players_and_odds['player2_name'].str.strip()
tournament_and_surface['player1'] = tournament_and_surface['player1'].str.strip()
tournament_and_surface['player2'] = tournament_and_surface['player2'].str.strip()

# === Normalize all names to title-case for consistency ===
import re

def clean_name(name):
    if not isinstance(name, str):
        return ""
    # Replace all types of spaces with a regular space, then strip
    name = name.replace("\xa0", " ").replace("\u00A0", " ")
    name = re.sub(r"\s+", " ", name)  # Collapse multiple spaces
    return name.strip().title()


for col in ['player1_name', 'player2_name']:
    players_and_odds[col] = players_and_odds[col].map(clean_name)

for col in ['player1', 'player2']:
    tournament_and_surface[col] = tournament_and_surface[col].map(clean_name)

atp_rankings['player_name'] = atp_rankings['player_name'].map(clean_name)
elo_and_stats['player name'] = elo_and_stats['player name'].map(clean_name)

# === Build short_name to full_name map ===
def full_to_short(full_name):
    parts = full_name.strip().split()
    if len(parts) < 2:
        return None
    first = parts[0]
    last = " ".join(parts[1:])
    return f"{last} {first[0]}."

atp_rankings['short_name'] = atp_rankings['player_name'].apply(full_to_short)
short_to_full_map = dict(zip(atp_rankings['short_name'], atp_rankings['player_name']))

# === Map short → full names in tournament_and_surface ===
tournament_and_surface['player1'] = tournament_and_surface['player1'].map(
    short_to_full_map).fillna(tournament_and_surface['player1'])
tournament_and_surface['player2'] = tournament_and_surface['player2'].map(
    short_to_full_map).fillna(tournament_and_surface['player2'])

# === PLAYER DataFrame ===
player_df = atp_rankings.rename(columns={
    'player_name': 'name',
    'rank': 'rank',
    'rank_points': 'rank_points'
})[['name', 'rank', 'rank_points']]

# Names in elo_and_stats (after cleaning)
elo_names = set(elo_and_stats['player name'])
# Names in atp_rankings (after cleaning)
atp_names = set(atp_rankings['player_name'])

# Names in elo not found in rankings
diff = elo_names - atp_names
print(f"❌ {len(diff)} names in ELO not found in ATP rankings:\n", sorted(diff))

# === PLAYER_STATS DataFrame ===
player_stats_df = elo_and_stats.rename(columns={
    'player name': 'name',
    'Elo Rank': 'elo_rank',
    'age': 'age',
    'elo': 'elo',
    'hElo rank': 'hElo_rank',
    'hElo': 'hElo',
    'cElo rank': 'cElo_rank',
    'cElo': 'cElo',
    'gElo rank': 'gElo_rank',
    'gElo': 'gElo',
    'peak elo': 'peak_elo',
    'peak month': 'peak_month',
    'atp rank': 'atp_rank'
})[['name', 'atp_rank', 'age', 'elo', 'elo_rank', 'hElo', 'hElo_rank',
    'cElo', 'cElo_rank', 'gElo', 'gElo_rank', 'peak_elo', 'peak_month']]

'''
# Merge rank_points into player_stats
player_stats_df = pd.merge(player_stats_df, atp_rankings[['player_name', 'rank_points']],
                           left_on='name', right_on='player_name', how='left').drop(columns=['player_name'])
'''

# Use already-normalized player_df
player_stats_df = pd.merge(
    player_stats_df,
    player_df[['name', 'rank_points']],
    on='name',
    how='left'
)

# Step 1: Build dict from normalized ATP rankings
name_to_rank_points = dict(zip(atp_rankings['player_name'], atp_rankings['rank_points']))

# Step 2: Define fuzzy matching function
def get_best_rank_points(name):
    match, score, _ = process.extractOne(name, name_to_rank_points.keys(), scorer=fuzz.token_sort_ratio)
    return name_to_rank_points[match] if score >= 90 else None

# Step 3: Apply only to missing values
missing_mask = player_stats_df['rank_points'].isna()
player_stats_df.loc[missing_mask, 'rank_points'] = player_stats_df.loc[missing_mask, 'name'].apply(get_best_rank_points)

print("Missing rank_points:", player_stats_df['rank_points'].isna().sum())
print(player_stats_df[player_stats_df['rank_points'].isna()].head())

# === MATCHES DataFrame ===

# Add unordered player pair key
players_and_odds['players_key'] = players_and_odds.apply(
    lambda row: frozenset([row['player1_name'], row['player2_name']]), axis=1)
tournament_and_surface['players_key'] = tournament_and_surface.apply(
    lambda row: frozenset([row['player1'], row['player2']]), axis=1)

# Rename the 'status' column before merging
tournament_and_surface = tournament_and_surface.rename(columns={"status": "match_status"})

# Merge on player pair + date
matches_df = pd.merge(
    players_and_odds,
    tournament_and_surface,
    how='inner',
    left_on=['match_date', 'players_key'],
    right_on=['date', 'players_key']
)

# Resolve duplicate match_status columns
if "match_status_x" in matches_df.columns and "match_status_y" in matches_df.columns:
    # Assume match_status_y (from tournament_and_surface) is the correct one
    matches_df["match_status"] = matches_df["match_status_y"]
    matches_df.drop(columns=["match_status_x", "match_status_y"], inplace=True)
elif "match_status_x" in matches_df.columns:
    matches_df.rename(columns={"match_status_x": "match_status"}, inplace=True)
elif "match_status_y" in matches_df.columns:
    matches_df.rename(columns={"match_status_y": "match_status"}, inplace=True)

print(matches_df.head(1))

# Drop helper columns
matches_df.drop(columns=['player1', 'player2', 'time', 'players_key'], inplace=True)

# Drop helper columns (only drop ones that exist)
#matches_df.drop(columns=[col for col in ['player1', 'player2', 'time', 'players_key'] if col in matches_df.columns],
#                inplace=True)

# Check if 'match_status' made it to the merged DataFrame
print("🧪 Columns after merge:", matches_df.columns.tolist())

# Final formatting
match_df = matches_df.rename(columns={
    'player1_name': 'player1_name',
    'player2_name': 'player2_name',
    'surface': 'surface',
    'date': 'date',
    'tournament': 'tournament',
    'player1_odds': 'player1_odds',
    'player2_odds': 'player2_odds',
    'status_1': 'status1',
    'status_2': 'status2',
    'player1_score': 'player1_score',
    'player2_score': 'player2_score',
    'match_status': 'match_status'
})[['player1_name', 'player2_name', 'surface', 'date', 'tournament',
     'status1', 'status2', 'match_status', 'player1_odds', 'player2_odds',
     'player1_score', 'player2_score']]

# === Save Outputs ===
output_path = resolve_path("SCRIPTS_OUTPUT_DIR")
players_output_csv_path = os.path.join(output_path, "players.csv")
player_stats_output_csv_path = os.path.join(output_path, "player_stats.csv")
match_output_csv_path = os.path.join(output_path, "matches.csv")

player_df.to_csv(players_output_csv_path, index=False)
player_stats_df.to_csv(player_stats_output_csv_path, index=False)
match_df.to_csv(match_output_csv_path, index=False)

# === Preview ===
print("✅ Players:\n", player_df.head(), "\n")
print("✅ Player Stats:\n", player_stats_df.head(), "\n")
print("✅ Matches:\n", match_df.head(), "\n")
