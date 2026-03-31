import asyncio
import json
import os
from pydoll.browser import Chrome

async def scrape_with_pydoll(url, selectors):
    print(f"🚀 Starting Pydoll for: {url}")
    
    async with Chrome() as browser:
        tab = await browser.start()
        await tab.go_to(url)
        await asyncio.sleep(5)
        
        js_code = f"""
        () => {{
            const selectors = {selectors};
            let elements = [];
            for (let sel of selectors) {{
                const found = document.querySelectorAll(sel);
                if (found.length > 0) {{
                    elements = found;
                    break;
                }}
            }}
            const results = [];
            for (let i = 0; i < Math.min(elements.length, 15); i++) {{
                const el = elements[i];
                results.push({{
                    text: el.innerText?.substring(0, 500) || '',
                    html: el.outerHTML?.substring(0, 500) || ''
                }});
            }}
            return results;
        }}
        """
        
        try:
            products_data = await tab.execute_script(js_code)
            print(f"✅ Extracted {len(products_data)} elements")
            return products_data
        except Exception as e:
            print(f"⚠️ Error: {e}")
            return []

async def main():
    url = "https://madeinca.ca/grocery-store-guide/"
    selectors = ["table tr", ".product", ".item", "ul li"]  # أكثر من محدد
    
    print("="*50)
    print("Testing Pydoll on Made in CA Grocery Guide")
    print("="*50)
    
    data = await scrape_with_pydoll(url, selectors)
    
    os.makedirs('data/bronze', exist_ok=True)
    output_path = 'data/bronze/pydoll_results.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Saved {len(data)} items to {output_path}")
    
    # عرض أول عنصر بشكل آمن
    if data and isinstance(data, list) and len(data) > 0:
        print("\n📋 First item preview:")
        first_item = data[0]
        if isinstance(first_item, dict):
            print("Text:", first_item.get('text', '')[:200])
            print("HTML:", first_item.get('html', '')[:200])
        else:
            print("Data format:", type(first_item))
            print(first_item[:200] if isinstance(first_item, str) else first_item)
    else:
        print("⚠️ No data to preview")

if __name__ == "__main__":
    asyncio.run(main())
