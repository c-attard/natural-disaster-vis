import pandas as pd

disasters = pd.read_excel("datasets/public_emdat_custom_request_2025-09-30_3e1debe8-7ea5-4b05-9973-cced1e8c63d6.xlsx")

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

disasters.to_excel("preprocessed_disasters.xlsx", index = False)