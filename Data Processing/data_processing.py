import processing_code.disaster_processing as dis_proc
import processing_code.GDP_processing as gdp_proc
import processing_code.location_preprocessing as loc_proc
import processing_code.temperature_processing as temp_proc

# Process global temperature data
temp_proc.process_temps("raw_datasets/HadCRUT.5.0.2.0.analysis.summary_series.global.monthly.csv","final_datasets/temperature_data.xlsx")

# Process disaster data
loc_proc.process_locations("raw_datasets/cities.csv", "raw_datasets/states.csv","raw_datasets/countries.csv","intermediate_datasets/location_data.xlsx")
dis_proc.preprocess_disasters("raw_datasets/public_emdat_custom_request_2025-09-30_3e1debe8-7ea5-4b05-9973-cced1e8c63d6.xlsx","intermediate_datasets/disaster_data.xlsx")
dis_proc.fill_coordinates("intermediate_datasets/disaster_data.xlsx", "intermediate_datasets/location_data.xlsx", "final_datasets/disaster_data.xlsx")

# Process GDP data
gdp_proc.process_gdp("raw_datasets/mpd2023_web.xlsx", "final_datasets/gdp_data.xlsx")