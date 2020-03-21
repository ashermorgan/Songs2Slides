# Import dependencies
from bs4 import BeautifulSoup
import os
import requests
from pptx import Presentation
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


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


# Create powerpoint
def CreatePptx(parsedLyrics, filepath):
    # Create presentation
    prs = Presentation()
    blank_slide_layout = prs.slide_layouts[6]
    
    for lyric in parsedLyrics:
        # Add slide
        slide = prs.slides.add_slide(blank_slide_layout)
    
        # Add text box
        left = Inches(0.5)
        top = Inches(0.5)
        width = Inches(9)
        height = Inches(6.5)
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.clear()
        tf.word_wrap = True
    
        # Add pharagraph
        p = tf.paragraphs[0]
        p.text = lyric
        p.font.size = Pt(40)
        p.alignment = PP_ALIGN.CENTER
        p.line_spacing = 1.25

    # Save powerpoint
    prs.save(filepath)


# Run CLI
if (__name__ == "__main__"):
    # Print title
    print("Songs2Slides")
    print()

    # Get song lyrics
    lyrics = []
    song = 1
    while (True):
        # Get song information
        title = input("Song #{0} Title: ".format(song))
        artist = input("Song #{0} Artist: ".format(song))
        
        # Get song lyrics
        try:
            lyrics += ParseLyrics(getLyrics(artist, title))
            lyrics += [""]
        except:
            print("We couldn't find the lyrics to that song.")
        
        # Add more songs
        if (input("Do you want to add another song? (y/n): ").lower() == "n"):
            break
        song += 1
    
    # Get filepath
    filepath = input("Please enter a filepath to save your powerpoint to: ")

    # Create powerpoint
    CreatePptx(lyrics, filepath)

    # Open powerpoint
    if (input("Do you want to view your powerpoint now? (y/n): ").lower() == "y"):
        os.startfile(filepath)
