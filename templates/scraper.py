import csv

import requests
from bs4 import BeautifulSoup

province = requests.get(
	url="https://en.wikipedia.org/wiki/List_of_municipalities_in_Yukon",
)

soup = BeautifulSoup(province.content, 'html.parser')
links = soup.find(id == "bodyContent").find_all('a')

counter = 0
vcount = 0
list2 = False
provinceList = []
for link in links:
    ref = str(link.string)
    print(ref)
    if ref == 'Carmacks':
        list2 = True
    elif ref == 'Whitehorse' and list2:
        provinceList.append(ref)
        break
    if ref != "None" and ref[0] != '[' and list2:
        provinceList.append(ref)
print(provinceList)
provinces = set(provinceList)
provinceList = sorted(provinces)
print(provinceList)
print(len(provinceList))

with open('YK.csv', 'w' ,newline="", encoding = "utf-8") as f:
    writer = csv.writer(f,quoting=csv.QUOTE_ALL)
    for word in provinceList:
        writer.writerow([word])
