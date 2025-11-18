import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

# Load pre-processed data
city_locations = pd.read_excel("preprocessed_locations.xlsx", sheet_name = 'cities')
state_locations = pd.read_excel("preprocessed_locations.xlsx", sheet_name = 'states')
country_locations = pd.read_excel("preprocessed_locations.xlsx", sheet_name = 'countries')
disasters = pd.read_excel("preprocessed_disasters.xlsx")

country_index = disasters.columns.get_loc("Country") + 1
location_index = disasters.columns.get_loc("Location") + 1
latitude_index = disasters.columns.get_loc("Latitude") + 1

for r in disasters.itertuples(index = True):
    if pd.isna(disasters.at[r.Index, 'Latitude']):
        try:
            match r[country_index]:
                case "Czechia":
                    country = "Czech Republic"
                    idx = country_locations[country_locations["name"] == country].index
                case "Eswatini":
                    country = "Swaziland"
                    idx = country_locations[country_locations["name"] == country].index
                case "China, Macao Special Administrative Region":
                    country = "Macau S.A.R."
                    idx = country_locations[country_locations["name"] == country].index
                case "Türkiye":
                    country = "Turkey"
                    idx = country_locations[country_locations["name"] == country].index
                case _:
                    country, score, idx = process.extractOne(r[country_index], country_locations["name"], score_cutoff = 80)
            try: # Find city location
                cities = city_locations[city_locations["country_name"] == country] # Filter cities by country
                city, score, idx = process.extractOne(r[location_index], cities["name"], score_cutoff = 20)
                disasters.at[r.Index, 'Latitude'] = cities.at[idx, 'latitude']
                disasters.at[r.Index, 'Longitude'] = cities.at[idx, 'longitude']
            except:
                try: # Find state location
                    states = state_locations[state_locations["country_name"] == country]
                    state, score, idx = process.extractOne(r[location_index], states["name"], score_cutoff = 20)
                    disasters.at[r.Index, 'Latitude'] = states.at[idx, 'latitude']
                    disasters.at[r.Index, 'Longitude'] = states.at[idx, 'longitude']
                except: # No city or state match, use country instead
                    disasters.at[r.Index, 'Latitude'] = country_locations.at[idx,'latitude']
                    disasters.at[r.Index, 'Longitude'] = country_locations.at[idx, 'longitude']
        except:
            pass


disasters.to_excel("disaster_data.xlsx", index = False)
