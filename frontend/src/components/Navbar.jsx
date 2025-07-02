import { Link } from "react-router-dom";
import "../styling/Navbar.css";

export default function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/" className="nav-link">Home</Link>
      <Link to="/news" className="nav-link">News</Link>
      <Link to="/player-stats" className="nav-link">Player Stats</Link>
      <Link to="/matches" className="nav-link">Matches</Link>
      <Link to="/insights" className="nav-link">Insights</Link>
    </nav>
  );
}
