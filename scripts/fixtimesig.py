import pandas as pd
import os

# Define the relative path to the CSV file
csv_path = os.path.join(os.getcwd(), '../data/comedyPro.csv')
output_path = os.path.join(os.getcwd(), '../data/comedyPro.csv')

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

    # Save the modified DataFrame to a new CSV file
    df.to_csv(output_path, index=False)
    print(f"Modified CSV saved to: {output_path}")

print(f"Current working directory: {os.getcwd()}")
print(f"Expected CSV path: {csv_path}")
print(f"Output CSV path: {output_path}")
