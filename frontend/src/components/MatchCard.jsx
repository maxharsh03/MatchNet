import "../styling/MatchCard.css"

export default function MatchCard({ match }) {
    const {
      player1_name,
      player2_name,
      status2,
      match_status,
      player1_odds,
      player2_odds,
      player1_score,
      player2_score,
    } = match;
  
    const formatOdds = (odds) =>
      odds !== null && odds !== undefined ? `${odds > 0 ? "" : ""}${odds}` : "-";
  
    const sportsbookLabels = [
      "Opening Line",
      "Caesar's Sportsbook",
      "bet365",
      "BetMGM",
      "Bet Rivers",
      "Sugar House",
      "Fanduel Sportsbook",
    ];
  
    return (
      <div className="match-card">
        {/* Header Row */}
        <div className="match-card-header">
          <div>{match_status}</div>
          <div>
            {match_status === "SCHEDULED"
                ? status2
                : match_status === "LIVE"
                ? status2
                : match_status === "FINISHED"
                ? "Score"
                : ""}
            </div>
          {sportsbookLabels.map((label, i) => (
            <div key={i}>{label}</div>
          ))}
        </div>
  
        {/* Player 1 Row */}
        <div className="match-card-row">
        <div className="player-name">{player1_name}</div>
        <div className="player-score">
            {player1_score !== null && player1_score !== undefined
            ? player1_score
            : "-"}
        </div>
        {player1_odds.slice(0, 7).map((odds, i) => (
            <div key={i} className="odds-cell">
            {formatOdds(odds)}
            </div>
        ))}
        </div>
  
        {/* Player 2 Row */}
        <div className="match-card-row">
        <div className="player-name">{player2_name}</div>
          <div className="player-score">
            {player2_score !== null && player2_score !== undefined
              ? player2_score
              : "-"}
          </div>
          {player2_odds.slice(0, 7).map((odds, i) => (
            <div key={i} className="odds-cell">
              {formatOdds(odds)}
            </div>
          ))}
        </div>
      </div>
    );
  }
