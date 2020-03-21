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