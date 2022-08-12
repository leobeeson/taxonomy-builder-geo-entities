import csv

cities_filepath = "data/cities_in_california.csv"
neighbourhoods = "data/neighbourhoods_by_city.csv"

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


prefix = "Neighborhoods in "
suffix = ", California"


clean_cities = []
for city in cities:
    city = city.removeprefix(prefix)
    city = city[len(suffix)]
