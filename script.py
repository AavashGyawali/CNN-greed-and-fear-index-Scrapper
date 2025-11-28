import requests
import pandas as pd
from datetime import datetime, timezone

# --- Set the start date ---
# Note that it works from 2020-07-14 onwards
START_DATE = "2020-07-14"

# CNN API URL
URL = f"https://production.dataviz.cnn.io/index/fearandgreed/graphdata/{START_DATE}"

# Browser-like headers to avoid 418 errors
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://edition.cnn.com/",
    "Origin": "https://edition.cnn.com",
}

# Fetch the data
resp = requests.get(URL, headers=headers)
resp.raise_for_status()
data = resp.json()

# Extract historical points
hist_data = data.get("fear_and_greed_historical", {}).get("data", [])

# Convert to DataFrame
df = pd.DataFrame([
    {
        "date": pd.to_datetime(datetime.fromtimestamp(item["x"] / 1000, timezone.utc)),
        "value": item["y"],
        "rating": item.get("rating")
    }
    for item in hist_data
])

# Sort by date
df.sort_values("date", inplace=True)

# Save as CSV
df.to_csv("cnn_fear_greed.csv", index=False)

print(f"Saved {len(df)} rows → cnn_fear_greed.csv")
