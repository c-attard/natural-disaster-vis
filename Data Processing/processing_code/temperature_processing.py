import pandas as pd

def process_temps(raw_file, output_file):

    temps = pd.read_csv(raw_file)

    temps = temps[['Time', 'Anomaly (deg C)']] # Remove unneeded columns
    temps = temps[temps["Time"] >= "2013"] # Filter for data from 2013 and later
    idx = pd.DatetimeIndex(temps["Time"])
    temps = temps.set_index(idx)
    temp_series = temps["Anomaly (deg C)"]
    temp_series = temp_series.resample('D').interpolate() # Upsample to daily frequency
    temps = temp_series.to_frame()

    temps.to_excel(output_file)