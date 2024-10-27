import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Parameters
start_date = '2015-01-01'
end_date = pd.to_datetime('today').normalize()  # Today's date
total_area_sqft = 5.3 * 1e6  # Total area of Manyata Tech Park in square feet
number_of_tenants = 26  # Number of tenants

# Generate date range
date_range = pd.date_range(start=start_date, end=end_date, freq='D')

# Create DataFrame for date
data = pd.DataFrame(date_range, columns=['Date'])

# Tenant names and their corresponding industry types
tenant_industry_dict = {
    'Alcatel Lucent Technologies': 'Telecommunications',
    'Andritz': 'Engineering',
    'ANZ': 'Finance',
    'Cerner Health Care Solutions': 'Healthcare',
    'Cognizant': 'IT Services',
    'Colt Technologies': 'Technology',
    'Data Craft India': 'Consulting',
    'Fidelity': 'Finance',
    'IBM': 'Engineering',
    'Jurimatrix': 'Consulting',
    'L and T': 'Manufacturing',
    'Mavenir': 'Biotechnology',
    'Monsanto Holdings': 'Telecommunications',
    'Nokia Siemens Network India': 'Technology',
    'Northern Operation Services': 'Outsourcing',
    'Nvidia Graphics': 'Semiconductors',
    'Stylus Commercial Services': 'IT Services',
    'Target Operation': 'Consulting',
    'Netscout System Software': 'Software',
    'Software Software Software': 'Travel',
    'Via.com': 'Software',
    'TP Vision': 'Software',
    'Justdial': 'Electronics',
    'Philips': 'Technology',
    'Novell': 'Software',
    'TCS': 'Telecommunications',  # Added TCS to ensure 26 tenants
}

# Ensure we have the correct number of tenants
if len(tenant_industry_dict) != number_of_tenants:
    raise ValueError(f"Expected {number_of_tenants} tenants, but found {len(tenant_industry_dict)}.")

# Convert the dictionary to a DataFrame
tenant_data = pd.DataFrame(list(tenant_industry_dict.items()), columns=['Tenant', 'Industry_Type'])

# Assign random tenant and industry type to each date entry
data = data.assign(Tenant=np.random.choice(tenant_data['Tenant'], size=len(data)))
data = data.merge(tenant_data, on='Tenant', how='left')

# Randomly assign number of floors (1 to 10)
data['Number_of_Floors'] = np.random.randint(1, 11, size=len(data))

# Randomly assign number of employees
data['Number_of_Employees'] = np.random.randint(50, 500, size=len(data))

# Apply shutdown period: 2020-03-01 to 2021-12-31
shutdown_start = pd.to_datetime('2020-03-01')
shutdown_end = pd.to_datetime('2021-12-31')
data.loc[(data['Date'] >= shutdown_start) & (data['Date'] <= shutdown_end), 'Number_of_Employees'] = 0

# Set number of employees to 0 on weekends (Saturday and Sunday)
data['Day_of_Week'] = data['Date'].dt.dayofweek
data.loc[data['Day_of_Week'].isin([5, 6]), 'Number_of_Employees'] = 0  # 5 = Saturday, 6 = Sunday

# Generate acquired area for each tenant
acquired_area_per_tenant = np.random.rand(number_of_tenants)
acquired_area_per_tenant = (acquired_area_per_tenant / acquired_area_per_tenant.sum()) * total_area_sqft  # in square feet

# Create a mapping for acquired area per tenant
area_mapping = dict(zip(tenant_data['Tenant'], acquired_area_per_tenant))

# Assign acquired area to each entry in the DataFrame based on the tenant
data['Acquired_Area'] = data['Tenant'].map(area_mapping)

# Calculate base electricity reading based on acquired area, number of floors, and number of employees
base_electricity_reading = (
    (data['Number_of_Employees'] * 0.2) +  # Example: each employee contributes to reading
    (data['Acquired_Area'] / 1000 * 0.1) +  # Area contribution to electricity reading (0.1 kWh per sqft)
    (data['Number_of_Floors'] * 5)  # Additional reading per floor
)

# Assign base electricity reading
data['Base_Electricity_Reading'] = base_electricity_reading

# Define industry type multipliers as a range (min, max)
industry_multiplier_ranges = {
    'Manufacturing': (1.3, 1.7),
    'Engineering': (1.3, 1.7),
    'Healthcare': (1.2, 1.5),
    'Finance': (1.1, 1.3),
    'IT Services': (1.3, 1.7),
    'Technology': (1.0, 1.2),
    'Consulting': (0.9, 1.1),
    'Biotechnology': (1.2, 1.3),
    'Telecommunications': (0.9, 1.1),
    'Semiconductors': (1.1, 1.3),
    'Electronics': (1.4, 1.6),
    'Outsourcing': (0.9, 1.1),
    'Travel': (0.9, 1.1),
    'Software': (1.2, 1.5),
}

# Apply the adjustments based on the industry type using the defined ranges
for industry, (min_multiplier, max_multiplier) in industry_multiplier_ranges.items():
    random_multiplier = np.random.uniform(min_multiplier, max_multiplier)
    data.loc[data['Industry_Type'] == industry, 'Base_Electricity_Reading'] *= random_multiplier

# Define weekday multipliers
day_multipliers = {
    0: 0.5,  # Monday
    1: 1.0,  # Tuesday
    2: 1.0,  # Wednesday
    3: 1.0,  # Thursday
    4: (1.2, 1.5),  # Friday (Increase on Fridays)
    5: 0.0,  # Saturday (No employees)
    6: 0.0,  # Sunday (No employees)
}

# Apply day multipliers to Base Electricity Reading
for day, multiplier in day_multipliers.items():
    if isinstance(multiplier, tuple):
        # For Friday, randomly select a multiplier within the specified range
        random_multiplier = np.random.uniform(multiplier[0], multiplier[1])
        data.loc[data['Day_of_Week'] == day, 'Base_Electricity_Reading'] *= random_multiplier
    else:
        data.loc[data['Day_of_Week'] == day, 'Base_Electricity_Reading'] *= multiplier

# Apply seasonal adjustments to electricity readings
data['Electricity_Reading'] = data['Base_Electricity_Reading']
seasonal_multiplier = 1  # Default multiplier
data['Month'] = data['Date'].dt.month

# Adjust reading based on season
data.loc[data['Month'].isin([2, 3, 4,5,6]), 'Electricity_Reading'] *= 2.0  # Highest in Feb-Apr
data.loc[data['Month'].isin([7, 8,]), 'Electricity_Reading'] *= 1.5 # Moderate in May-Sep
data.loc[data['Month'].isin([9,10]), 'Electricity_Reading'] *= 0.9  # Least in Oct-Nov
data.loc[data['Month'].isin([12,11,1]), 'Electricity_Reading'] *= 1.8  # More than moderate in Dec-Jan

# Add noise to electricity readings
data['Electricity_Reading'] += np.random.normal(0, 5, len(data))

# Ensure non-negative electricity readings
data['Electricity_Reading'] = data['Electricity_Reading'].clip(lower=0)

# Clean up the DataFrame
#data.drop(columns=['Day_of_Week', 'Month'], inplace=True)  # Drop temporary columns

# Display the first few rows of the DataFrame
print(data.info())

# Optionally save to CSV
data.to_csv('manyata_tech_park_data.csv', index=False)
