# Songs2Slides
Creates a lyrics powerpoint from a list of songs. This program does NOT add any copyright information to the powerpoint. The user must do this manually.

## Features
- Can parse any song given the artist and title.
- The lyrics are automatically split into slides.
- The user can easily review and edit the slides.
- The slides can be added to a new or existing powerpoint.

## Powerpoint Format
The default powerpoint format may be changed at anytime in `settings.json`.
- Each slide contains a single textblock with 0.5 inch margins.
- Text is 40pt Calibri and centered.
- Each slide contains 4 lines.
- Text wrap is enabled for long lines.
- New slides are automatically started at the beginning of verses, bridges, choruses, etc.
- A blank slide is added between each song.