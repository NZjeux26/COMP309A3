import pandas as pd

# Load the dataset
df = pd.read_csv('../data/genremodecon.csv')

# Split the concatenated genres into individual genres for each artist
df['genres_list'] = df['genre - Concatenate'].apply(lambda x: x.split())

# Explode the genres list to have one genre per row
df_exploded = df.explode('genres_list')

# Get unique genres for each artist
unique_genres = df_exploded.groupby('artist_name')['genres_list'].unique().reset_index()

# Join the unique genres into a string separated by '||'
unique_genres['genre_summary'] = unique_genres['genres_list'].apply(lambda genres: ','.join(genres))

# Drop the original genres list and keep only the artist name and genre summary
df_final = unique_genres[['artist_name', 'genre_summary']]

# Save the result to a CSV file
df_final.to_csv('artist_unique_genres.csv', index=False)

# Check the first few rows
print(df_final.head())
