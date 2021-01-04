import requests
import pandas as pd
import xmltodict
import sys
from pprint import pprint


if len(sys.argv) < 2:
	print("Need website URL as parameter, i.e. https://google.com")
	sys.exit(1)

url = f"{sys.argv[1]}/sitemap.xml".replace('//s', '/s')
res = requests.get(url)
raw = xmltodict.parse(res.text)

data = [[r["loc"], r["lastmod"]] for r in raw["sitemapindex"]["sitemap"]]
print("Number of sitemaps:", len(data))
df = pd.DataFrame(data, columns=["links", "lastmod"])
print(df.to_string())

for index, row in df.iterrows():
	print(f"### {row['links']} ###")
	u = requests.get(row['links']).text
	doc = xmltodict.parse(u)
	try:
		for d in doc['urlset']['url']:
    			print(f"  {d['loc']} ")
	except:
		print(f"  {doc['urlset']['url']['loc']}")
        
