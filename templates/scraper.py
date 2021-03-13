import csv

import requests
from bs4 import BeautifulSoup

province = requests.get(
	url="https://en.wikipedia.org/wiki/List_of_municipalities_in_Alberta",
)

soup = BeautifulSoup(province.content, 'html.parser')
links = soup.find(id = "bodyContent").find_all("a")

counter = 0
list2 = False
provinceList = []

for link in links:
    ref = str(link.string)
    if ref == 'Acme' or ref == 'MD of Acadia No. 34':
        list2 = True
        counter += 1
    elif ref == 'Youngstown' or ref == 'Wood Buffalo, Regional Municipality of' and list:
        list2 = False
    elif ref == 'Yellowhead County' and list:
        list2 = False
        break
    elif ref == 'Crowsnest Pass, Municipality of' and counter != 0:
        list = True
    if ref != "None" and ref[0] != '[' and list2:
        provinceList.append(ref)

print(provinceList)
provinces = set(provinceList)
provinceList = sorted(provinces)
print(len(provinceList))

with open('Alberta.csv', 'w' ,newline="", encoding = "utf-8") as f:
    writer = csv.writer(f,quoting=csv.QUOTE_ALL)
    for word in provinceList:
        writer.writerow([word])
