import json
import os
import pandas as pd

all_items = []

# 1. بيانات Cloudflare
cf_file = 'data/bronze/cloudflare_all_sites.json'
if os.path.exists(cf_file):
    with open(cf_file) as f:
        cf_data = json.load(f)
    for site, content in cf_data.items():
        for selector in content.get('data', []):
            for item in selector.get('results', []):
                text = item.get('text', '') or item.get('innerText', '')
                html = item.get('html', '') or item.get('outerHTML', '')
                if text and text.strip():
                    all_items.append({
                        'source': f'cloudflare_{site}',
                        'text': text[:500],
                        'html': html[:500] if html else ''
                    })

# 2. بيانات Pydoll (بتنسيق مرن)
pydoll_file = 'data/bronze/pydoll_results.json'
if os.path.exists(pydoll_file):
    with open(pydoll_file) as f:
        pydoll_data = json.load(f)
    
    # لو كانت البيانات قائمة
    if isinstance(pydoll_data, list):
        for idx, item in enumerate(pydoll_data):
            if isinstance(item, dict):
                text = item.get('text', '') or item.get('innerText', '') or str(item)
                html = item.get('html', '') or item.get('outerHTML', '')
            elif isinstance(item, str):
                text = item
                html = ''
            else:
                text = str(item)
                html = ''
            
            if text and text.strip():
                all_items.append({
                    'source': f'pydoll_{idx}',
                    'text': text[:500],
                    'html': html[:500] if html else ''
                })
    # لو كانت البيانات dict
    elif isinstance(pydoll_data, dict):
        for key, value in pydoll_data.items():
            text = str(value)[:500]
            if text.strip():
                all_items.append({
                    'source': f'pydoll_{key}',
                    'text': text,
                    'html': ''
                })

# 3. البيانات الأصلية من madeinca (silver)
silver_file = 'data/silver/cleaned_data.csv'
if os.path.exists(silver_file):
    df_old = pd.read_csv(silver_file)
    for _, row in df_old.iterrows():
        text = row.get('name', '') or row.get('text', '')
        if text and str(text).strip():
            all_items.append({
                'source': row.get('site', 'madeinca_original'),
                'text': str(text)[:500],
                'html': str(row.get('raw_html', ''))[:500]
            })

# حفظ الكل
if all_items:
    df_all = pd.DataFrame(all_items)
    df_all = df_all.drop_duplicates(subset=['source', 'text'])
    os.makedirs('data/silver', exist_ok=True)
    df_all.to_csv('data/silver/cleaned_data.csv', index=False)
    print(f"✅ Merged all data: {len(df_all)} unique items")
    print("\n📊 Sources breakdown:")
    print(df_all['source'].value_counts())
    
    # Gold Layer
    gold_summary = df_all.groupby('source').size().reset_index(name='product_count')
    os.makedirs('data/gold', exist_ok=True)
    gold_summary.to_csv('data/gold/aggregated_metrics.csv', index=False)
    print("\n📈 Gold summary saved.")
else:
    print("⚠️ No data found to merge")
