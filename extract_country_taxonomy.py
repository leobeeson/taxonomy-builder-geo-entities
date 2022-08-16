import csv
import json
import re
from re import Pattern


countries_filepath = "data/wikipedia_geographic_names_adjectives_and_demonyms.csv"

pattern_control_chars: Pattern = re.compile("\xa0|\xad")

def remove_undesirable_chars(text: str) -> str:
    minus_unnecessary_spaces = re.sub("\s+", " ", text)
    minus_control_chars = re.sub(pattern_control_chars, "", minus_unnecessary_spaces)
    return minus_control_chars


continent = set()
region = set()
country = set()
us_state = set()
city = set()
continental_adjective = set()
regional_adjective = set()
country_adjective = set()
us_state_adjective = set()
city_adjective = set()
continental_demonym = set()
regional_demonym = set()
country_demonym = set()
us_state_demonym = set()
city_demonym = set()
with open(countries_filepath, "r") as file_input:
    csv_reader = csv.reader(file_input)
    next(csv_reader)
    for row in csv_reader:
        if "," in row[1]:
            names = [remove_undesirable_chars(segment_.strip()) for segment_ in row[1].split(",")]
        else:
            names = [remove_undesirable_chars(row[1].strip())]
        if "," in row[2]:
            adjectives = [remove_undesirable_chars(segment_.strip()) for segment_ in row[2].split(",")]
        else:
            adjectives = [remove_undesirable_chars(row[2].strip())]
        if "," in row[3]:
            demonyms = [remove_undesirable_chars(segment_.strip()) for segment_ in row[3].split(",")]
        else:
            demonyms = [remove_undesirable_chars(row[3].strip())]
        
        if row[0] == "Continent":          
            continent.update(names)
            continental_adjective.update(adjectives)
            continental_demonym.update(demonyms)
        elif row[0] == "Region-US":
            us_state.update(names)
            us_state_adjective.update(adjectives)
            us_state_demonym.update(demonyms)
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

continent.discard("")
region.discard("")
country.discard("")
us_state.discard("")
city.discard("")
continental_adjective.discard("")
regional_adjective.discard("")
country_adjective.discard("")
us_state_adjective.discard("")
city_adjective.discard("")
continental_demonym.discard("")
regional_demonym.discard("")
country_demonym.discard("")
us_state_demonym.discard("")
city_demonym.discard("")

global_geographical_entities = {}
global_geographical_entities["geographical_names"] = {}
global_geographical_entities["geographical_names"]["continent"] = list(continent)
global_geographical_entities["geographical_names"]["region"] = list(region)
global_geographical_entities["geographical_names"]["country"] = list(country)
global_geographical_entities["geographical_names"]["us_state"] = list(us_state)
global_geographical_entities["geographical_names"]["city"] = list(city)
global_geographical_entities["geographical_adjectives"] = {}
global_geographical_entities["geographical_adjectives"]["continent"] = list(continental_adjective)
global_geographical_entities["geographical_adjectives"]["region"] = list(regional_adjective)
global_geographical_entities["geographical_adjectives"]["country"] = list(country_adjective)
global_geographical_entities["geographical_adjectives"]["us_state"] = list(us_state_adjective)
global_geographical_entities["geographical_adjectives"]["city"] = list(city_adjective)
global_geographical_entities["geographical_demonyms"] = {}
global_geographical_entities["geographical_demonyms"]["continent"] = list(continental_demonym)
global_geographical_entities["geographical_demonyms"]["region"] = list(regional_demonym)
global_geographical_entities["geographical_demonyms"]["country"] = list(country_demonym)
global_geographical_entities["geographical_demonyms"]["us_state"] = list(us_state_demonym)
global_geographical_entities["geographical_demonyms"]["city"] = list(city_demonym)

with open("data/global_geographical_entities.json", "w") as output_file:
    json.dump(global_geographical_entities, output_file)


test_str = "Amazon river and Amazon region"
remove_undesirable_chars(test_str)
