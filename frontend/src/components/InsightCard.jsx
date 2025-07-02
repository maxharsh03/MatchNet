import React from "react";
import "../styling/InsightCard.css";  // import the CSS file

export default function InsightCard({ insight }) {
  return (
    <div className="insight-card">
      <div className="insight-date-time">
        <div>{insight.date}</div>
        <div>{insight.time}</div>
      </div>

      <div className="insight-player-info">
        <div className="player-name">{insight.player1_name}</div>
        <div>Win Probability: {(insight.probability_player1 * 100).toFixed(1)}%</div>
        <div>Best Line: {insight.best_line_player1 || "-"}</div>
        <div>Best Bookmaker: {insight.best_book_player1 || "-"}</div>
        <div>EV: {insight.ev_player1 ? parseFloat(insight.ev_player1).toFixed(1) : "-"}</div>
        <div>Bet: {insight.bet_on_player1 !== null && insight.bet_on_player1 !== undefined ? (insight.bet_on_player1 ? "Yes" : "No") : "Unknown"}</div>
      </div>
      <div className="insight-player-info">
        <div className="player-name">{insight.player2_name}</div>
        <div>Win Probability: {(insight.probability_player2 * 100).toFixed(1)}%</div>
        <div>Best Line: {insight.best_line_player2 || "-"}</div>
        <div>Best Bookmaker: {insight.best_book_player2 || "-"}</div>
        <div>EV: {insight.ev_player2 ? parseFloat(insight.ev_player2).toFixed(1) : "-"}</div>
        <div>Bet: {insight.bet_on_player2 !== null && insight.bet_on_player2 !== undefined ? (insight.bet_on_player2 ? "Yes" : "No") : "Unknown"}</div>
      </div>
    </div>
  );
}
