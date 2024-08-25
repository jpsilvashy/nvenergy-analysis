import pandas as pd
import matplotlib.pyplot as plt
from zipfile import ZipFile
import io
import glob

def get_user_rates():
    print("Please enter your electricity rates and time-of-use periods.")
    print("Press Enter without any input to use all default values.")
    print("Or enter custom values, pressing Enter after each to use the default for that item.")
    
    defaults = {
        'summer_peak': 0.37534,
        'summer_off_peak': 0.07643,
        'winter_peak': 0.07691,
        'winter_off_peak': 0.07691,
        'peak_start': 15,
        'peak_end': 21,
        'summer_start': 6,
        'summer_end': 9
    }
    
    user_input = input("Press Enter to use all defaults, or type anything to enter custom values: ")
    
    if user_input == "":
        return defaults
    
    rates = {}
    for key, default_value in defaults.items():
        user_value = input(f"{key.replace('_', ' ').title()} [{default_value}]: ")
        rates[key] = type(default_value)(user_value) if user_value else default_value
    
    return rates

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

def load_and_process_data(data_directory):
    zip_files = glob.glob(f'{data_directory}/usage-data-*.zip')
    all_demand_data = []
    all_usage_data = []
    
    for zip_file in zip_files:
        demand_data, usage_data = process_zip_file(zip_file)
        if demand_data is not None:
            all_demand_data.append(demand_data)
        if usage_data is not None:
            all_usage_data.append(usage_data)
    
    combined_demand_data = pd.concat(all_demand_data, ignore_index=True)
    combined_usage_data = pd.concat(all_usage_data, ignore_index=True)
    
    combined_demand_data.drop_duplicates(subset=['startTime'], keep='first', inplace=True)
    combined_usage_data.drop_duplicates(subset=['startTime'], keep='first', inplace=True)
    
    combined_demand_data['startTime'] = pd.to_datetime(combined_demand_data['startTime'])
    combined_usage_data['startTime'] = pd.to_datetime(combined_usage_data['startTime'])
    
    combined_demand_data.set_index('startTime', inplace=True)
    combined_usage_data.set_index('startTime', inplace=True)
    
    return combined_demand_data, combined_usage_data

def resample_hourly(demand_data, usage_data):
    demand_hourly = demand_data['value'].resample('h').mean()
    usage_hourly = usage_data['Usage'].resample('h').mean()
    return demand_hourly, usage_hourly

def get_peak_times(usage_hourly, n=5):
    return usage_hourly.nlargest(n)

def get_rate(row, rates):
    month = row.name.month
    hour = row.name.hour
    is_summer = rates['summer_start'] <= month <= rates['summer_end']
    is_peak = rates['peak_start'] <= hour < rates['peak_end']
    
    if is_summer:
        return rates['summer_peak'] if is_peak else rates['summer_off_peak']
    else:
        return rates['winter_peak'] if is_peak else rates['winter_off_peak']

def add_rate_and_cost(usage_hourly, rates):
    usage_hourly = usage_hourly.to_frame(name='usage')
    usage_hourly['rate'] = usage_hourly.apply(lambda row: get_rate(row, rates), axis=1)
    usage_hourly['cost'] = usage_hourly['usage'] * usage_hourly['rate']
    return usage_hourly
