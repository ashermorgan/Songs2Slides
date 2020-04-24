# Import dependencies
import json
import os
from Songs2Slides import models, config
import subprocess
import sys
import tempfile



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
            parsedLyrics = models.ParseLyrics(models.GetLyrics(artist, title))
            if (config.parsing["title-slides"]):
                lyrics += ["{0}\n{1}".format(title, artist)]
            lyrics += parsedLyrics
            if (lyrics[-1] != ""):
                lyrics += [""]
        except:
            print("The song could not be found. Make sure that you spelled it correctly.")
            song -= 1
        
        # Add more songs
        if (song >= 1 and input("Do you want to add another song? (y/n): ").lower() == "n"):
            break
        else:
            song += 1
    
    # Review lyrics
    if (input("Do you want to review the parsed lyrics first? (y/n): ").lower() == "y"):
        try:
            # Create temp file
            temp = tempfile.NamedTemporaryFile(mode="w+t", suffix=".txt", delete=False)
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
            newLyrics = rawLines.split("\n\n")
            del newLyrics[-1]
            lyrics = newLyrics
        except:
            print("There was an error while reviewing the lyrics. The unrevised lyrics will be used instead.")
        finally:
            # Delete temp file
            os.remove(temp.name)

    # Get filepath
    filepath = input("Enter a filepath to save the powerpoint to: ")

    # Add extension
    if (len(filepath) == 0):
        filepath = "Untitled.pptx"
    elif (len(filepath) < 4):
        filepath += ".pptx"
    elif (len(filepath) == 4 and filepath[-4:] != ".ppt"):
        filepath += ".pptx"
    elif (len(filepath) > 4 and filepath[-5:] != ".pptx" and filepath[-4:] != ".ppt"):
        filepath += ".pptx"

    # Confirm overwrite
    if (os.path.exists(filepath)):
        openFirst = (input("This powerpoint already exists. Do you want to add on to it? (y/n): ").lower() == "y")
    else:
        openFirst = False

    # Create powerpoint
    try:
        models.CreatePptx(lyrics, filepath, openFirst)
    except:
        print("There was an error while creating the powerpoint.")
        input("Press enter to exit...")
        sys.exit()
    
    # Open powerpoint
    if (input("Do you want to view the powerpoint now? (y/n): ").lower() == "y"):
        try:
            os.startfile(filepath)
        except:
            print("There was an error while opening the powerpoint.")
            input("Press enter to exit...")
            sys.exit()