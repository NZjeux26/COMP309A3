import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('../data/merged_data.csv')

# Check the column name for genres (assuming it's 'Genre')
genre_column = 'genre'

# Sample 1000 rows from each genre
sampled_df = df.groupby(genre_column).apply(lambda x: x.sample(1000, random_state=94)).reset_index(drop=True)

# Save the sampled data to a new CSV file
sampled_df.to_csv('../data/mini_setV.csv', index=False)

print("Sampling complete. The sampled data is saved in 'sampled_output.csv'.")
