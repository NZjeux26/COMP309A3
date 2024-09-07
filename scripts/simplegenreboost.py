import pandas as pd
from collections import Counter

# Step 1: Load the CSVs
artists_genres_df = pd.read_csv('../data/artist_unique_genres.csv')
predictions_df = pd.read_csv('../data/outputs/test_predictions2.csv')

# Step 2: Create a dictionary of known artists, their genres, and mode genre for easy lookup
artist_info_map = {}
for idx, row in artists_genres_df.iterrows():
    artist_name = row['artist_name']
    genres = row['genre_summary'].split(",")  # Assume multiple genres are comma-separated
    mode_genre = row['genre_mode']
    artist_info_map[artist_name] = {'genres': genres, 'genre_mode': mode_genre}

# Step 3: Iterate over the prediction rows and verify the genres
for idx, row in predictions_df.iterrows():
    artist_name = row['artist_name']
    
    # If the artist is in the known list, check their genres
    if artist_name in artist_info_map:
        known_genres = artist_info_map[artist_name]['genres']
        mode_genre = artist_info_map[artist_name]['genre_mode']
        predicted_genre = row['genre']
        
        # If the predicted genre is not in the known genres, replace with genre_mode
        if predicted_genre not in known_genres:
            predictions_df.at[idx, 'genre'] = mode_genre  # Update the genre in the predictions dataframe
            
# Step 4: Output the modified predictions to a new CSV
predictions_df.to_csv('../data/outputs/updated_predictions3.csv', index=False)

print("Predictions updated successfully.")