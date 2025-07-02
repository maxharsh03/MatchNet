export default function PlayerStatsTable({ players }) {
  console.log("Rendering table for players:", players);
  return (
    <div className="table-container">
      <table>
        <thead>
          <tr>
            <th>Elo Rank</th>
            <th>Name</th>
            <th>ATP Rank</th>
            <th>Age</th>
            <th>Elo</th>
            <th>Elo Rank</th>
            <th>Hard Elo</th>
            <th>Hard Elo Rank</th>
            <th>Clay Elo</th>
            <th>Clay Elo Rank</th>
            <th>Grass Elo</th>
            <th>Grass Elo Rank</th>
            <th>Peak Elo</th>
            <th>Peak Month</th>
            <th>ATP Rank Points</th>
          </tr>
        </thead>
        <tbody>
          {players.map((p, idx) => (
            <tr key={idx}>
              <td>{idx + 1}</td>
              <td>{p.name}</td>
              <td>{p.atp_rank}</td>
              <td>{p.age}</td>
              <td>{p.elo}</td>
              <td>{p.elo_rank}</td>
              <td>{p.hElo}</td>
              <td>{p.hElo_rank}</td>
              <td>{p.cElo}</td>
              <td>{p.cElo_rank}</td>
              <td>{p.gElo}</td>
              <td>{p.gElo_rank}</td>
              <td>{p.peak_elo}</td>
              <td>{p.peak_month}</td>
              <td>{p.rank_points}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
