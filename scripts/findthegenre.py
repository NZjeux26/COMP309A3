import csv
import discogs_client
import time

# Initialize Discogs client
d = discogs_client.Client('your_user_agent', user_token='vlGVlObmBoFJaeSwQiOGNiUnHxlgJJVjWtVJFuJG')

def get_artist_genre(artist_name):
    try:
        # Search for the artist
        results = d.search(artist_name, type='artist')
        if results:
            for result in results:
                # Check if the result is an Artist object
                if isinstance(result, discogs_client.models.Artist):
                    artist = result
                    genres = set()
                    
                    # Check artist's releases for genres
                    try:
                        releases = artist.releases
                        count = 0
                        for release in releases:
                            if count >= 5:  # Limit to first 5 releases
                                break
                            release_details = d.release(release.id)
                            if hasattr(release_details, 'genres'):
                                genres.update(release_details.genres)
                            if hasattr(release_details, 'styles'):
                                genres.update(release_details.styles)
                            count += 1
                    except Exception as e:
                        print(f"Error fetching releases for {artist_name}: {e}")
                    
                    if genres:
                        return ', '.join(genres)
                    break  # Stop after checking the first artist result
        
    except Exception as e:
        print(f"Error searching Discogs for {artist_name}: {e}")
    
    return ''  # Return empty string if no genre found or error occurred

def process_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['subgenre'] if 'subgenre' not in reader.fieldnames else reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for row in reader:
            if row['artist_name'] != 'empty_field':
                subgenre = get_artist_genre(row['artist_name'])
                row['subgenre'] = subgenre
                if subgenre:
                    print(f"Found subgenre for {row['artist_name']}: {subgenre}")
                else:
                    print(f"Could not find subgenre for {row['artist_name']}")
                time.sleep(1)  # Respect Discogs API rate limit
            else:
                row['subgenre'] = ''  # Leave subgenre blank for unknown artists
            
            writer.writerow(row)

# Usage
input_file = '../data/training-data/alternative.csv'
output_file = 'output_with_genres.csv'
process_csv(input_file, output_file)
