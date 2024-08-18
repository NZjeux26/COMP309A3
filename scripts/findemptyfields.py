import pandas as pd

# Path to your CSV file
csv_file_path = 'your_file.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# Count how many cells contain the value 'empty_field'
count_empty_field = (df == 'empty_field').sum().sum()

print(f"Count of 'empty_field': {count_empty_field}")
