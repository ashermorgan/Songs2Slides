# Import dependencies
from copy import deepcopy
from flask import render_template, request, send_file, url_for, jsonify
import io
import json
import os
from Songs2Slides import app, core
from Songs2Slides.config import defaultSettings
import tempfile



# Home page
@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")



# Settings page
@app.route("/settings/", methods=["GET"])
def settings():
    return render_template("settings.html", title = "Settings")



# Settings JSON file
@app.route("/settings.json", methods=["GET"])
def settingsJSON():
    return jsonify(defaultSettings)



# Get Powerpoint
@app.route("/pptx", methods=["POST"])
def pptx():
    # Get settings
    settings = deepcopy(defaultSettings)
    try:
        for setting in request.json["settings"]:
            settings[setting] = request.json["settings"][setting]
    except:
        pass

    try:
        # Get temp
        temp = tempfile.NamedTemporaryFile(mode="w+t", suffix=".pptx", delete=False)
        temp.close()

        # Get lyrics
        lyrics = json.loads(request.form["lyrics"])

        # Save uploaded powerpoint
        if (request.files["pptxFile"].filename != ""):
            request.files["pptxFile"].save(temp.name)

        # Create powerpoint
        core.CreatePptx(lyrics, temp.name, settings, True)

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
    # Get settings
    settings = deepcopy(defaultSettings)
    try:
        for setting in request.json["settings"]:
            settings[setting] = request.json["settings"][setting]
    except:
        pass

    # Get lyrics
    lyrics = []
    failed = []
    for song in request.json["songs"]:
        try:
            lyrics += core.ParseLyrics(song[0], song[1], settings)
        except:
            failed += [song]
    
    # Return lyrics
    return jsonify({"lyrics": lyrics, "errors": failed})
