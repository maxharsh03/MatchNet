def american_to_decimal(odds):
    if odds > 0:
        return (odds / 100) + 1
    elif odds < 0:
        return (100 / abs(odds)) + 1
    else:
        return None  # 0 is invalid for betting odds

def expected_value(bet_size, decimal_odds, win_prob):
    return bet_size * (win_prob * (decimal_odds - 1) - (1 - win_prob))

def compute_ev_and_suggestion_with_bookmaker(bet_size, odds_list, win_prob):
    sportsbooks = [
        "Caesars Sportsbook",
        "bet365",
        "BetMGM",
        "Bet Rivers",
        "Sugar House",
        "Fanduel Sportsbook"
    ]

    best_ev = float('-inf')
    best_data = None

    for i, raw in enumerate(odds_list[1:], start=1):  # Skip index 0 (opening line)
        try:
            val = int(raw)
            dec_odds = american_to_decimal(val)
            if dec_odds is None:
                continue
            ev = expected_value(bet_size, dec_odds, win_prob)
            if ev > best_ev:
                best_ev = ev
                best_data = (val, sportsbooks[i - 1], ev)
        except (ValueError, TypeError, IndexError):
            continue

    if best_data is None:
        return None, None, None, None

    best_odds, best_sportsbook, ev = best_data
    recommend = ev > 0

    return best_odds, best_sportsbook, round(ev, 3), recommend
