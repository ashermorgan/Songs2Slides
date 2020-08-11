# Contains default parsing and PowerPoint settings
defaultSettings = {
    # Parsing settings
    "title-slides": True,
    "slide-between-songs": True,
    "lines-per-slide": 4,
    "remove-parentheses": False,

    # Slide settings
    "slide-width": 13.333,
    "slide-height": 7.5,
    "slide-color": "#000000",
    
    # Margin settings
    "margin-left": 0.5,
    "margin-right": 0.5,
    "margin-top": 0.5,
    "margin-bottom": 0.5,

    # Font settings
    "font-family": "Calibri",
    "font-size": 40,
    "font-bold": False,
    "font-italic": False,
    "font-color": "#FFFFFF",

    # Paragraph settings
    "vertical-alignment": "Middle", # Can be Top, Middle, or Bottom
    "line-spacing": 1.25,
    "word-wrap": True
}



# Contains cached and custom song information
cachedSongs = {
    # Keys should be lowercase ASCII strings without whitespace or special characters
    "testartist-testsong": {
        # Title and Artist of the song (formated however you want)
        "title":"Test Song",
        "artist":"Test Artist",

        # Lyrics with two newlines between each stanza and no newlines at the beginning or end
        "lyrics":"test1\ntest2\n\ntest3\ntest4"
    }
}
