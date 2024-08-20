import pandas as pd
import numpy as np

def impute_duration(df, strategy='mean'):
    """
    Impute the invalid values (-1) in the duration_ms column.

    Parameters:
    df (pd.DataFrame): The DataFrame containing the duration_ms column.
    strategy (str): The strategy to use for imputation. Either 'mean' or 'mode'.

    Returns:
    pd.DataFrame: The DataFrame with the imputed duration_ms column.
    """
    if strategy == 'mean':
        impute_value = round(df['duration_ms'].replace(-1, pd.NA).mean())
    elif strategy == 'mode':
        impute_value = round(df['duration_ms'].replace(-1, pd.NA).mode()[0])
    else:
        raise ValueError("Strategy not recognized. Use 'mean' or 'mode'.")

    # Get indices where the duration_ms is -1
    indices = df[df['duration_ms'] == -1].index

    # Replace each -1 with a slightly different value based on the impute_value
    for i, idx in enumerate(indices):
        df.at[idx, 'duration_ms'] = impute_value + i % 10  # Adding a small variation
    
    return df

def process_csv(input_file, output_file, strategy='mean'):
    """
    Process the input CSV file, impute missing/invalid duration_ms values, and save to a new CSV.

    Parameters:
    input_file (str): The path to the input CSV file.
    output_file (str): The path to save the processed CSV file.
    strategy (str): The strategy for imputation ('mean' or 'mode').
    """
    # Load the CSV file into a DataFrame
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    print("Data loaded successfully.")

    # Impute the duration_ms column
    df = impute_duration(df, strategy)
    print(f"Imputed duration_ms values using the {strategy} strategy.")

    # Save the processed DataFrame to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"Processing complete. The file has been saved as '{output_file}'.")

# Example usage:
# Adjust the input_file and output_file paths according to your directory structure.

input_file = '../data/Mega_processed_data.csv'
output_file = '../data/processed_data.csv'
process_csv(input_file, output_file, strategy='mean')
