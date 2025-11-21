import pandas as pd
from fuzzywuzzy import process

def preprocess_disasters(raw_file, output_file):

    disasters = pd.read_excel(raw_file)

    disasters = disasters[["Disaster Subgroup", "Disaster Type", "ISO", "Country", "Subregion", "Region", "Location", "Appeal", "Declaration", "Latitude", "Longitude","Start Year", "Start Month", "Start Day", "Total Deaths"]] # Remove unneeded columns
    disasters = disasters[disasters["Start Year"] >= 2013] # Filter for 2013 and later
    disasters = disasters[disasters["Disaster Subgroup"].isin(["Climatological", "Hydrological", "Meteorological"])] # Filter for climate related natural disasters
    disasters = disasters.drop(["Disaster Subgroup"], axis = 1) # Subgroup information no longer required
    disasters = disasters[disasters["Disaster Type"] != "Extreme temperature"] # Remove extreme temperature
    disasters = disasters.dropna(subset = "Total Deaths")
    disasters = disasters.loc[(disasters["Appeal"] == "Yes") | (disasters["Declaration"] == "Yes") | (disasters["Total Deaths"] >= 10)] # Filter for severity
    disasters = disasters.drop(["Appeal", "Declaration"], axis = 1) # Columns no longer required
    disasters["Start Month"] = disasters["Start Month"].fillna(1) # Fill missing start months
    disasters["Start Day"] = disasters["Start Day"].fillna(1) # Fill missing start days
    disasters = disasters.rename(columns = {"Start Year": "year", "Start Month": "month", "Start Day": "day"})
    disasters["Date"] = pd.to_datetime(disasters[["year", "month", "day"]])
    disasters = disasters.drop(["year", "month", "day"], axis = 1) # Separate year, month, day columns no longer required

    disasters.to_excel(output_file, index = False)


def fill_coordinates(disaster_file, location_file, output_file):

    # Load pre-processed data
    city_locations = pd.read_excel(location_file, sheet_name='cities')
    state_locations = pd.read_excel(location_file, sheet_name='states')
    country_locations = pd.read_excel(location_file, sheet_name='countries')
    disasters = pd.read_excel(disaster_file)

    country_index = disasters.columns.get_loc("Country") + 1
    location_index = disasters.columns.get_loc("Location") + 1
    latitude_index = disasters.columns.get_loc("Latitude") + 1

    for r in disasters.itertuples(index=True):
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
                        country, score, idx = process.extractOne(r[country_index], country_locations["name"],
                                                                 score_cutoff=80)
                try:  # Find city location
                    cities = city_locations[city_locations["country_name"] == country]  # Filter cities by country
                    city, score, idx = process.extractOne(r[location_index], cities["name"], score_cutoff=20)
                    disasters.at[r.Index, 'Latitude'] = cities.at[idx, 'latitude']
                    disasters.at[r.Index, 'Longitude'] = cities.at[idx, 'longitude']
                except:
                    try:  # Find state location
                        states = state_locations[state_locations["country_name"] == country]
                        state, score, idx = process.extractOne(r[location_index], states["name"], score_cutoff=20)
                        disasters.at[r.Index, 'Latitude'] = states.at[idx, 'latitude']
                        disasters.at[r.Index, 'Longitude'] = states.at[idx, 'longitude']
                    except:  # No city or state match, use country instead
                        disasters.at[r.Index, 'Latitude'] = country_locations.at[idx, 'latitude']
                        disasters.at[r.Index, 'Longitude'] = country_locations.at[idx, 'longitude']
            except:
                pass

    disasters.to_excel(output_file, index=False)