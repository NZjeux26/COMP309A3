import pandas as pd

# Step 1: Load the CSVs
# Assume the files are named 'artists_genres.csv' and 'predictions.csv'
# You will need to replace these with your actual file names or paths
artists_genres_df = pd.read_csv('../data/artist_unique_genres.csv')
predictions_df = pd.read_csv('../data/NLRNGPredicitons.csv')

# Step 2: Create a dictionary of known artists and their genres for easy lookup
artist_genre_map = {}
for idx, row in artists_genres_df.iterrows():
    artist_name = row['artist_name']
    genres = row['genre_summary'].split(",")  # Assume multiple genres are comma-separated
    artist_genre_map[artist_name] = genres

# Step 3: Iterate over the prediction rows and verify the genres
for idx, row in predictions_df.iterrows():
    artist_name = row['artist_name']
    
    # If the artist is in the known list, check their genres
    if artist_name in artist_genre_map:
        known_genres = artist_genre_map[artist_name]
        predicted_genre = row['genre']
        
        # If the predicted genre is in the known genres, do nothing
        if predicted_genre not in known_genres: #replace this with if not in known genres, replace with mode
            # Pick the highest probability genre from the known genres
            genre_probabilities = {genre: row[f'NLRNG ({genre})'] for genre in known_genres if f'NLRNG ({genre})' in row}
            
            # Find the genre with the highest probability
            if genre_probabilities:
                best_genre = max(genre_probabilities, key=genre_probabilities.get)
                predictions_df.at[idx, 'genre'] = best_genre  # Update the genre in the predictions dataframe

# Step 4: Output the modified predictions to a new CSV
predictions_df.to_csv('updated_predictions.csv', index=False)

print("Predictions updated successfully.")
