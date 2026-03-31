import requests
import json
import time
import os

# بيانات حساب Cloudflare
ACCOUNT_ID = "828dbb69a1801a4ced3c4ade5a373c7e"
API_TOKEN = "cfut_ijC4ut61p9MjfkUjusOoavIBixtrW3CDYQhSEf5a17ce44bc"

def scrape_with_cloudflare(url, selectors, wait_for="networkidle0"):
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "url": url,
        "elements": [{"selector": sel} for sel in selectors],
        "gotoOptions": {
            "waitUntil": wait_for
        }
    }
    
    print(f"🚀 Scraping: {url}")
    
    try:
        response = requests.post(
            f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/browser-rendering/scrape",
            headers=headers,
            json=payload,
            timeout=60
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return None
        
        result = response.json()
        
        if not result.get("success"):
            print(f"❌ API Error: {result.get('errors')}")
            return None
        
        print(f"✅ Success! Found {len(result['result'])} selectors with data")
        return result["result"]
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

# ============================================
# قائمة المواقع والـ selectors الخاصة بكل موقع
# ============================================

sites_config = {
    "Made_in_CA_Grocery_Guide": {
        "url": "https://madeinca.ca/grocery-store-guide/",
        "selectors": ["table tr"]
    },
    "Aliments_du_Quebec": {
        "url": "https://www.alimentsduquebec.com/fr/produits",
        "selectors": [".product-item", ".product-title"]
    }
}

def scrape_all_sites():
    all_results = {}
    
    for site_name, config in sites_config.items():
        print("\n" + "="*50)
        print(f"📁 Scraping: {site_name}")
        print("="*50)
        
        results = scrape_with_cloudflare(
            config["url"],
            config["selectors"],
            wait_for="networkidle0"
        )
        
        if results:
            all_results[site_name] = {
                "url": config["url"],
                "data": results,
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
        else:
            print(f"⚠️ Skipping {site_name} - no data")
        
        time.sleep(2)
    
    os.makedirs('data/bronze', exist_ok=True)
    output_file = 'data/bronze/cloudflare_all_sites.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    
    print("\n" + "="*50)
    print(f"💾 Results saved to: {output_file}")
    print(f"📊 Sites scraped: {len(all_results)}")
    
    return all_results

if __name__ == "__main__":
    print("🚀 Starting Cloudflare Scraper for CFDB")
    results = scrape_all_sites()
