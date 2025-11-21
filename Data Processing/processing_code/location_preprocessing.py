import pandas as pd

def process_locations(city_file, state_file, country_file, output_file):

    city_locations = pd.read_csv(city_file)
    state_locations = pd.read_csv(state_file)
    country_locations = pd.read_csv(country_file)

    city_locations = city_locations[["name", "country_name", "latitude", "longitude"]]
    state_locations =state_locations[["name", "country_name", "latitude", "longitude"]]
    country_locations = country_locations[["name", "latitude", "longitude"]]


    with pd.ExcelWriter(output_file) as writer:
        city_locations.to_excel(writer, sheet_name = 'cities', index = False)
        state_locations.to_excel(writer, sheet_name = 'states', index = False)
        country_locations.to_excel(writer, sheet_name = 'countries', index = False)