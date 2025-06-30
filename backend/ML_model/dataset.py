import pandas as pd
import numpy as np
import random

# Define product types and their spoilage sensitivity
product_ranges = {
    'Milk': {'temp_range': (2, 10), 'humid_range': (60, 90), 'shock_range': (0, 5), 'temp_threshold': 7},
    'Meat': {'temp_range': (0, 8), 'humid_range': (70, 95), 'shock_range': (0, 5), 'temp_threshold': 6},
    'Vegetables': {'temp_range': (2, 12), 'humid_range': (80, 98), 'shock_range': (0, 5), 'temp_threshold': 8},
    'Fruits': {'temp_range': (4, 15), 'humid_range': (70, 90), 'shock_range': (0, 5), 'temp_threshold': 9},
    'Eggs': {'temp_range': (2, 10), 'humid_range': (50, 70), 'shock_range': (0, 5), 'temp_threshold': 7}
}

num_samples = 5000
data = []

for _ in range(num_samples):
    product_type = random.choice(list(product_ranges.keys()))
    prod_info = product_ranges[product_type]

    temp = round(random.uniform(*prod_info['temp_range']), 1)
    humid = round(random.uniform(*prod_info['humid_range']), 1)
    shock = round(random.uniform(*prod_info['shock_range']), 2)

    # Risk logic per product
    risk_level = 1 if (temp > prod_info['temp_threshold']) or (humid > 85) or (shock > 2.5) else 0

    data.append({
        'Product Type': product_type,
        'Temperature (°C)': temp,
        'Humidity (%)': humid,
        'Shock Level (g)': shock,
        'Risk Level': risk_level
    })

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV
df.to_csv('foodchain_iq_dataset_5k.csv', index=False)

print("✅ Dataset generated and saved as 'foodchain_iq_dataset_5k.csv'")