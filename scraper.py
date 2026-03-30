import requests
from bs4 import BeautifulSoup
import json
import os
import time

def scrape_made_in_ca():
    url = "https://madeinca.ca/grocery-store-guide/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    print(f"Fetching {url} ...")
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    products = []
    table = soup.find('table')
    
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skipping the header row
            cols = row.find_all('td')
            if len(cols) >= 2:
                brand = cols[0].get_text(strip=True)
                product_desc = cols[1].get_text(strip=True)
                if brand and product_desc:
                    products.append({
                        'site': 'Made_in_CA_Grocery_Guide',
                        'name': f"{brand} - {product_desc[:100]}",
                        'raw_html': str(row)[:500]
                    })
    
    if not products:
        products.append({
            'site': 'Made_in_CA_Grocery_Guide',
            'name': 'No_data_found',
            'raw_html': soup.get_text()[:1000]
        })
    
    print(f"Extracted {len(products)} products from Made in CA")
    return products

def main():
    all_data = []
    
    # Scraping Made in CA
    made_in_ca_data = scrape_made_in_ca()
    all_data.extend(made_in_ca_data)
    
    # Saving to bronze layer
    os.makedirs('data/bronze', exist_ok=True)
    with open('data/bronze/raw_scrape.json', 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)
    
    print(f"Total saved {len(all_data)} items to data/bronze/raw_scrape.json")

if __name__ == '__main__':
    main()
