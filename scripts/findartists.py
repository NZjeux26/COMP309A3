import csv
import discogs_client
import time

# Initialize Discogs client
d = discogs_client.Client('your_user_agent', user_token='vlGVlObmBoFJaeSwQiOGNiUnHxlgJJVjWtVJFuJG')

def get_matching_artist(track_name, track_genre, known_artists):
    try:
        results = d.search(track_name, type='release')
        if results:
            for result in results:
                for artist in result.artists:
                    artist_name = artist.name.strip().lower()
                    if artist_name in known_artists:
                        if track_genre.lower() in [genre.lower() for genre in known_artists[artist_name]['genres']]:
                            return artist.name  # Return the matching artist's name
    except Exception as e:
        print(f"Error fetching from Discogs: {e}")
    return None

def load_known_artists(artists_file):
    known_artists = {}
    with open(artists_file, 'r', encoding='utf-8', errors='ignore') as file:
        reader = csv.DictReader(file)
        for row in reader:
            artist_name = row.get('artist_name')
            genres = row.get('genre_summary', '').split()
            if artist_name:
                known_artists[artist_name.strip().lower()] = {'name': artist_name, 'genres': genres}
    return known_artists

def process_csv(artists_file, songs_file, output_file, start_row=1):
    known_artists = load_known_artists(artists_file)
    
    with open(songs_file, 'r', encoding='utf-8', errors='ignore') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for i, row in enumerate(reader, start=1):
            if i < start_row:
                writer.writerow(row)  # Write the row as is for skipped rows
                continue

            if row['artist_name'] == 'empty_field' and row['track_name']:
                matching_artist = get_matching_artist(row['track_name'], row['genre'], known_artists)
                if matching_artist:
                    row['artist_name'] = matching_artist
                    print(f"Row {i}: Updated artist for track '{row['track_name']}': {matching_artist}")
                else:
                    print(f"Row {i}: Could not find a matching artist for track '{row['track_name']}' with genre '{row['genre']}'")
                time.sleep(0.5)  # Respect Discogs API rate limit
            
            writer.writerow(row)

# Usage
artists_file = '../data/artist_unique_genres.csv'
songs_file = '../data/testing-data/unknownArtists.csv'
output_file = '../data/updatedartists2.csv'
start_row = 1619  # Start processing from this row
process_csv(artists_file, songs_file, output_file, start_row)