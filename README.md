
# CFDB Prototype – Canadian Closed Food Database

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

A complete end‑to‑end prototype for **Canada’s Closed Food Database (CFDB)**.  
It scrapes real product data from Canadian sources, applies a Medallion pipeline (Bronze → Silver → Gold), and performs exploratory data analysis with visualizations.

## Project Overview

This project demonstrates how to build a reliable data pipeline for Canadian food products.  
It combines multiple scraping techniques:
- **Requests + BeautifulSoup** – static sites  
- **Cloudflare Browser Rendering API** – dynamic pages, one‑call crawling  
- **Pydoll** – async automation via Chrome DevTools Protocol (no WebDriver)  

The collected data is then cleaned, integrated, and analysed to produce insights about Canadian‑made products.

##  Tech Stack

- **Scraping**: `requests`, `beautifulsoup4`, `pydoll`, `cloudflare` API  
- **Data Processing**: `pandas`, `duckdb`  
- **Visualisation**: `matplotlib`, `seaborn`, `wordcloud`  
- **Environment**: Python 3.13, Jupyter Notebook, Git, GitHub  

##  Repository Structure
CFDB_prototype/
├── scraper.py # Basic scraping with requests + BS4
├── cloudflare_scraper.py # Uses Cloudflare /scrape endpoint
├── pydoll_scraper_fixed.py # Async scraping with Pydoll
├── collect_all_data.py # Merges data from all sources
├── pipeline.py # Bronze → Silver → Gold transformation
├── eda_analysis.py # Full EDA script (can be run as .py)
├── cfdb_final_eda.ipynb # Interactive EDA notebook
├── requirements.txt # All dependencies
├── data/
│ ├── bronze/ # Raw scraped data (ignored by Git)
│ ├── silver/
│ │ └── cleaned_data.csv # Cleaned and merged dataset (465 products)
│ └── gold/
│ ├── aggregated_metrics.csv # Summary per source
│ ├── final_summary.csv # Final gold metrics
│ └── *.png # Visualisations
├── README.md
└── .gitignore


##  Medallion Pipeline (Bronze → Silver → Gold)

| Layer | Description | Output |
|-------|-------------|--------|
| **Bronze** | Raw data from each scraper (JSON) | `data/bronze/*.json` |
| **Silver** | Cleaned, deduplicated, merged data | `data/silver/cleaned_data.csv` |
| **Gold** | Aggregated metrics & visualisations | `data/gold/*.csv`, `*.png` |

## Data Summary

After merging all sources, we obtained **465 unique Canadian product entries**.

| Source | Count |
|--------|-------|
| Cloudflare (Made in CA) | 461 |
| Original madeinca.ca (requests) | 2 |
| Pydoll (Made in CA) | 2 |

### Visualisations (saved in `data/gold/`)

| Chart | Description |
|-------|-------------|
| `source_distribution.png` | Number of products per data source |
| `top_brands.png` | Most frequent brand guesses |
| `text_length_dist.png` | Distribution of description length |
| `category_mentions.png` | Keyword‑based product categories |
| `wordcloud.png` | Common words in product descriptions |

## How to Run

1. **Clone the repository**  
   ```bash
   git clone https://github.com/saranour700/CFDB_prototype.git
   cd CFDB_prototype
