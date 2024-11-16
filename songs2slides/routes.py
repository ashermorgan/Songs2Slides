from flask import abort, Blueprint, redirect, render_template, request, \
    send_file, url_for
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
def create_root():
    return redirect(url_for('.create_step_1'), 301)

@bp.get('/create/step-1/')
def create_step_1():
    return render_template('create-step-1.html')

@bp.get('/create/step-2/')
def create_step_2_get():
    # GET requests not allowed, redirect to step 1
    return redirect(url_for('.create_step_1'), 302)

@bp.post('/create/step-2/')
def create_step_2():
    # Parse form data
    songs = parse_form(request.form)

    # Get lyrics
    api_error = True # Whether an API error occured for all requests
    for i in range(len(songs)):
        try:
            songs[i] = core.get_song_data(songs[i].title, songs[i].artist)
            api_error = False
            slides = core.parse_song_lyrics(songs[i].lyrics, 4)
            songs[i].lyrics = '\n\n'.join(slides)
        except core.SongNotFound:
            api_error = False
        except Exception as e:
            pass

    # Count missing songs
    missing = sum([1 for x in songs if x.lyrics == None])

    # Return song data
    return render_template('create-step-2.html', songs=songs, missing=missing,
                           api_error=api_error)

@bp.get('/create/step-3/')
def create_step_3_get():
    # GET requests not allowed, redirect to step 1
    return redirect(url_for('.create_step_1'), 302)

@bp.post('/create/step-3/')
def create_step_3():
    # Parse form data
    songs = parse_form(request.form)

    # Return song data
    return render_template('create-step-3.html', songs=songs)

@bp.get('/post-download/')
def post_download():
    return render_template('post-download.html')

@bp.get('/slides/')
def slides_get():
    # GET requests not allowed, redirect to home page
    return redirect(url_for('.home'), 302)

@bp.post('/slides/')
def slides():
    # Parse form data
    songs = parse_form(request.form)
    title_slides = 'title-slides' in request.form
    blank_slides = 'blank-slides' in request.form

    # Assemble slides
    slides = core.assemble_slides(songs, lines_per_slide = None,
        title_slides=title_slides, blank_slides=blank_slides)

    if (request.form.get('output-type') == 'pptx'):
        # Create and send powerpoint
        with tempfile.NamedTemporaryFile(suffix='.pptx') as f:
            core.create_pptx(slides, f.name)
            return send_file(f.name, as_attachment=True,
                             download_name='slides.pptx')
    else:
        # Render HTML slides
        return render_template('slides.html', slides=slides)
