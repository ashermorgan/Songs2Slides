from dotenv import load_dotenv

import os
import requests

class SongData:
    """
    Represents data about a song

    Attributes:
    -----------
    title : str
        The title of the song
    artist : str
        The artist of the song
    lyrics : str
        The song's lyrics, with double newlines separating stanzas
    """

    def __init__(self, title: str, artist: str, lyrics: str):
        self.title = title
        self.artist = artist
        self.lyrics = lyrics

def get_song_data(title: str, artist:str):
    """
    Get song data from an external API

    Parameters:
    -----------
    title : str
        The title of the song
    artist : str
        The artist of the song

    Returns
    -------
    SongData
        The song data
    """

    url = os.getenv('API_URL')
    if url is None:
        raise Exception()
    url = url.replace('{title}', title, 1)
    url = url.replace('{artist}', artist, 1)
    data = requests.get(url).json()

    if 'lyrics' in data.keys():
        return SongData(data['title'], data['artist'], data['lyrics'])
    else:
        raise Exception()
