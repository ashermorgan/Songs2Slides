# Import dependencies
from bs4 import BeautifulSoup
import json
import os
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import requests
import subprocess
import sys
import tempfile


# Gets the lyrics
def GetLyrics(artist, song):
    # Convert to lowercase
    artist = artist.lower()
    song = song.lower()
    
    # Remove extra whitespace
    artist = ' '.join(artist.split())
    song = ' '.join(song.split())

    # Replace invalid characters
    old = [" ", "!", "@", "#", "$", "%", "^", "&",   "*", "(", ")", "+", "=", "'", "?", "/", "|", "\\", ".", ",", "á", "é", "í", "ó", "ñ", "ú"]
    new = ["-", "",  "",  "",  "s", "",  "-", "and", "",  "",  "",  "-", "-", "",  "",  "",  "",  "",   "",  "",  "a", "e", "i", "o", "n", "u"]
    for i in range(0, len(old)):
        artist = artist.replace(old[i], new[i])
        song = song.replace(old[i], new[i])

    # Get lyrics
    page = requests.get("https://genius.com/{0}-{1}-lyrics".format(artist, song))
    lyrics = BeautifulSoup(page.text, 'html.parser').find('div', class_='lyrics').get_text()
    
    # Return lyrics
    return lyrics


# Parses the lyrics into blocks
def ParseLyrics(lyrics):
    # Load settings
    with open("settings.json") as f:
        settings = json.load(f)
    
    # Parse lyrics
    rawLines = lyrics.split("\n")
    lines = []
    BlockSize = settings["lines-per-slide"]
    for i in range(0, len(rawLines)):
        if (rawLines[i] == "" or rawLines[i][0] == "["):
            # Start new block on the next line
            BlockSize = settings["lines-per-slide"]
        elif (BlockSize == settings["lines-per-slide"]):
            # Start a new block
            lines.append(rawLines[i])
            BlockSize = 1
        else:
            # Continue a block
            lines[-1] = lines[-1] + "\n" + rawLines[i]
            BlockSize += 1
    return lines


# Create powerpoint
def CreatePptx(parsedLyrics, filepath):
    # Load settings
    with open("settings.json") as f:
        settings = json.load(f)

    # Create presentation
    prs = Presentation()
    blank_slide_layout = prs.slide_layouts[6]
    
    for lyric in parsedLyrics:
        # Add slide
        slide = prs.slides.add_slide(blank_slide_layout)
    
        # Add text box
        left = Inches(settings["margin-left"])
        top = Inches(settings["margin-top"])
        width = Inches(10 - settings["margin-left"] - settings["margin-right"])
        height = Inches(7.5 - settings["margin-top"] - settings["margin-bottom"])
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.clear()
        tf.word_wrap = settings["word-wrap"]
    
        # Add pharagraph
        p = tf.paragraphs[0]
        p.text = lyric
        p.font.name = settings["font-family"]
        p.font.size = Pt(settings["font-size"])
        p.font.bold = settings["font-bold"]
        p.font.italic = settings["font-italic"]
        p.font.color.rgb = RGBColor(settings["font-color"][0], settings["font-color"][1], settings["font-color"][2])
        p.alignment = PP_ALIGN.CENTER
        p.line_spacing = settings["line-spacing"]

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
            lyrics += ParseLyrics(GetLyrics(artist, title))
            if (lyrics[-1] != ""):
                lyrics += [""]
        except:
            print("We couldn't find the lyrics to that song.")
            song -= 1
        
        # Add more songs
        if (song >= 1 and input("Do you want to add another song? (y/n): ").lower() == "n"):
            break
        song += 1
    
    # Review lyrics
    if (input("Would you like to review the parsed lyrics first? (y/n): ").lower() == "y"):
        try:
            # Create temp file
            temp = tempfile.NamedTemporaryFile(mode='w+t', suffix=".txt", delete=False)
            for line in lyrics:
                temp.writelines(line)
                temp.writelines("\n\n")
            temp.close()
            
            # Open temp file and wait
            subprocess.Popen(["notepad", temp.name]).wait()

            # Read file
            with open(temp.name) as f:
                rawLines = f.read()

            # Parse lyrics
            lyrics = []
            for song in rawLines.split("\n\n\n"):
                lyrics += ParseLyrics(song)
                if (lyrics[-1] != ""):
                    lyrics += [""]
        finally:
            # Delete temp file
            os.remove(temp.name)

    
    # Get filepath
    filepath = input("Please enter a filepath to save your powerpoint to: ")

    # Add extension
    if (len(filepath) == 0):
        filepath = "Untitled.pptx"
    elif (len(filepath) < 4):
        filepath += ".pptx"
    elif (len(filepath) == 4 and filepath[-4:] != ".ppt"):
        filepath += ".pptx"
    elif (len(filepath) > 4 and filepath[-5:] != ".pptx" and filepath[-4:] != ".ppt"):
        filepath += ".pptx"

    # Create powerpoint
    try:
        CreatePptx(lyrics, filepath)
    except:
        print("We were unable to create the powerpoint.")
        sys.exit()
    
    # Open powerpoint
    if (input("Do you want to view your powerpoint now? (y/n): ").lower() == "y"):
        os.startfile(filepath)
