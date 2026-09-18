const API_BASE_URL = import.meta.env.VITE_API_URL || "/api";

export async function generateCampaign(form) {
  const response = await fetch(`${API_BASE_URL}/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(form),
  });

  let data;

  try {
    data = await response.json();
  } catch {
    throw new Error("The server returned an invalid response.");
  }

  if (!response.ok) {
    throw new Error(data.error || "Campaign generation failed.");
  }

  return data;
}