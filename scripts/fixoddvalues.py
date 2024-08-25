import pandas as pd

def remove_invalid_duration(df):
    """
    Remove invalid values (-1) in the duration_ms column by setting them to NaN.
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the duration_ms column.

    Returns:
    pd.DataFrame: The DataFrame with the invalid duration_ms values set to NaN.
    """
    df['duration_ms'] = df['duration_ms'].replace(-1, pd.NA)
    return df

def remove_invalid_tempo(df):
    """
    Remove invalid values ('?') in the tempo column by setting them to NaN.
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the tempo column.

    Returns:
    pd.DataFrame: The DataFrame with the invalid tempo values set to NaN.
    """
    df['tempo'] = df['tempo'].replace('?', pd.NA)
    return df

def remove_invalid_instrumentalness(df):
    """
    Remove invalid values (0) in the instrumentalness column by setting them to NaN.
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the instrumentalness column.

    Returns:
    pd.DataFrame: The DataFrame with the invalid instrumentalness values set to NaN.
    """
    df['instrumentalness'] = df['instrumentalness'].replace(0, pd.NA)
    return df

def remove_invalid_popularity(df):
    """
    Remove invalid values (0) in the popularity column by setting them to a blank string.
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the popularity column.

    Returns:
    pd.DataFrame: The DataFrame with the invalid popularity values set to a blank string.
    """
    df['popularity'] = df['popularity'].replace(0, '')
    return df

def process_csv(input_file, output_file):
    """
    Process the input CSV file, remove invalid values, correct time signatures, and save to a new CSV.

    Parameters:
    input_file (str): The path to the input CSV file.
    output_file (str): The path to save the processed CSV file.
    """
    # Load the CSV file into a DataFrame
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    print("Data loaded successfully.")

    # Apply the invalid value removals and corrections
    df = remove_invalid_duration(df)
    df = remove_invalid_tempo(df)
    df = remove_invalid_instrumentalness(df)
    df = remove_invalid_popularity(df)
    print(f"Invalid values and misinterpreted time signatures have been corrected.")

    # Save the processed DataFrame to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"Processing complete. The file has been saved as '{output_file}'.")

# Example usage:
# Adjust the input_file and output_file paths according to your directory structure.

input_file = '../data/training-data/pop.csv'
output_file = '../data/PopPro.csv'
process_csv(input_file, output_file)
