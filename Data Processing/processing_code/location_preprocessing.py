import pandas as pd

city_locations = pd.read_csv("datasets/cities.csv")
state_locations = pd.read_csv("datasets/states.csv")
country_locations = pd.read_csv("datasets/countries.csv")

city_locations = city_locations[["name", "country_name", "latitude", "longitude"]]
state_locations =state_locations[["name", "country_name", "latitude", "longitude"]]
country_locations = country_locations[["name", "latitude", "longitude"]]


with pd.ExcelWriter("preprocessed_locations.xlsx") as writer:
    city_locations.to_excel(writer, sheet_name = 'cities', index = False)
    state_locations.to_excel(writer, sheet_name = 'states', index = False)
    country_locations.to_excel(writer, sheet_name = 'countries', index = False)