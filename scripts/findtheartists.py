import csv
import discogs_client
import time

# Initialize Discogs client
# Replace 'your_user_agent' and 'your_token' with your actual Discogs API credentials
d = discogs_client.Client('your_user_agent', user_token='vlGVlObmBoFJaeSwQiOGNiUnHxlgJJVjWtVJFuJG')

def get_artist_from_discogs(track_id):
    try:
        # Fetch the release using the track ID
        release = d.release(track_id)
        if release:
            # Return all artists of the release
            return ", ".join(artist.name for artist in release.artists)
    except Exception as e:
        print(f"Error fetching from Discogs: {e}")
    return None

def process_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for row in reader:
            if row['artist_name'] == 'empty_field' and row['track_id']:
                artist = get_artist_from_discogs(row['track_id'])
                if artist:
                    row['artist_name'] = artist
                    print(f"Updated artist for track ID {row['trackID']}: {artist}")
                else:
                    print(f"Could not find artist for track ID {row['track_id']}")
                time.sleep(1)  # Respect Discogs API rate limit
            
            writer.writerow(row)

# Usage
input_file = 'blues.csv'
output_file = 'output.csv'
process_csv(input_file, output_file)