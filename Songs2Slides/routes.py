# Import dependencies
from flask import render_template, request, send_file, url_for
import io
import json
import os
from Songs2Slides import app, models, config
import tempfile



# Home page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")



# Powerpoint download
@app.route("/pptx", methods=["POST"])
def pptx():
    # Parse POST parameters
    data = json.loads(request.form["data"])
    
    # Get lyrics
    lyrics = []
    for song in data:
        try:
            lyrics += models.ParseLyrics(song[0], song[1])
        except:
            pass
    
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
