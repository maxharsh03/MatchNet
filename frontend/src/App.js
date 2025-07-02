import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import News from "./pages/News";
import PlayerStats from "./pages/PlayerStats";
import Matches from "./pages/Matches";
import Insights from "./pages/Insights";
import "./styling/index.css";

export default function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/news" element={<News />} />
        <Route path="/player-stats" element={<PlayerStats />} />
        <Route path="/matches" element={<Matches />} />
        <Route path="/insights" element={<Insights />} />
      </Routes>
    </Router>
  );
}
