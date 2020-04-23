# Import dependencies
from bs4 import BeautifulSoup
from Songs2Slides import config
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt
import requests



# Gets the lyrics
def GetLyrics(artist, song):
    # Convert to lowercase
    artist = artist.lower()
    song = song.lower()

    # Replace invalid characters
    old = [" ", "!", "@", "#", "$", "%", "^", "&",     "*", "(", ")", "+", "=", "'", "?", "/", "|", "\\", ".", ",", "á", "é", "í", "ó", "ñ", "ú"]
    new = ["-", "",  "",  "",  "s", "",  "-", "-and-", "",  "",  "",  "-", "-", "",  "",  "",  "",  "",   "",  "",  "a", "e", "i", "o", "n", "u"]
    for i in range(0, len(old)):
        artist = artist.replace(old[i], new[i])
        song = song.replace(old[i], new[i])
    
    # Remove unnecessary dashes
    artist = "-".join(list(filter(lambda a: a != "", artist.split("-"))))
    song   = "-".join(list(filter(lambda a: a != "", song.split("-"))))

    # Get lyrics
    page = requests.get("https://genius.com/{0}-{1}-lyrics".format(artist, song))
    lyrics = BeautifulSoup(page.text, "html.parser").find("div", class_="lyrics").get_text()
    
    # Return lyrics
    return lyrics



# Parses the lyrics into blocks
def ParseLyrics(lyrics):
    # Split lyrics
    rawLines = lyrics.split("\n")

    # Remove starting and ending newlines
    del rawLines[0]
    del rawLines[0]
    del rawLines[-1]
    del rawLines[-1]

    # Parse lyrics into lines
    lines = []
    slideSize = config.parsing["lines-per-slide"]
    for i in range(0, len(rawLines)):
        if (rawLines[i] == ""):
            # Start a new slide without content
            lines.append("")
            slideSize = 0
        elif (rawLines[i][0] == "["):
            # Ignore
            pass
        elif (slideSize == config.parsing["lines-per-slide"]):
            # Start a new slide with content
            lines.append(rawLines[i])
            slideSize = 1
        elif (slideSize == 0):
            # Continue a blank slide
            lines[-1] = lines[-1] + rawLines[i]
            slideSize += 1
        else:
            # Continue a slide
            lines[-1] = lines[-1] + "\n" + rawLines[i]
            slideSize += 1
    return lines



# Create powerpoint
def CreatePptx(parsedLyrics, filepath, openFirst):
    if (openFirst):
        try:
            # Open presentation
            prs = Presentation(filepath)
        except:
            # Create presentation
            prs = Presentation()

            # Set slide width and height
            prs.slide_width = Inches(config.slide["width"])
            prs.slide_height = Inches(config.slide["height"])
    else:
        # Create presentation
        prs = Presentation()

        # Set slide width and height
        prs.slide_width = Inches(config.slide["width"])
        prs.slide_height = Inches(config.slide["height"])
    
    # Get blank slide
    blank_slide_layout = prs.slide_layouts[6]
    
    # Get margins
    left = Inches(config.margin["left"])
    top = Inches(config.margin["top"])
    width = prs.slide_width - Inches(config.margin["left"] + config.margin["right"])
    height = prs.slide_height - Inches(config.margin["top"] + config.margin["bottom"])
    
    for lyric in parsedLyrics:
        # Add slide
        slide = prs.slides.add_slide(blank_slide_layout)
        
        # Apply slide formating
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = RGBColor(config.slide["color"][0], config.slide["color"][1], config.slide["color"][2])
        
        # Add text box
        txBox = slide.shapes.add_textbox(left, top, width, height)
        tf = txBox.text_frame
        tf.clear()

        # Apply text formating
        tf.word_wrap = config.paragraph["word-wrap"]
        if (config.paragraph["vertical-alignment"].lower() == "top"):
            tf.vertical_anchor = MSO_ANCHOR.TOP
        elif (config.paragraph["vertical-alignment"].lower() == "bottom"):
            tf.vertical_anchor = MSO_ANCHOR.BOTTOM
        else:
            tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    
        # Add pharagraph
        p = tf.paragraphs[0]
        p.text = lyric

        # Apply pharagraph formating
        p.font.name = config.font["family"]
        p.font.size = Pt(config.font["size"])
        p.font.bold = config.font["bold"]
        p.font.italic = config.font["italic"]
        p.font.color.rgb = RGBColor(config.font["color"][0], config.font["color"][1], config.font["color"][2])
        p.alignment = PP_ALIGN.CENTER
        p.line_spacing = config.paragraph["line-spacing"]

    # Save powerpoint
    prs.save(filepath)