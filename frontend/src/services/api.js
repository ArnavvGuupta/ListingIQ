
const API_BASE= "http://127.0.0.1:8000";

async function fetchJSON(path) {
  const response = await fetch(`${API_BASE}${path}`);

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

export const getSummary = () =>
  fetchJSON("/api/dashboard/summary");

export async function getCities() {
  const response = await fetch(`${API_BASE}/api/dashboard/cities?limit=500`);
  if (!response.ok) throw new Error("Failed to load city report");
  return response.json();
}

export async function getCategories() {
  const response = await fetch(`${API_BASE}/api/dashboard/categories?limit=500`);
  if (!response.ok) throw new Error("Failed to load category report");
  return response.json();
}

export async function getSources() {
  const response = await fetch(`${API_BASE}/api/dashboard/sources?limit=500`);
  if (!response.ok) throw new Error("Failed to load source report");
  return response.json();
}

export const getListings = () =>
  fetchJSON("/api/listings?skip=0&limit=50");
