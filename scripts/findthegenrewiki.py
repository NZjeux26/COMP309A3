import csv
import wikipediaapi
import re

# Define a custom User-Agent string
user_agent = "ArtistGenreFetcher/1.0 (A script to fetch artist genres from Wikipedia; brownphil3@vuw.ac.nz)"

# Initialize Wikipedia API with the custom User-Agent
wiki = wikipediaapi.Wikipedia('en', user_agent=user_agent)

def get_artist_genre_from_wikipedia(artist_name):
    try:
        # Search for the artist's Wikipedia page
        page = wiki.page(artist_name)
        if page.exists():
            # Extract text from the page
            text = page.text
            
            # Try to find the genre information in the text
            genre_section = re.search(r'(?i)genre[s]?:\s*(.*)', text)
            if genre_section:
                genres = genre_section.group(1).split(',')
                genres = [genre.strip() for genre in genres]
                return ', '.join(genres)
            
            # Alternatively, you can look for 'infobox' contents
            infobox_genres = re.search(r'(?i)genre[s]?\s*=\s*(.*)', page.summary)
            if infobox_genres:
                genres = infobox_genres.group(1).split(',')
                genres = [genre.strip() for genre in genres]
                return ', '.join(genres)
    
    except Exception as e:
        print(f"Error fetching Wikipedia data for {artist_name}: {e}")
    
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
                subgenre = get_artist_genre_from_wikipedia(row['artist_name'])
                row['subgenre'] = subgenre
                if subgenre:
                    print(f"Found genre for {row['artist_name']}: {subgenre}")
                else:
                    print(f"Could not find genre for {row['artist_name']}")
            else:
                row['subgenre'] = ''  # Leave subgenre blank for unknown artists
            
            writer.writerow(row)

# Usage
input_file = '../data/training-data/alternative.csv'
output_file = 'output_with_genres.csv'
process_csv(input_file, output_file)
