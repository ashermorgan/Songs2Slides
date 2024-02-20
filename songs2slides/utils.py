from dotenv import load_dotenv

from dataclasses import dataclass
import os
import requests

@dataclass
class SongData:
    """
    Represents data about a song

    Attributes
    ----------
    title : str
        The title of the song
    artist : str
        The artist of the song
    lyrics : str
        The song's lyrics, with double newlines separating stanzas
    """

    title: str
    artist: str
    lyrics: str

def get_song_data(title: str, artist:str):
    """
    Get song data from an external API

    Parameters
    ----------
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

def get_slide_contents(lyrics: str, lines_per_slide: int = 4):
    """
    Generate slide contents from song lyrics

    Parameters
    ----------
    lyrics : str
        The song lyrics
    lines_per_slide : int
        The maximum number of lines per slide (the default is 4)

    Returns
    -------
    list of str
        The list of slide contents
    """

    slides = ['']
    line_count = 0

    for line in lyrics.split('\n'):
        line = line.strip()

        if line == '':
            # Empty line represents new slide
            slides += ['']
            line_count = 0

        elif line_count < lines_per_slide:
            # Add line to current slide
            if line_count != 0: slides[-1] += '\n'
            slides[-1] += line
            line_count += 1

        else:
            # Overflow to new slide
            slides += [line]
            line_count = 1

    # Remove first/last slide if empty
    # len(slides) is always greater than 1 or single slide is not empty
    if slides[0] == '': slides = slides[1:]
    if slides[-1] == '': slides = slides[:-1]

    return slides
