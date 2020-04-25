# Songs2Slides
Creates a lyrics powerpoint from a list of songs. This program does NOT add any copyright information to the powerpoint. The user must do this manually.

## Features
Not all features are currently available in the web interface.
- Can parse any song given the artist and title.
- New slides are automatically started at the beginning of verses, bridges, choruses, etc.
- The user can easily review and edit the slides.
- The default powerpoint format may be changed at anytime in `Songs2Slides/config.py`.
- The slides can be added to a new or existing powerpoint.

## Usage
Install the python requirements.
```
pip install -r requirements.txt
```
To use the command line interface, run `cliapp.py`.
```
python cliapp.py
```
To use the web interface, run `webapp.py` and then go to https://localhost:5000 in your web browser.
```
python webapp.py
start https://localhost:5000
```