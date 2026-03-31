# CFDB Prototype - Real Data Pipeline

## Project Overview
This prototype demonstrates an end-to-end data pipeline for **Canada's Closed Food Database (CFDB)**.  
It scrapes real product data from Canadian sources, cleans and transforms it using Medallion Architecture (Bronze → Silver → Gold), and performs exploratory data analysis with visualizations.

## 🛠️ Tech Stack
- Python (Requests, BeautifulSoup, Pandas, DuckDB)
- Visualization: Matplotlib, Seaborn, WordCloud
- Jupyter Notebook, Git, GitHub

##  Pipeline Architecture

| Layer | Description | Output |
|-------|-------------|--------|
| Bronze | Raw scraped data (HTML, JSON) | `data/bronze/raw_scrape.json` |
| Silver | Cleaned, deduplicated data | `data/silver/cleaned_data.csv` |
| Gold | Aggregated metrics & visualizations | `data/gold/*.png`, `aggregated_metrics.csv` |

## Visual Results

### Products by Province
<img width="1400" height="617" alt="Screenshot From 2026-03-31 00-08-22" src="https://github.com/user-attachments/assets/9885f2a0-2ec2-49ce-8a94-f38852539674" />


##  How to Run

```bash
git clone https://github.com/saranour700/CFDB_prototype.git
cd CFDB_prototype
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python scraper.py
python pipeline.py
python visualize.py
