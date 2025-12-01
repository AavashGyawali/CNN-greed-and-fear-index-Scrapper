CNN Fear & Greed Historical Data Scraper
========================================

This repository contains a small Python script that downloads the **historical CNN Fear & Greed Index** data from CNN’s public data API and saves it as a clean CSV file for further analysis in Excel, Python, R, or any other tool.

The script:

- Sends a browser-like HTTP request to CNN’s Fear & Greed endpoint
- Parses the JSON response
- Converts the historical data to a `pandas` DataFrame
- Normalizes timestamps into readable UTC datetimes
- Saves the result as `cnn_fear_greed.csv`

---

## Project Structure

- `script.py` – Main script that calls the CNN API and saves the data to CSV.
- `requirements.txt` – Python package dependencies needed to run the script.
- `venv/` – (Optional) Local virtual environment directory (can be recreated; usually not committed to GitHub).

---

## Data Source

The script uses CNN’s public data endpoint for the Fear & Greed Index:

- Base URL pattern:  
  `https://production.dataviz.cnn.io/index/fearandgreed/graphdata/<START_DATE>`
- In this project, `START_DATE` is configured in `script.py` as:
  - `START_DATE = "2020-07-14"`
- The endpoint returns JSON that includes a `fear_and_greed_historical.data` array with timestamp (ms since epoch), index value, and rating.

> **Note**: CNN may change or restrict this endpoint at any time. This project is purely for educational and analytical purposes.

---

## Requirements

- **Python**: 3.12 (or any reasonably modern Python 3 version)
- **OS**: Linux, macOS, or Windows
- **Packages**:
  - `requests`
  - `pandas`
  - (and transitive dependencies listed in `requirements.txt`)

You can see exact, pinned versions in `requirements.txt`.

---

## Quick Start

### 1. Clone the repository

From your terminal:

```bash
git clone https://github.com/AavashGyawali/CNN-greed-and-fear-index-Scrapper.git
cd CNN-greed-and-fear-index-Scrapper

```


### 2. (Optional but recommended) Create and activate a virtual environment

If you don’t already have one:

```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
```

On Windows (PowerShell):

```bash
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

With the virtual environment activated (or in your base Python env, if you prefer):

```bash
pip install -r requirements.txt
```

### 4. Run the script

From the project root:

```bash
python script.py
```

If everything succeeds, you should see output similar to:

```text
Saved <N> rows → cnn_fear_greed.csv
```

And a `cnn_fear_greed.csv` file will be created in the project directory.

---

## Output File

### `cnn_fear_greed.csv`

This CSV contains one row per historical observation from CNN’s Fear & Greed Index endpoint, with the following columns:

- `date` – UTC datetime corresponding to the index timestamp.
- `value` – Numeric Fear & Greed index value.
- `rating` – Text label describing the sentiment, typically something like `"Extreme Fear"`, `"Fear"`, `"Neutral"`, `"Greed"`, `"Extreme Greed"` (depending on CNN’s API).

You can open this CSV in:

- Excel / Google Sheets
- Python (`pandas.read_csv`)
- R (`read.csv`)
- Any BI or charting tool that accepts CSV input

---

## How It Works (Code Overview)

The core logic is in `script.py`:

- **Define the start date**:
  - `START_DATE` is set to `"2020-07-14"`. CNN mentions that historical data is available from that date onward.
- **Build the URL**:
  - `URL = f"https://production.dataviz.cnn.io/index/fearandgreed/graphdata/{START_DATE}"`
- **Set HTTP headers**:
  - Uses a browser-like `User-Agent`, `Accept`, `Referer`, and `Origin` to avoid HTTP 418 / bot-detection errors.
- **Fetch the data**:
  - Uses `requests.get(URL, headers=headers)` and `resp.raise_for_status()` to fail fast on HTTP errors.
- **Parse the JSON**:
  - `resp.json()` gives the full JSON payload.
  - It looks for `data["fear_and_greed_historical"]["data"]`, which is a list of points.
- **Transform to DataFrame**:
  - Each item is mapped to a dict with:
    - `date` – derived by converting the `x` timestamp (in milliseconds) to a UTC-aware `datetime`.
    - `value` – the `y` field.
    - `rating` – optional descriptive label from CNN (`item.get("rating")`).
  - The list of dicts is passed to `pandas.DataFrame`.
  - The DataFrame is sorted ascending by `date`.
- **Save to CSV**:
  - `df.to_csv("cnn_fear_greed.csv", index=False)` writes the file without an index column.
  - A simple print statement reports how many rows were saved.

---

## Configuration & Customization

### Change the start date

If you want to request from a different start date (assuming CNN supports it), open `script.py` and modify:

```python
START_DATE = "2020-07-14"
```

Use the format `YYYY-MM-DD`. Note that CNN may not support dates earlier than `"2020-07-14"`, or the API may behave differently.

### Change the output file name

By default, the output is written as:

```python
df.to_csv("cnn_fear_greed.csv", index=False)
```

Change the file name to anything you prefer, for example:

```python
df.to_csv("data/fear_greed_history.csv", index=False)
```

Make sure the target directory (`data/` in this example) exists.

---

## Error Handling & Troubleshooting

- **HTTP 4xx/5xx errors**:
  - The script uses `resp.raise_for_status()`, which will raise an exception if CNN returns an error status code.
  - Check your network connection and confirm the endpoint is still available.
- **HTTP 418 or bot-related errors**:
  - The script already uses realistic browser headers to reduce this risk.
  - If issues persist, try running again later or adjust headers (e.g., `User-Agent`) cautiously.
- **Empty or missing data**:
  - If `fear_and_greed_historical.data` is missing or empty in the JSON response, the resulting CSV may be empty.
  - In that case, inspect the raw JSON (e.g., `print(data.keys())`) to see if CNN changed the structure.
- **Import errors** (e.g., `ModuleNotFoundError: No module named 'pandas'`):
  - Ensure you have activated your virtual environment and run `pip install -r requirements.txt`.

---

## Best Practices & Notes

- **Virtual environment**:
  - Using a virtual environment (like `venv/`) keeps this project’s dependencies isolated from your global Python installation.
- **Version pinning**:
  - `requirements.txt` pins explicit versions of packages to make runs reproducible.
- **GitHub recommendations**:
  - Typically, you would **not** commit the `venv/` directory to GitHub. Instead, add it to `.gitignore` and let users recreate it using `requirements.txt`.

---

## Extending the Project

Once you have the CSV, here are a few ideas for extending this project:

- **Visualization**:
  - Use `matplotlib`, `seaborn`, or `plotly` to plot the Fear & Greed Index over time.
- **Statistical analysis**:
  - Combine this dataset with stock market indices (e.g., S&P 500) to study relationships between sentiment and market movements.
- **Automation**:
  - Schedule the script to run daily with `cron` (Linux/macOS) or Task Scheduler (Windows) to keep a local archive up to date.

---

## License

This project is licensed under the **MIT License**.

- See the `LICENSE` file in the repository root for the full license text.
- You are free to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of this software, subject to the terms of the MIT License.
- Although the project was created with the help of AI tools, you (the repository owner) hold the copyright
  to the resulting code and configuration, and you are offering it under the MIT terms.

---

## Disclaimer

This project is **not affiliated with, endorsed, or sponsored by CNN**.  
Use this script and the resulting data responsibly and in accordance with CNN’s terms of use and any applicable laws.


