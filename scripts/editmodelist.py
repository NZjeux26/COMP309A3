import pandas as pd

# Load the dataset
df = pd.read_csv('../data/genremodecon.csv')

# Split the concatenated genres into individual genres for each artist
df['genres_list'] = df['genre - Concatenate'].apply(lambda x: x.split())

# Explode the genres list to have one genre per row
df_exploded = df.explode('genres_list')

# Count occurrences of each genre per artist
genre_counts = df_exploded.groupby(['artist_name', 'genres_list']).size().reset_index(name='genre_count')

# Pivot the data to get genres as columns and fill missing values with 0
df_pivot = genre_counts.pivot(index='artist_name', columns='genres_list', values='genre_count').fillna(0)

# Create a string summarizing each artist's genre and count
df_pivot['genre_summary'] = df_pivot.apply(lambda row: ', '.join([f'{genre} {int(count)}' for genre, count in row.items() if count > 0]), axis=1)

# Save only artist name and genre summary to CSV
df_final = df_pivot[['genre_summary']].reset_index()
df_final.to_csv('artist_genre_summary.csv', index=False)

# Check the first few rows
print(df_final.head())
