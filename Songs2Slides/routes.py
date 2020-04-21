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