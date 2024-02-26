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

@bp.post('/slides/')
def slides():
    # Parse form data
    songs = parse_form(request.form)

    # Assemble slides
    slides = core.assemble_slides(songs, lines_per_slide = None)

    # Create and send powerpoint
    with tempfile.NamedTemporaryFile(suffix='.pptx') as f:
        core.create_pptx(slides, f.name)
        return send_file(f.name, as_attachment=True,
                         download_name='slides.pptx')
