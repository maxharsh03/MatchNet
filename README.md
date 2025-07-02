# 🎾 MatchNet

**MatchNet** is an intelligent tennis betting assistant that combines 20+ years of match history with real-time data to generate win probabilities, compute expected values, and recommend profitable bets based on odds across multiple bookmakers.

## 🚀 Overview

MatchNet leverages:
- Historical ATP data from Jeff Sackman's open-source database
- Live match scraping via automated pipelines
- Machine learning predictions using player and match metadata
- Expected value (EV) analysis using bookmaker odds
- A full-stack architecture to display betting insights via a modern web UI

---

## 📊 Machine Learning Pipeline

### 🧠 Data Acquisition

- 20+ years of ATP tennis match results were downloaded from [Jeff Sackman's Tennis Data repository](https://github.com/JeffSackmann/tennis_atp).
- CSV files were concatenated, cleaned, and unified into a single dataset of historical match records.

### 🧼 Data Cleaning & Feature Engineering

- Null values were removed or imputed.
- Player rankings and points were matched from yearly rank files.
- Features engineered include:
  - `player_rank`
  - `player_rank_points`
  - `rank_diff`
  - `rank_points_diff`
  - `surface` (encoded numerically)

### 🤖 Model Training

Multiple models were trained and compared:
- ✅ Logistic Regression
- ✅ Random Forest Classifier
- ✅ Shallow Neural Network
- ✅ Deep Neural Network

#### 🔍 Hyperparameter Tuning
- Grid search was used to tune hyperparameters for all models.
- Final model: **Shallow Neural Network**, selected for its performance and generalizability.

#### 🎯 Performance
- **Training Accuracy**: ~66%
- The model outputs win probabilities from the perspective of **player 0** (consistent with training labels).

---

## 🔄 Live Data Pipeline

A robust scraping pipeline was implemented using **Playwright** to:
- Extract **live**, **scheduled**, and **finished** match data
- Aggregate player rankings, odds from multiple bookmakers, and match metadata
- Normalize and structure this data for inference

### 🔗 Sources
- Flashscore (for live match updates and tournament metadata)
- Betting aggregators for real-time bookmaker odds (e.g., BetMGM, Fanduel, bet365)

---

## 💸 Betting Insight Engine

MatchNet computes:

- ✅ Win Probabilities
- ✅ Best Odds (per player across books)
- ✅ Expected Value (EV) per bet
- ✅ Bet Recommendation (based on positive EV)

Using a unit bet size of **$10**, EV is calculated using:
- EV = (probability * payout) - (1 - probability) * unit

Where:
- `payout = (odds / 100) * unit` (for underdog positive odds)
- Odds are compared across multiple bookmakers

---

## 🖥️ Frontend

The frontend is built in **React**, rendering components such as:
- Match cards
- Player stats
- Live insights
- Betting recommendations

Insights include:
- Players
- Surface & tournament
- Win probabilities
- Best odds + EV
- Bookmaker
- Whether to place a bet

---

## ⚙️ Deployment Plan

- **Frontend** → [Amazon S3](https://aws.amazon.com/s3/) (static hosting)
- **Backend (FastAPI)** → [EC2](https://aws.amazon.com/ec2/) with automatic deployment using GitHub Actions
- **Cron Job** → Scheduled job on EC2 to run the full scraping + prediction pipeline
- **MongoDB** → Cloud database used for persistent storage

---

## 🗂️ Directory Structure

MatchNet/
├── backend/ # FastAPI app + API routes
│ ├── app/
│ ├── models/
│ ├── routers/
│ ├── scraping/ # Playwright scripts
| ├── scripts/ # Data processing + orchestration
| ├── betting/ # EV calculation + odds comparison
| ├── model/ # Trained ML model + scaler
├── frontend/ # React app
├── data/ # Processed match and player data
├── notebooks/ # EDA, training, and tuning notebooks
├── .env # Environment variables
└── README.md
