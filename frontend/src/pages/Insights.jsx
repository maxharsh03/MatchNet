import React, { useEffect, useState } from "react";
import InsightCard from "../components/InsightCard";
import Calendar from "../components/Calendar";
import { getInsights } from "../services/api";
import "../styling/InsightCard.css";

export default function Insights() {
  const [insights, setInsights] = useState([]);
  const [selectedDate, setSelectedDate] = useState(new Date());

  useEffect(() => {
    async function fetchInsights() {
      const data = await getInsights();
      setInsights(data);
    }
    fetchInsights();
  }, []);

  const handleDateChange = (newDate) => {
    setSelectedDate(newDate);
  };

  const formatDateForComparison = (date) => {
    return date.toISOString().split('T')[0];
  };

  // Filter by selected date
  const filteredInsights = selectedDate
    ? insights.filter((insight) => insight.date === formatDateForComparison(selectedDate))
    : insights;

  // Group by date for display structure
  const groupedInsights = filteredInsights.reduce((acc, insight) => {
    const key = insight.date || "Unknown Date";
    if (!acc[key]) acc[key] = [];
    acc[key].push(insight);
    return acc;
  }, {});

  const dateGroups = Object.entries(groupedInsights);

  return (
    <div className="insight-container">
      <Calendar 
        selectedDate={selectedDate}
        onDateChange={handleDateChange}
      />

      {dateGroups.length === 0 ? (
        <p className="no-insights">No insights available.</p>
      ) : (
        dateGroups.map(([dateLabel, insightsOnDate]) => (
          <div key={dateLabel} className="insight-date-group">
            {insightsOnDate.map((insight, idx) => (
              <InsightCard key={idx} insight={insight} />
            ))}
          </div>
        ))
      )}
    </div>
  );
}
