import React, { useEffect, useState } from "react";
import MatchCard from "../components/MatchCard";
import Calendar from "../components/Calendar";
import { getMatches } from "../services/api";
import "../styling/MatchCard.css";

export default function Matches() {
  const [matches, setMatches] = useState([]);
  const [filter, setFilter] = useState("ALL");
  const [selectedDate, setSelectedDate] = useState(new Date());
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    async function fetchMatches() {
      if (isLoading) return; // Prevent multiple simultaneous requests
      
      setIsLoading(true);
      try {
        const data = await getMatches();
        setMatches(data);
      } catch (error) {
        console.error("Error fetching matches:", error);
      } finally {
        setIsLoading(false);
      }
    }
    
    fetchMatches();
  }, []); // Only run once on mount

  // Filter by match_status
  let filteredMatches =
    filter === "ALL"
      ? matches
      : matches.filter((m) => m.match_status === filter);

  // Further filter by date if applicable
  const showDatePicker = ["ALL", "SCHEDULED", "FINISHED"].includes(filter);

  if (showDatePicker && selectedDate) {
    // Get date in local timezone to avoid UTC offset issues
    const selectedYear = selectedDate.getFullYear();
    const selectedMonth = selectedDate.getMonth();
    const selectedDay = selectedDate.getDate();
    
    filteredMatches = filteredMatches.filter((m) => {
      if (!m.date) return false;
      const matchDate = new Date(m.date);
      return matchDate.getFullYear() === selectedYear &&
             matchDate.getMonth() === selectedMonth &&
             matchDate.getDate() === selectedDay;
    });
  }

  // Group by tournament
  const groupedMatches = filteredMatches.reduce((acc, match) => {
    const key = `${match.tournament} - ${match.surface}`;
    if (!acc[key]) acc[key] = [];
    acc[key].push(match);
    return acc;
  }, {});

  const tournamentGroups = Object.entries(groupedMatches);

  return (
    <div className="match-card-container">
      <div className="filter-bar">
        <div className="filter-buttons">
          {["ALL", "LIVE", "SCHEDULED", "FINISHED"].map((status) => (
            <button
              key={status}
              className={`filter-button ${filter === status ? "active" : ""}`}
              onClick={() => {
                setFilter(status);
                if (status !== "ALL" && status !== "SCHEDULED" && status !== "FINISHED") {
                  setSelectedDate(null);
                } else {
                  setSelectedDate(new Date());
                }
              }}
            >
              {status}
            </button>
          ))}
        </div>

        {showDatePicker && (
          <Calendar 
            selectedDate={selectedDate} 
            onDateChange={setSelectedDate}
          />
        )}
      </div>

      {/* Match Cards Grouped by Tournament */}
      {tournamentGroups.length === 0 ? (
        <p style={{ color: "white", padding: "1rem" }}>No matches available.</p>
      ) : (
        tournamentGroups.map(([groupLabel, groupMatches]) => (
          <div key={groupLabel} className="tournament-group">
            <div className="tournament-header">{groupLabel}</div>
            {groupMatches.map((match, idx) => (
              <MatchCard key={idx} match={match} />
            ))}
          </div>
        ))
      )}
    </div>
  );
}
