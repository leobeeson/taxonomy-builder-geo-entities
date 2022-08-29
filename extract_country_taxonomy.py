import csv
import json
import re
from re import Pattern


wikipedia_countries_filepath = "data/wikipedia_geographic_names_adjectives_and_demonyms.csv"
california_neighbourhoods_filepath = "data/neighbourhoods_by_city_in_california.json"
california_zip_codes = "data/ZIP_Locale_Detail - ZIP_Codes_CA.csv"
worldcities_filepath = "data/worldcities.csv"

worldcities_city_filter = ["United States", "Mexico"]

pattern_control_chars: Pattern = re.compile("\xa0|\xad")
pattern_contains_suffix_town: Pattern = re.compile("^.+town$")
suffix_town: str = "town"


def remove_undesirable_chars(text: str) -> str:
    minus_unnecessary_spaces = re.sub("\s+", " ", text)
    minus_control_chars = re.sub(pattern_control_chars, "", minus_unnecessary_spaces)
    return minus_control_chars


def expand_suffix(text: str, suffix: str) -> list[str]:
    expansions = set([text])
    if re.search(pattern_contains_suffix_town, text):
        prefix = text.split("town")[0].strip()
        expansions.add(prefix + suffix)
        expansions.add(prefix + " " + suffix)
        expansions.add(prefix + "-" + suffix)
    return list(expansions)


def expand_plural_demonyms(demonyms: list[str]) -> list[str]:
    demonyms_expanded = []
    for demonym in demonyms:
        demonyms_expanded.append(demonym)
        if len(demonym) > 0 and demonym[-1] == "s":
            demonyms_expanded.append(demonym[:-1])
    return demonyms_expanded


def default_pipeline(text: str) -> list[str]:
    keywords = []
    if len(text) > 0:
        if "," in text:
            segments = text.split(",")
        else:
            segments = [text]
        for segment in segments:
            segment = segment.strip()
            segment = remove_undesirable_chars(segment)
            expansions = expand_suffix(segment, suffix_town)
            keywords.extend(expansions)
    return keywords


def demonym_pipeline(text: str) -> list[str]:
    keywords = default_pipeline(text)
    demonyms = expand_plural_demonyms(keywords)
    return demonyms


continent = set()
region = set()
country = set()
state = set()
city = set()
neighbourhood = set()
zip_code = set()
continental_adjective = set()
regional_adjective = set()
country_adjective = set()
state_adjective = set()
city_adjective = set()
neighbourhood_adjective = set()
continental_demonym = set()
regional_demonym = set()
country_demonym = set()
state_demonym = set()
city_demonym = set()
neighbourhood_demonym = set()

# Transform Wikipedia Regions and Countries Data
with open(wikipedia_countries_filepath, "r") as input_file:
    csv_reader = csv.reader(input_file)
    next(csv_reader)
    for row in csv_reader:
        names = default_pipeline(row[1])
        adjectives = default_pipeline(row[2])
        demonyms = demonym_pipeline(row[3])
        if row[0] == "Continent":          
            continent.update(names)
            continental_adjective.update(adjectives)
            continental_demonym.update(demonyms)
        elif row[0] == "Region-US":
            state.update(names)
            state_adjective.update(adjectives)
            state_demonym.update(demonyms)
        elif "Region" in row[0]:
            region.update(names)
            regional_adjective.update(adjectives)
            regional_demonym.update(demonyms)
        elif row[0] == "Country":
            country.update(names)
            country_adjective.update(adjectives)
            country_demonym.update(demonyms)
        elif row[0] == "City":
            city.update(names)
            city_adjective.update(adjectives)
            city_demonym.update(demonyms)


# Transform Wikipedia Data California Neighbourhoods:
with open(california_neighbourhoods_filepath) as input_file:
    neighbourhood_data = json.load(input_file)

for city_name, neighbourhood_names in neighbourhood_data.items():
    city.add(city_name)
    for neighbourhood_name in neighbourhood_names:
        neighbourhood_name = default_pipeline(neighbourhood_name)
        neighbourhood.update(neighbourhood_name)

# Transform Simplemaps WorldCities Data:
with open(worldcities_filepath, "r") as input_file:
    csv_reader = csv.reader(input_file)
    next(csv_reader)
    for row in csv_reader:
        if row[4] == "United States":
            if row[7] == "California":
                city_name = row[1]
                city.add(city_name)
                state_name = row[7]
                state.add(state_name)    
        elif row[4] in worldcities_city_filter:
            city_name = row[1]
            city.add(city_name)
            state_name = row[7]
            state.add(state_name)

# Transform Zip Codes California:
with open(california_zip_codes, "r") as input_file:
    csv_reader = csv.reader(input_file)
    next(csv_reader)
    for row in csv_reader:
        zip_code.add(row[0])


global_geographical_entities = {}
global_geographical_entities["geographical_names"] = {}
global_geographical_entities["geographical_names"]["continent"] = list(continent)
global_geographical_entities["geographical_names"]["region"] = list(region)
global_geographical_entities["geographical_names"]["country"] = list(country)
global_geographical_entities["geographical_names"]["state"] = list(state)
global_geographical_entities["geographical_names"]["city"] = list(city)
global_geographical_entities["geographical_names"]["neighbourhood"] = list(neighbourhood)
global_geographical_entities["geographical_names"]["zip_code"] = list(zip_code)
global_geographical_entities["geographical_adjectives"] = {}
global_geographical_entities["geographical_adjectives"]["continent"] = list(continental_adjective)
global_geographical_entities["geographical_adjectives"]["region"] = list(regional_adjective)
global_geographical_entities["geographical_adjectives"]["country"] = list(country_adjective)
global_geographical_entities["geographical_adjectives"]["state"] = list(state_adjective)
global_geographical_entities["geographical_adjectives"]["city"] = list(city_adjective)
global_geographical_entities["geographical_adjectives"]["neighbourhood"] = list(neighbourhood_adjective)
global_geographical_entities["geographical_demonyms"] = {}
global_geographical_entities["geographical_demonyms"]["continent"] = list(continental_demonym)
global_geographical_entities["geographical_demonyms"]["region"] = list(regional_demonym)
global_geographical_entities["geographical_demonyms"]["country"] = list(country_demonym)
global_geographical_entities["geographical_demonyms"]["state"] = list(state_demonym)
global_geographical_entities["geographical_demonyms"]["city"] = list(city_demonym)
global_geographical_entities["geographical_demonyms"]["neighbourhood"] = list(neighbourhood_demonym)


with open("data/global_geographical_entities.json", "w") as output_file:
    json.dump(global_geographical_entities, output_file)


