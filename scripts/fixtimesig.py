import pandas as pd
import os

# Define the relative path to the CSV file
csv_path = os.path.join(os.getcwd(), 'blues.csv')

# Check if the file exists
if not os.path.exists(csv_path):
    print(f"File not found: {csv_path}")
else:
    # Read the CSV file into a DataFrame using the verified path
    df = pd.read_csv(csv_path)

    # Function to correct the time_signature
    def correct_time_signature(value):
        if isinstance(value, str) and '-Apr' in value:
            return value.split('-')[0] + '/4'
        return value

    # Apply the correction
    df['time_signature'] = df['time_signature'].apply(correct_time_signature)

    print(df)

print(f"Current working directory: {os.getcwd()}")
print(f"Expected CSV path: {csv_path}")
