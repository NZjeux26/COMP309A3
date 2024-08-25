import csv
import wikipediaapi
import re
import time
import requests

# Define a custom User-Agent string
user_agent = "ArtistGenreFetcher/1.0 (A script to fetch artist genres from Wikipedia; brownphil3@vuw.ac.nz)"

# Initialize Wikipedia API with the custom User-Agent
wiki = wikipediaapi.Wikipedia(user_agent=user_agent)

def format_artist_name(name):
    return name.replace(' ', '_').title()

def get_artist_genre_from_wikipedia(artist_name):
    print(f"Searching for: {artist_name}")
    try:
        # Use MediaWiki API to get the raw wikitext
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "format": "json",
            "titles": artist_name,
            "prop": "revisions",
            "rvprop": "content",
            "rvslots": "main"
        }
        response = requests.get(url, params=params, headers={"User-Agent": user_agent})
        data = response.json()
        
        # Extract the page content
        pages = data['query']['pages']
        for page_id in pages:
            content = pages[page_id]['revisions'][0]['slots']['main']['*']
            
            # Look for the genre information in the infobox
            genre_match = re.search(r'\|\s*genres?\s*=\s*(.+?)(?:\n\||\n\})', content, re.IGNORECASE | re.DOTALL)
            if genre_match:
                genres_raw = genre_match.group(1)
                # Clean up the genres
                genres = re.findall(r'\[\[([^\]|]+)', genres_raw)
                if not genres:
                    genres = re.findall(r'([^,\[\]]+)', genres_raw)
                genres = [genre.strip() for genre in genres if genre.strip()]
                print(f"Extracted genres: {genres}")
                return ', '.join(genres)
            
            print("No genre information found in the infobox.")
    
    except Exception as e:
        print(f"Error fetching Wikipedia data for {artist_name}: {str(e)}")
    
    return ''

def process_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile, \
         open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['subgenre'] if 'subgenre' not in reader.fieldnames else reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for row in reader:
            if row['artist_name'] != 'empty_field':
                artist_name = format_artist_name(row['artist_name'])
                subgenre = get_artist_genre_from_wikipedia(artist_name)
                row['subgenre'] = subgenre
                if subgenre:
                    print(f"Found genre for {row['artist_name']}: {subgenre}")
                else:
                    print(f"Could not find genre for {row['artist_name']}")
            else:
                row['subgenre'] = ''  # Leave subgenre blank for unknown artists
            
            writer.writerow(row)
            time.sleep(1)  # 1 second delay between requests

# Usage
input_file = '../data/training-data/alternative.csv'
output_file = 'output_with_genres.csv'
process_csv(input_file, output_file)