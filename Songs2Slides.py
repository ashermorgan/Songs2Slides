# Import dependencies
from bs4 import BeautifulSoup
import requests


# Gets the lyrics
def getLyrics(artist, song):
    artist = artist.replace(" ", "-")
    song = song.replace(" ", "-")
    page = requests.get("https://genius.com/{0}-{1}-lyrics".format(artist, song))
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    return lyrics


# Parses the lyrics into blocks
def ParseLyrics(lyrics):
    rawLines = lyrics.split("\n")
    lines = []
    BlockSize = 0
    for i in range(0, len(rawLines)):
        if (rawLines[i] == "" or rawLines[i][0] == "["):
            BlockSize = 4
        elif (BlockSize == 4):
            lines.append(rawLines[i])
            BlockSize = 1
        else:
            lines[-1] = lines[-1] + "\n" + rawLines[i]
            BlockSize += 1
    return lines