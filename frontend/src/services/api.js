// base url for testing locally
const BASE_URL = "http://localhost:8000/api"; // change to your backend base URL

// 🧠 GET: Player Stats (GET /player-stats)
export async function getPlayerStats() {
  try {
    const res = await fetch(`${BASE_URL}/player-stats/`);
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
    const res = await fetch(`${BASE_URL}/matches/`);
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
    const res = await fetch(`${BASE_URL}/insights/`);
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
    const response = await fetch(`${BASE_URL}/trigger-pipeline/`, {
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
