import csv
import discogs_client
import time

# Initialize Discogs client
# Replace 'your_user_agent' and 'your_token' with your actual Discogs API credentials
d = discogs_client.Client('your_user_agent', user_token='vlGVlObmBoFJaeSwQiOGNiUnHxlgJJVjWtVJFuJG')

def search_discogs(track_name):
    try:
        results = d.search(track_name, type='release')
        if results:
            # Get the first result's first artist
            return results[0].artists[0].name
    except Exception as e:
        print(f"Error searching Discogs: {e}")
    return None

def process_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for row in reader:
            if row['artist_name'] == 'empty_field':
                artist = search_discogs(row['track_name'])
                if artist:
                    row['artist_name'] = artist
                    print(f"Updated artist for {row['track_name']}: {artist}")
                else:
                    print(f"Could not find artist for {row['track_name']}")
                time.sleep(1)  # Respect Discogs API rate limit
            
            writer.writerow(row)

# Usage
input_file = 'blues.csv'
output_file = 'output.csv'
process_csv(input_file, output_file)