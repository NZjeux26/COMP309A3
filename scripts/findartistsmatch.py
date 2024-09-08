import csv
import discogs_client
import time

# Initialize Discogs client
d = discogs_client.Client('your_user_agent', user_token='vlGVlObmBoFJaeSwQiOGNiUnHxlgJJVjWtVJFuJG')

def get_matching_artist(track_name, known_artists):
    try:
        # Search for the track by name
        results = d.search(track_name, type='release')
        if results:
            for result in results:
                for artist in result.artists:
                    if artist.name.strip().lower() in known_artists:
                        return artist.name  # Return the matching artist's name
    except Exception as e:
        print(f"Error fetching from Discogs: {e}")
    return None

def load_known_artists(artists_file):
    known_artists = set()
    with open(artists_file, 'r', encoding='utf-8', errors='ignore') as file:
        reader = csv.DictReader(file)
        for row in reader:
            artist_name = row.get('artist_name')
            if artist_name:
                known_artists.add(artist_name.strip().lower())
    return known_artists

def process_csv(artists_file, songs_file, output_file):
    # Load known artists
    known_artists = load_known_artists(artists_file)
    
    with open(songs_file, 'r', encoding='utf-8', errors='ignore') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for row in reader:
            if row['artist_name'] == 'empty_field' and row['track_name']:
                matching_artist = get_matching_artist(row['track_name'], known_artists)
                if matching_artist:
                    row['artist_name'] = matching_artist
                    print(f"Updated artist for track '{row['track_name']}': {matching_artist}")
                else:
                    print(f"Could not find a matching artist for track '{row['track_name']}'")
                time.sleep(1)  # Respect Discogs API rate limit
            
            writer.writerow(row)

# Usage
artists_file = '../data/genremodeFullset.csv'  # CSV containing the list of known artists
songs_file = '../data/testing-data/unknownArtists.csv'      # CSV containing the list of songs with unknown artists
output_file = 'output.csv'    # Output CSV to store the results
process_csv(artists_file, songs_file, output_file)
