import { useEffect, useState } from "react";
import PlayerStatsTable from "../components/PlayerStatsTable";
import { getPlayerStats } from "../services/api";
import "../styling/PlayerStatsTable.css"

export default function PlayerStats() {
  const [playerStats, setPlayerStats] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchStats = async () => {
      const data = await getPlayerStats();

      const playerArray = Object.values(data);
      console.log("Player array:", playerArray);

      // console.log(data);
      setPlayerStats(data);
      setLoading(false);
    };

    fetchStats();
  }, []);

  if (loading) return <div className="p-4 text-lg">Loading player stats...</div>;
  if (playerStats.length === 0) return <div className="p-4 text-lg">No player stats available.</div>;

  return (
    <div className="p-4">
      <h1 className="text-2xl font-semibold mb-4" style={{ textAlign: "center" }}>
        Player Stats
      </h1>
      <p className="text-center text-gray-600 mb-6" style={{ textAlign: "center" }}>
        Display of player stats including overall elo, elo across surfaces, age, and atp rank/points.
      </p>
        <PlayerStatsTable players={playerStats} />
    </div>
  );
};
