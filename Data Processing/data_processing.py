import processing_code.disaster_fuzzy_processing
import processing_code.disaster_preprocessing
import processing_code.GDP_processing
import processing_code.location_preprocessing
import processing_code.temperature_processing as temp_proc

temp_proc.process_temps("raw_datasets/HadCRUT.5.0.2.0.analysis.summary_series.global.monthly.csv", "processed_datasets/temperature_data.xlsx")
