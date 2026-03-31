import pandas as pd
import matplotlib.pyplot as plt
import re

df = pd.read_csv('data/silver/cleaned_data.csv')

print("First 5 rows:")
print(df.head())

print("\nData info:")
print(df.info())

def extract_province(html):
    match = re.search(r'>([^<>]*?(?:Ontario|Quebec|British Columbia|Alberta|Manitoba|Saskatchewan|Nova Scotia|New Brunswick|Newfoundland|PEI|Yukon|Northwest Territories|Nunavut))<', html, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return 'Unknown'

df['province'] = df['raw_html'].apply(extract_province)

print("\nProvince distribution:")
province_counts = df['province'].value_counts()
print(province_counts)

if not province_counts.empty:
    plt.figure(figsize=(10,6))
    province_counts.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Number of Products by Province (from Made in CA)')
    plt.xlabel('Province')
    plt.ylabel('Count')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('data/gold/products_by_province.png')
    print("Saved: data/gold/products_by_province.png")
else:
    print("No province data extracted yet.")

site_counts = df['site'].value_counts()
plt.figure(figsize=(8,5))
site_counts.plot(kind='bar', color='lightgreen', edgecolor='black')
plt.title('Number of Products by Site')
plt.xlabel('Site')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig('data/gold/products_by_site.png')
print("Saved: data/gold/products_by_site.png")

print("\nTop 10 product names:")
print(df['name'].head(10))

plt.show()
