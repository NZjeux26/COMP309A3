import pandas as pd

# Step 1: Read the CSV files into DataFrames
df1 = pd.read_csv('../data/mega_full_processed.csv')  # The first CSV with artist_name and track_id
df2 = pd.read_csv('../data/updatedartists2.csv')  # The second CSV with track_id and artist_name

# Step 2: Merge the DataFrames on 'track_id' using a left join
merged_df = pd.merge(df1, df2[['instance_id', 'artist_name']], on='instance_id', how='left', suffixes=('', '_new'))

# Step 3: Replace 'empty_field' in the artist_name of the first DataFrame
merged_df['artist_name'] = merged_df.apply(
    lambda row: row['artist_name_new'] if row['artist_name'] == 'empty_field' and row['artist_name_new'] != 'empty_field' else row['artist_name'], 
    axis=1
)

# Drop the 'artist_name_new' column as it is no longer needed
merged_df.drop(columns=['artist_name_new'], inplace=True)

# Step 4: Save the resulting DataFrame back to a CSV file
merged_df.to_csv('merged_artists_songs.csv', index=False)
