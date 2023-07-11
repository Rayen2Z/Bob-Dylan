import os
import re
import time

import lyricsgenius as genius
import pandas as pd
from dotenv import load_dotenv

df = pd.read_csv('bobby_discography.csv', delimiter=";")

# Assign an album_id to each album
df_album = df[['album_title', 'year_of_release', 'month_of_release']].drop_duplicates()
df_album['album_id'] = range(1, len(df_album) + 1)
df = df.merge(df_album[['album_title', 'album_id']], on='album_title')

# Setup Genius API
api_key = os.getenv('GENUIS_API_TOKEN')


# Function to fetch lyrics
def fetch_lyrics(song, artist):
    song = api.search_song(song, artist)
    time.sleep(1)
    if song is not None:
        return song.lyrics
    else:
        return None


# Iterate over songs and fetch lyrics
df['lyrics'] = df.apply(lambda row: fetch_lyrics(row['song_title'], "Bob Dylan"), axis=1)


def remove_pattern(text):
    if pd.isnull(text):
        return text
    return re.sub(r'\d*Embed$', '', text)


def clean_lyrics(df):
    # Remove the initial part before the actual lyrics
    df['lyrics'] = df['lyrics'].str.replace('.*Lyrics', '', regex=True)

    # Replace occurrences of square brackets with a space
    df['lyrics'] = df['lyrics'].str.replace('\[.*?\]', '', regex=True)

    # Remove the ending part after the actual lyrics
    df['lyrics'] = df['lyrics'].str.replace('You might also like.*', '', regex=True)

    # Replace newline characters with a point followed by a space
    df['lyrics'] = df['lyrics'].str.replace('\n', '. ', regex=False)

    # Remove leading and trailing whitespaces and newline characters
    df['lyrics'] = df['lyrics'].str.strip()

    # Apply the function to the 'lyrics' column
    df['lyrics'] = df['lyrics'].apply(remove_pattern)

    return df


df = clean_lyrics(df)
df.to_csv('bobby_discography_with_lyrics.csv', index=False)

## Prepare data for storage

# Create a DataFrame for Album node 
df_album = df[['album_id', 'album_title', 'year_of_release', 'month_of_release']].drop_duplicates()
df_album.to_csv('album_node.csv', index=False)

# Create a DataFrame for Song node 
df_song = df[['id', 'song_title', 'type', 'lyrics']].drop_duplicates().rename(columns={'id': 'song_id'})
df_song.to_csv('song_node.csv', index=False)

# Create DataFrame for Relationships using album_id and id
df_relationships = df[['album_id', 'id']].rename(columns={'id': 'song_id'})
df_relationships.to_csv('relationships.csv', index=False)
