// base url for testing locally
const BASE_URL = process.env.REACT_APP_API_URL

// 🧠 GET: Player Stats (GET /player-stats)
export async function getPlayerStats() {
  try {
    const res = await fetch(`${BASE_URL}/api/player-stats/`);
    if (!res.ok) throw new Error("Failed to fetch player stats");
    return await res.json();
  } catch (err) {
    console.error(err);
    return [];
  }
}

// 🧠 GET: Matches (GET /matches)
export async function getMatches() {
  try {
    const res = await fetch(`${BASE_URL}/api/matches/`);
    if (!res.ok) throw new Error("Failed to fetch matches");
    return await res.json();
  } catch (err) {
    console.error(err);
    return [];
  }
}

// 🧠 GET: Insights (GET /insights)
export async function getInsights() {
  try {
    const res = await fetch(`${BASE_URL}/api/insights/`);
    if (!res.ok) throw new Error("Failed to fetch insight");
    return await res.json();
  } catch (err) {
    console.error(err);
    return [];
  }
}

// GET: News (GET /news)

// Trigger pipeline (POST /trigger-pipeline)
export async function triggerPipeline() {
  try {
    const response = await fetch(`${BASE_URL}/api/trigger-pipeline/`, {
      method: "POST",
    });

    if (!response.ok) {
      throw new Error("Pipeline trigger failed");
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error triggering pipeline:", error);
    return { error: error.message };
  }
}
