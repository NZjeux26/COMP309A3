import pandas as pd
from collections import Counter

# Step 1: Load the CSVs
artists_genres_df = pd.read_csv('../data/artist_unique_genres.csv')
predictions_df = pd.read_csv('../data/outputs/test_predictions2.csv')

# Step 2: Create a dictionary of known artists and their mode genre for easy lookup
artist_mode_genre_map = dict(zip(artists_genres_df['artist_name'], artists_genres_df['genre_mode']))

# Step 3: Iterate over the prediction rows and verify the genres
for idx, row in predictions_df.iterrows():
    artist_name = row['artist_name']
    
    # If the artist is in the known list, check their mode genre
    if artist_name in artist_mode_genre_map:
        mode_genre = artist_mode_genre_map[artist_name]
        predicted_genre = row['genre']
        
        # If the predicted genre is not the mode genre, replace with mode genre
        if predicted_genre != mode_genre:
            predictions_df.at[idx, 'genre'] = mode_genre  # Update the genre in the predictions dataframe
            
# Step 4: Output the modified predictions to a new CSV
predictions_df.to_csv('../data/outputs/updated_predictions3.csv', index=False)

print("Predictions updated successfully.")