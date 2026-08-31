import zipfile
import pandas as pd

with zipfile.ZipFile("google_transit.zip", "r") as zip_file:
    stops = pd.read_csv(zip_file.open("stops.txt"))

print(stops[stops["stop_id"] == 100])