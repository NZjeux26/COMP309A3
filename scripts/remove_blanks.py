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
    Remove invalid values (0) in the instrumentness column by setting them to NaN.
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the instrumentness column.

    Returns:
    pd.DataFrame: The DataFrame with the invalid instrumentness values set to NaN.
    """
    df['instrumentalness'] = df['instrumentalness'].replace(0, pd.NA)
    return df

def correct_time_signature(df):
    """
    Correct time signature values that are misinterpreted as dates (e.g., "4-Apr" to "4/4").
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the time_signature column.

    Returns:
    pd.DataFrame: The DataFrame with corrected time signature values.
    """
    # Convert time_signature to string to ensure correct replacement
    df['time_signature'] = df['time_signature'].astype(str).str.strip()
    
    # Define a mapping for known misinterpretations
    corrections = {
        '4-Apr': '4',
        '5-Apr': '5/4',
        '1-Apr': '1/4',
        '2-Apr': '2/4',
        '3-Apr': '3/4'
        # Add more corrections if needed
    }
    
    # Apply corrections
    df['time_signature'] = df['time_signature'].replace(corrections)
    
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
    df = correct_time_signature(df)
    print(f"Invalid values and misinterpreted time signatures have been corrected.")

    # Save the processed DataFrame to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"Processing complete. The file has been saved as '{output_file}'.")

# Example usage:
# Adjust the input_file and output_file paths according to your directory structure.

input_file = '../data/merged_data.csv'
output_file = '../data/Mega_processed_data.csv'
process_csv(input_file, output_file)
