import pandas as pd

gdps = pd.read_excel("datasets/mpd2023_web.xlsx", sheet_name = "Full data")
gdps = gdps.drop(["region"], axis = 1) # Remove unneeded columns
gdps = gdps[gdps["year"] >= 2013] # Filter for 2013 and later
gdps["month"] = 1
gdps["day"] = 1
gdps["date"] = pd.to_datetime(gdps[["year", "month", "day"]])


countries = gdps["country"].unique()

resampled_gdps = pd.DataFrame()

for country in countries:
    country_data = gdps[gdps["country"] == country]
    # print(country_data)

    idx = pd.DatetimeIndex(country_data["date"])
    country_data = country_data.set_index(idx)

    gdp_series = country_data["gdppc"]
    pop_series = country_data["pop"]

    gdp_series = gdp_series.resample('D').interpolate()
    pop_series = pop_series.resample('D').interpolate()

    gdp_dict = {"gdppc": gdp_series, "pop": pop_series}

    country_data = pd.DataFrame(gdp_dict)
    country_data["country"] = country
    # countrycode = gdps[gdps["country"] == country]["countrycode"]
    # print(countrycode)
    country_data["countrycode"] = gdps[gdps["country"] == country]["countrycode"].iloc[0]
    country_data["date"] = country_data.index

    resampled_gdps = pd.concat([resampled_gdps, country_data], ignore_index = True)

gdps = resampled_gdps

gdps["Total GDP"] = gdps["gdppc"] * gdps["pop"] # Add column for total GDP

gdps.to_excel("GDP_data.xlsx")