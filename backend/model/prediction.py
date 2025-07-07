# load model
import os
from dotenv import load_dotenv
from pathlib import Path
from tensorflow.keras.models import load_model
from sklearn.preprocessing import StandardScaler
import joblib

def prediction(match_df):
    try:
        PROJECT_ROOT = Path(__file__).resolve().parents[1]  # Assumes this script is in `backend/scraping/` or similar

        # Step 2: Load .env from root
        load_dotenv(dotenv_path=PROJECT_ROOT / ".env")

        # Step 3: Resolve all env vars to absolute paths
        def resolve_path(var_name):
            relative_path = os.getenv(var_name)
            if not relative_path:
                raise ValueError(f"{var_name} not found in .env")
            return PROJECT_ROOT / relative_path

        model_path = resolve_path("MODEL_PATH")
        scaler_path = resolve_path("SCALER_PATH")

    except Exception as e:
        print("Error during import or path setup:", e)

    model = load_model(model_path)

    # Select the numeric columns
    numeric_columns = ['player0_rank', 'player1_rank', 'player0_rank_points', 'player1_rank_points', 'rank_diff', 'rank_points_diff']

    # Initialize StandardScaler
    scaler = joblib.load(scaler_path)

    # Scale the numeric columns
    match_df[numeric_columns] = scaler.transform(match_df[numeric_columns])

    predictions = model.predict(match_df)

    # Optional: if it's binary classification, convert to 0/1
    # predicted_classes = (predictions > 0.5).astype(int)

    return predictions
