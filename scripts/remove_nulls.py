import pandas as pd

def remove_null_values(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Remove null values
    df_clean = df.dropna()
    
    # Save the cleaned data to a new CSV file
    df_clean.to_csv(output_file, index=False)
    
    print(f"Null values removed. Cleaned data saved to {output_file}")

if __name__ == "__main__":
    # Add your input and output file names here
    input_file = "../data/outputs/megaoutputtest3.csv"
    output_file = "../data/outputs/megaoutputtest3.csv"
    
    remove_null_values(input_file, output_file)