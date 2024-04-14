import pytest

from songs2slides import create_app, core, routes

@pytest.fixture(autouse=True)
def client():
    app = create_app()
    return app.test_client()

def test_get_lyrics_basic(client, mocker):
    # Mock get_song_data, parse_song_lyrics, and render_template
    mocker.patch('songs2slides.core.get_song_data')
    mocker.patch('songs2slides.core.parse_song_lyrics')
    mocker.patch('songs2slides.routes.render_template')
    songs = [
        core.SongData('T1', 'A1', 'L1'),
        core.SongData('T2', 'A2', 'L2'),
    ]
    core.get_song_data.side_effect = songs
    core.parse_song_lyrics.side_effect = ['L1', 'L2']

    # Send request
    client.post('/create/step-2/', data={
        'title-1': 'T1',
        'artist-1': 'A1',
        'title-2': 'T2',
        'artist-2': 'A2',
    })

    # Assert mocks called correctly
    core.get_song_data.assert_has_calls([
        mocker.call('T1', 'A1'), mocker.call('T2', 'A2')
    ])
    core.parse_song_lyrics.assert_has_calls([
        mocker.call('L1', 4), mocker.call('L2', 4)
    ])
    routes.render_template.assert_called_with('create-step-2.html',
        songs=songs, missing=0)

def test_get_lyrics_one_error(client, mocker):
    # Mock get_song_data, parse_song_lyrics, and render_template
    mocker.patch('songs2slides.core.get_song_data')
    mocker.patch('songs2slides.core.parse_song_lyrics')
    mocker.patch('songs2slides.routes.render_template')
    songs = [
        core.SongData('T1', 'A1', None),
        core.SongData('T2', 'A2', 'L2'),
    ]
    core.get_song_data.side_effect = [Exception(), songs[1]]
    core.parse_song_lyrics.side_effect = ['L1', 'L2']

    # Send request
    client.post('/create/step-2/', data={
        'title-1': 'T1',
        'artist-1': 'A1',
        'title-2': 'T2',
        'artist-2': 'A2',
    })

    # Assert mocks called correctly
    core.get_song_data.assert_has_calls([
        mocker.call('T1', 'A1'), mocker.call('T2', 'A2')
    ])
    core.parse_song_lyrics.assert_has_calls([mocker.call('L2', 4)])
    routes.render_template.assert_called_with('create-step-2.html', songs=songs, missing=1)

def test_get_lyrics_missing_artist(client, mocker):
    # Mock get_song_data
    mocker.patch('songs2slides.core.get_song_data')

    # Send request
    res = client.post('/create/step-2/', data={
        'title-1': 'T1',
        'title-2': 'T2',
        'artist-2': 'A2',
    })

    # Assert mocks not called
    core.get_song_data.assert_not_called()

    # Assert response has 400 status code
    assert res.status_code == 400

def test_update_lyrics(client, mocker):
    # Mock render_template
    mocker.patch('songs2slides.routes.render_template')

    # Send request
    client.post('/create/step-3/', data={
        'title-1': 'T1',
        'artist-1': 'A1',
        'lyrics-1': 'L1',
        'title-2': 'T2',
        'artist-2': 'A2',
        'lyrics-2': 'L2',
        'output-type': 'html',
        'title-slides': 'on',
    })

    # Assert render_template called correctly
    routes.render_template.assert_called_with('create-step-3.html', songs=[
        core.SongData('T1', 'A1', 'L1'),
        core.SongData('T2', 'A2', 'L2'),
    ])

def test_create_slides_basic(client, mocker):
    # Mock assemble_slides, create_pptx, and send_file
    mocker.patch('songs2slides.core.assemble_slides')
    mocker.patch('songs2slides.core.create_pptx')
    mocker.patch('songs2slides.routes.send_file')

    # Send request
    client.post('/slides/', data={
        'title-1': 'T1',
        'artist-1': 'A1',
        'lyrics-1': 'L1',
        'title-2': 'T2',
        'artist-2': 'A2',
        'lyrics-2': 'L2',
        'output-type': 'pptx',
        'title-slides': 'on',
        'blank-slides': 'on',
    })

    # Assert mocks called correctly
    core.assemble_slides.assert_called_with([
            core.SongData('T1', 'A1', 'L1'),
            core.SongData('T2', 'A2', 'L2'),
        ],
        lines_per_slide = None,
        title_slides = True,
        blank_slides = True,
    )
    file = core.create_pptx.call_args.args[1]
    routes.send_file.assert_called_with(file, as_attachment=True,
                                   download_name='slides.pptx')

def test_create_slides_mising_artist(client, mocker):
    # Mock assemble_slides
    mocker.patch('songs2slides.core.assemble_slides')

    # Send request
    res = client.post('/slides/', data={
        'title-1': 'T1',
        'artist-1': 'A1',
        'lyrics-1': 'L1',
        'title-2': 'T2',
        'lyrics-2': 'L2',
        'output-type': 'pptx',
        'title-slides': 'on',
        'blank-slides': 'on',
    })

    # Assert response has 400 status code
    assert res.status_code == 400

    # Assert assemble_slides not called
    core.assemble_slides.assert_not_called()

def test_create_slides_html_slides(client, mocker):
    # Mock assemble_slides, create_pptx, render_template
    mocker.patch('songs2slides.core.assemble_slides')
    mocker.patch('songs2slides.core.create_pptx')
    mocker.patch('songs2slides.routes.render_template')
    slides = ['T1', 'L1\nL2', 'L3', 'T2', 'L4']
    core.assemble_slides.return_value = slides

    # Send request
    client.post('/slides/', data={
        'title-1': 'T1',
        'artist-1': 'A1',
        'lyrics-1': 'L1',
        'title-2': 'T2',
        'artist-2': 'A2',
        'lyrics-2': 'L2',
        'output-type': 'html',
        'title-slides': 'on',
        'blank-slides': 'on',
    })

    # Assert mocks called correctly
    core.assemble_slides.assert_called_with([
            core.SongData('T1', 'A1', 'L1'),
            core.SongData('T2', 'A2', 'L2'),
        ],
        lines_per_slide = None,
        title_slides = True,
        blank_slides = True,
    )
    core.create_pptx.assert_not_called()
    routes.render_template.assert_called_with('slides.html', slides=slides)

def test_create_slides_no_title_slides(client, mocker):
    # Mock assemble_slides, create_pptx, render_template
    mocker.patch('songs2slides.core.assemble_slides')
    mocker.patch('songs2slides.core.create_pptx')
    mocker.patch('songs2slides.routes.render_template')
    slides = ['T1', 'L1\nL2', 'L3', 'T2', 'L4']
    core.assemble_slides.return_value = slides

    # Send request
    client.post('/slides/', data={
        'title-1': 'T1',
        'artist-1': 'A1',
        'lyrics-1': 'L1',
        'title-2': 'T2',
        'artist-2': 'A2',
        'lyrics-2': 'L2',
        'output-type': 'html',
        'blank-slides': 'on',
    })

    # Assert mocks called correctly
    core.assemble_slides.assert_called_with([
            core.SongData('T1', 'A1', 'L1'),
            core.SongData('T2', 'A2', 'L2'),
        ],
        lines_per_slide = None,
        title_slides = False,
        blank_slides = True,
    )
    core.create_pptx.assert_not_called()
    routes.render_template.assert_called_with('slides.html', slides=slides)

def test_create_slides_no_blank_slides(client, mocker):
    # Mock assemble_slides, create_pptx, render_template
    mocker.patch('songs2slides.core.assemble_slides')
    mocker.patch('songs2slides.core.create_pptx')
    mocker.patch('songs2slides.routes.render_template')
    slides = ['T1', 'L1\nL2', 'L3', 'T2', 'L4']
    core.assemble_slides.return_value = slides

    # Send request
    client.post('/slides/', data={
        'title-1': 'T1',
        'artist-1': 'A1',
        'lyrics-1': 'L1',
        'title-2': 'T2',
        'artist-2': 'A2',
        'lyrics-2': 'L2',
        'output-type': 'html',
        'title-slides': 'on',
    })

    # Assert mocks called correctly
    core.assemble_slides.assert_called_with([
            core.SongData('T1', 'A1', 'L1'),
            core.SongData('T2', 'A2', 'L2'),
        ],
        lines_per_slide = None,
        title_slides = True,
        blank_slides = False,
    )
    core.create_pptx.assert_not_called()
    routes.render_template.assert_called_with('slides.html', slides=slides)
