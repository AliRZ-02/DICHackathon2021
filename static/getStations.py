import csv
import json

names = {}
for i in range (1, 18):
    with open('CLIMATE'+str(i)+'.json') as file:
        data = json.load(file)
        features = data["features"]
        for element in features:
            if element["properties"]["HAS_MONTHLY_SUMMARY"] == "Y":
                names[element["properties"]["STATION_NAME"]] = element["id"]

full = [list(names.keys()), list(names.values())]

# with open('CLIMATE.csv', 'w' ,newline="") as f:
#     writer = csv.writer(f,quoting=csv.QUOTE_ALL)
#     for word in full:
#         for column in word:
#             writer.writerow([column])

print(names)
print(len(names))