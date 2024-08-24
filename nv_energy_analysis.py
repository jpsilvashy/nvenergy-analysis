import pandas as pd
import matplotlib.pyplot as plt
from zipfile import ZipFile
import io
import glob
import os

def read_csv_from_zip(zip_file, csv_filename):
    with ZipFile(zip_file) as zf:
        with zf.open(csv_filename) as f:
            return pd.read_csv(io.TextIOWrapper(f))

def process_zip_file(zip_file):
    demand_data = None
    usage_data = None
    
    with ZipFile(zip_file) as zf:
        for filename in zf.namelist():
            if filename.endswith('_Demand.csv'):
                demand_data = read_csv_from_zip(zip_file, filename)
            elif filename.endswith('.csv') and not filename.endswith('_Demand.csv'):
                usage_data = read_csv_from_zip(zip_file, filename)
    
    return demand_data, usage_data

# Get all zip files in the data directory
zip_files = glob.glob('/app/data/usage-data-*.zip')

all_demand_data = []
all_usage_data = []

for zip_file in zip_files:
    demand_data, usage_data = process_zip_file(zip_file)
    if demand_data is not None:
        all_demand_data.append(demand_data)
    if usage_data is not None:
        all_usage_data.append(usage_data)

# Combine all data
combined_demand_data = pd.concat(all_demand_data, ignore_index=True)
combined_usage_data = pd.concat(all_usage_data, ignore_index=True)

# Remove duplicates
combined_demand_data.drop_duplicates(subset=['startTime'], keep='first', inplace=True)
combined_usage_data.drop_duplicates(subset=['startTime'], keep='first', inplace=True)

# Convert 'startTime' to datetime
combined_demand_data['startTime'] = pd.to_datetime(combined_demand_data['startTime'])
combined_usage_data['startTime'] = pd.to_datetime(combined_usage_data['startTime'])

# Set 'startTime' as index
combined_demand_data.set_index('startTime', inplace=True)
combined_usage_data.set_index('startTime', inplace=True)

# Resample to hourly data and calculate mean
demand_hourly = combined_demand_data['value'].resample('H').mean()
usage_hourly = combined_usage_data['Usage'].resample('H').mean()

# Plot the data
plt.figure(figsize=(12, 6))
plt.plot(demand_hourly.index, demand_hourly.values, label='Demand (KW)')
plt.plot(usage_hourly.index, usage_hourly.values, label='Usage (KWH)')
plt.title('NV Energy Hourly Demand and Usage')
plt.xlabel('Time')
plt.ylabel('KW / KWH')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('/app/data/nv_energy_analysis.png')
plt.close()

# Calculate some statistics
print(f"Average Demand: {demand_hourly.mean():.2f} KW")
print(f"Max Demand: {demand_hourly.max():.2f} KW")
print(f"Average Usage: {usage_hourly.mean():.2f} KWH")
print(f"Total Usage: {usage_hourly.sum():.2f} KWH")

# Identify peak usage times
peak_times = usage_hourly.nlargest(5)
print("\nPeak Usage Times:")
print(peak_times)

# Save combined data to CSV files
combined_demand_data.to_csv('/app/data/combined_demand_data.csv')
combined_usage_data.to_csv('/app/data/combined_usage_data.csv')

print("Analysis complete. Results saved in /app/data/")