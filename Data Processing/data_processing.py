# import processing_code.disaster_fuzzy_processing
# import processing_code.disaster_preprocessing
import processing_code.GDP_processing as gdp_proc
import processing_code.location_preprocessing as loc_proc
import processing_code.temperature_processing as temp_proc

# Process global temperature data
temp_proc.process_temps("raw_datasets/HadCRUT.5.0.2.0.analysis.summary_series.global.monthly.csv","final_datasets/temperature_data.xlsx")

# Process disaster data
loc_proc.process_locations("raw_datasets/cities.csv", "raw_datasets/states.csv","raw_datasets/countries.csv","intermediate_datasets/location_data.xlsx")


# Process GDP data
gdp_proc.process_gdp("raw_datasets/mpd2023_web.xlsx", "final_datasets/gdp_data.xlsx")