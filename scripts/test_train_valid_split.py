import pandas as pd
from sklearn.model_selection import train_test_split

def split_dataset(input_file, train_file, test_file, val_file, train_size=0.7, test_size=0.2, val_size=0.1, random_state=None):
    """
    Split the dataset into training, testing, and validation sets.

    Parameters:
    - input_file (str): The path to the input CSV file.
    - train_file (str): The path to save the training set CSV file.
    - test_file (str): The path to save the testing set CSV file.
    - val_file (str): The path to save the validation set CSV file.
    - train_size (float): The proportion of data to include in the training set (default 0.7).
    - test_size (float): The proportion of data to include in the testing set (default 0.2).
    - val_size (float): The proportion of data to include in the validation set (default 0.1).
    - random_state (int): Random seed for reproducibility (default None).

    Returns:
    - None
    """
    # Load the dataset
    print(f"Loading data from {input_file}...")
    df = pd.read_csv(input_file)
    print(f"Data loaded successfully with {len(df)} records.")

    # Ensure the sizes add up to 1.0 (with a small tolerance for floating-point precision)
    total_size = train_size + test_size + val_size
    assert abs(total_size - 1.0) < 1e-8, "Train, test, and validation sizes must sum to 1.0"

    # First, split the data into training + validation and testing sets
    df_train_val, df_test = train_test_split(df, test_size=test_size, random_state=random_state)
    print(f"Test set created with {len(df_test)} records.")

    # Then, split the remaining data into training and validation sets
    val_relative_size = val_size / (train_size + val_size)  # relative size of validation set in the remaining data
    df_train, df_val = train_test_split(df_train_val, test_size=val_relative_size, random_state=random_state)
    print(f"Train set created with {len(df_train)} records.")
    print(f"Validation set created with {len(df_val)} records.")

    # Save the splits to CSV files
    df_train.to_csv(train_file, index=False)
    df_test.to_csv(test_file, index=False)
    df_val.to_csv(val_file, index=False)
    print(f"Datasets have been saved as:\nTrain: {train_file}\nTest: {test_file}\nValidation: {val_file}")

# Example usage:
input_file = '../data/mega_full_processed.csv'
train_file = '../data/train_data.csv'
test_file = '../data/test_data.csv'
val_file = '../data/val_data.csv'
split_dataset(input_file, train_file, test_file, val_file, random_state=42)
