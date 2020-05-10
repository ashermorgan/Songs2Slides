# Import dependencies
from flask import render_template, request, send_file, url_for, jsonify
import io
import json
import os
from Songs2Slides import app, models
from Songs2Slides.config import defaultSettings
import tempfile



# Home page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")



# Get Powerpoint
@app.route("/pptx", methods=["POST"])
def pptx():
    if "songs" in request.json:
        lyrics = []
        for song in request.json["songs"]:
          try:
              lyrics += models.ParseLyrics(song[0], song[1], defaultSettings)
          except:
              pass
    elif "lyrics" in request.json:
        # Get lyrics
        lyrics = request.json["lyrics"]
    
    try:
        # Create powerpoint
        temp = tempfile.NamedTemporaryFile(mode="w+t", suffix=".pptx", delete=False)
        models.CreatePptx(lyrics, temp.name, defaultSettings, False)
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
            lyrics += models.ParseLyrics(song[0], song[1], defaultSettings)
        except:
            pass
    
    # Return lyrics
    return jsonify({"lyrics": lyrics})
