from collections import defaultdict
import csv
import re
import json

cities_filepath = "data/cities_in_california.csv"
neighbourhoods = "data/neighbourhoods_by_city.csv"

prefix = "Neighborhoods in "
suffix = ", California"


# Get Cities
cities = []
with open(cities_filepath, "r") as file_input:
    csv_reader = csv.reader(file_input)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
            continue
        cities.append(row[1])
        line_count += 1

clean_cities = []
for city in cities:
    city = city.removeprefix(prefix)
    city = city.removesuffix(suffix)
    clean_cities.append(city)

with open("data/cities_in_california.txt", "w") as output_file:
    output_file.write("\n".join(clean_cities))


# Get Neighbourhoods
pattern = re.compile("\s+\(.+\)*.*")
neighbourhoods_per_city = defaultdict(set)
with open(neighbourhoods, "r") as file_input:
    csv_reader = csv.reader(file_input)
    line_count = 0
    for row in csv_reader:
        if line_count == 0 or line_count == 1:
            line_count += 1
            continue
        if "neighborhood" in row[1].lower():
            continue
        city = row[0].removeprefix(prefix)
        city = city.removeprefix(prefix)
        city = city.removesuffix(suffix)
        neighbourhood = row[1]
        neighbourhood = neighbourhood.split(",")[0]
        neighbourhood = pattern.sub("", neighbourhood)
        if "/" in neighbourhood:
            neighbourhoods_split = [n.strip() for n in neighbourhood.split("/")]
            neighbourhoods_per_city[city].update(neighbourhoods_split)
        else:
            neighbourhoods_per_city[city].add(neighbourhood)
        line_count += 1

with open("data/neighbourhoods_by_city_in_california.json", "w") as output_file:
    json.dump(neighbourhoods_per_city, output_file, default=lambda x: list(x) if isinstance(x, set) else x)
