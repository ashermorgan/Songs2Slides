from flask import abort, Blueprint, render_template, request, send_file
import tempfile

from songs2slides import core

bp = Blueprint('main', __name__)

def parse_form(form):
    """
    Parse song data from a form

    Parameters
    ----------
    form : flask.Request.form
        The form data

    Returns
    -------
    list of core.SongData
        The parsed song information
    """

    songs = []
    try:
        i = 1
        while f'title-{i}' in request.form:
            songs += [core.SongData(
                form[f'title-{i}'],
                form[f'artist-{i}'],
                form.get(f'lyrics-{i}', None)
            )]
            i += 1
    except:
        abort(400)
    else:
        return songs

@bp.route('/')
def home():
    return render_template('home.html')

@bp.get('/create/')
def create():
    return render_template('create-step-1.html')

@bp.post('/create/')
def get_lyrics():
    # Parse form data
    songs = parse_form(request.form)

    # Get lyrics
    for i in range(len(songs)):
        try:
            songs[i] = core.get_song_data(songs[i].title, songs[i].artist)
            slides = core.parse_song_lyrics(songs[i].lyrics, 4)
            songs[i].lyrics = '\n\n'.join(slides)
        except:
            pass

    # Count missing songs
    missing = sum([1 for x in songs if x.lyrics == None])

    # Return song data
    return render_template('create-step-2.html', songs=songs, missing=missing)

@bp.post('/slides/')
def create_slides():
    # Parse form data
    songs = parse_form(request.form)

    # Assemble slides
    slides = core.assemble_slides(songs, lines_per_slide = None)

    if (request.form.get('output-type') == 'pptx'):
        # Create and send powerpoint
        with tempfile.NamedTemporaryFile(suffix='.pptx') as f:
            core.create_pptx(slides, f.name)
            return send_file(f.name, as_attachment=True,
                             download_name='slides.pptx')
    else:
        # Render HTML slides
        return render_template('slides.html', slides=slides)
