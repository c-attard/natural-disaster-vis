import pandas as pd

temps = pd.read_csv("datasets/HadCRUT.5.0.2.0.analysis.summary_series.global.monthly.csv")

temps = temps[['Time', 'Anomaly (deg C)']] # Remove unneeded columns
temps = temps[temps["Time"] >= "2013"] # Filter for data from 2013 and later
idx = pd.DatetimeIndex(temps["Time"])
temps = temps.set_index(idx)
temp_series = temps["Anomaly (deg C)"]
temp_series = temp_series.resample('D').interpolate() # Upsample to daily frequency
temps = temp_series.to_frame()

temps.to_excel("temperature_data.xlsx")