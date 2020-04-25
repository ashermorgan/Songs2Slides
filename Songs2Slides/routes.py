# Import dependencies
from flask import render_template, request, send_file, url_for, jsonify
import io
import json
import os
from Songs2Slides import app, models, config
import tempfile



# Home page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")



# Get Powerpoint
@app.route("/pptx", methods=["POST"])
def pptx():
    # Parse POST parameters
    if "songs" in request.json:
        # Get lyrics
        lyrics = []
        for song in request.json["songs"]:
            try:
                parsedLyrics = models.ParseLyrics(models.GetLyrics(song[1], song[0]))
                if (config.parsing["title-slides"]):
                    lyrics += ["{0}\n{1}".format(song[0], song[1])]
                lyrics += parsedLyrics
                if (lyrics[-1] != ""):
                    lyrics += [""]
            except:
                pass
    elif "lyrics" in request.json:
        # Get lyrics
        lyrics = request.json["lyrics"]
    
    try:
        # Create powerpoint
        temp = tempfile.NamedTemporaryFile(mode="w+t", suffix=".pptx", delete=False)
        models.CreatePptx(lyrics, temp.name, False)
        temp.close()

        # Read file into stream
        with open(temp.name, 'rb') as f:
            pptx = io.BytesIO(f.read())
    finally:
        # Delete temp file
        os.remove(temp.name)
    
    # Return powerpoint
    return send_file(pptx, as_attachment=True, attachment_filename='download.pptx')



# Get lyrics
@app.route("/lyrics", methods=["POST"])
def lyrics():
    # Get lyrics
    lyrics = []
    for song in request.json["songs"]:
        try:
            parsedLyrics = models.ParseLyrics(models.GetLyrics(song[1], song[0]))
            if (config.parsing["title-slides"]):
                lyrics += ["{0}\n{1}".format(song[0], song[1])]
            lyrics += parsedLyrics
            if (lyrics[-1] != ""):
                lyrics += [""]
        except:
            pass
    
    # Return lyrics
    return jsonify({"lyrics": lyrics})