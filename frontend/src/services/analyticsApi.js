
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export async function getJanuaryAnalytics() {
  const response = await fetch(
    `${API_BASE_URL}/api/analytics/january`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch January analytics");
  }

  return response.json();
}

export async function getDailyAnalytics() {
  const response = await fetch(
    `${API_BASE_URL}/api/analytics/january/daily`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch daily analytics");
  }

  return response.json();
}