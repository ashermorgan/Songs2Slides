import pytest

from songs2slides import core

def test_filter_lyrics_inline():
    # Declare raw lyrics and expected cleaned lyrics
    lyrics = 'A[remove]B\nC(remove)D'
    expected = 'AB\nCD'

    # Clean lyrics
    result = core.filter_lyrics(lyrics)

    # Assert slides are correct
    assert result == expected

def test_filter_lyrics_whole_lines():
    # Declare raw lyrics and expected cleaned lyrics
    lyrics = 'A\n[remove]\nB\n(remove)\nC'
    expected = 'A\nB\nC'

    # Clean lyrics
    result = core.filter_lyrics(lyrics)

    # Assert slides are correct
    assert result == expected

def test_filter_lyrics_multiple_lines():
    # Declare raw lyrics and expected cleaned lyrics
    lyrics = 'A\n[re\nmove]\nB\n(re\nmove)\nC'
    expected = 'A\nB\nC'

    # Clean lyrics
    result = core.filter_lyrics(lyrics)

    # Assert slides are correct
    assert result == expected

def test_filter_lyrics_blank_lines():
    # Declare raw lyrics and expected cleaned lyrics
    lyrics = 'A\n[remove]\n\n(remove)\nB'
    expected = 'A\n\nB'

    # Clean lyrics
    result = core.filter_lyrics(lyrics)

    # Assert slides are correct
    assert result == expected

def test_filter_lyrics_all():
    # Declare raw lyrics and expected cleaned lyrics
    lyrics = 'A[remove]B\n[remove]\n\nC(remove)D\n(re\nmove)'
    expected = 'AB\n\nCD'

    # Clean lyrics
    result = core.filter_lyrics(lyrics)

    # Assert slides are correct
    assert result == expected

def test_filter_lyrics_empty_string():
    # Clean lyrics
    result = core.filter_lyrics('')

    # Assert slides are correct
    assert result == ''

def test_get_song_data_success(mocker):
    # Mock os.getenv, requests.get, and filter_lyrics
    mocker.patch('songs2slides.core.os.getenv')
    mocker.patch('songs2slides.core.requests.get')
    mocker.patch('songs2slides.core.filter_lyrics')
    core.os.getenv.side_effect = [
        'api://lyrics/{artist}/{title}',
        'Bearer secrettoken'
    ]
    core.requests.get.return_value.json.return_value = {
        'lyrics': 'raw',
        'title': 'Foo',
        'artist': 'Bar',
    }
    core.requests.get.return_value.status_code = 200
    core.filter_lyrics.return_value = 'clean'

    # Get song data
    song_data = core.get_song_data('foo', 'bar')

    # Assert mocked methods were used correctly
    core.os.getenv.assert_has_calls([
        mocker.call('API_URL'),
        mocker.call('API_AUTH', None)
    ])
    core.requests.get.assert_called_with('api://lyrics/bar/foo', headers={
        'Authorization': 'Bearer secrettoken'
    })
    core.filter_lyrics.assert_called_with('raw')

    # Assert song data is correct
    assert song_data.title == 'Foo'
    assert song_data.artist == 'Bar'
    assert song_data.lyrics == 'clean'

def test_get_song_data_no_auth_header(mocker):
    # Mock os.getenv, requests.get, and filter_lyrics
    mocker.patch('songs2slides.core.os.getenv')
    mocker.patch('songs2slides.core.requests.get')
    mocker.patch('songs2slides.core.filter_lyrics')
    core.os.getenv.side_effect = [
        'api://lyrics/{artist}/{title}',
        None,
    ]
    core.requests.get.return_value.json.return_value = {
        'lyrics': 'raw',
        'title': 'Foo',
        'artist': 'Bar',
    }
    core.requests.get.return_value.status_code = 200
    core.filter_lyrics.return_value = 'clean'

    # Get song data
    song_data = core.get_song_data('foo', 'bar')

    # Assert mocked methods were used correctly
    core.os.getenv.assert_has_calls([
        mocker.call('API_URL'),
        mocker.call('API_AUTH', None)
    ])
    core.requests.get.assert_called_with('api://lyrics/bar/foo', headers={})
    core.filter_lyrics.assert_called_with('raw')

    # Assert song data is correct
    assert song_data.title == 'Foo'
    assert song_data.artist == 'Bar'
    assert song_data.lyrics == 'clean'

def test_get_song_data_no_url(mocker):
    # Mock os.getenv and requests.get
    mocker.patch('songs2slides.core.os.getenv')
    mocker.patch('songs2slides.core.requests.get')
    core.os.getenv.return_value = None
    core.requests.get.return_value.text = b'{}'
    core.requests.get.return_value.status_code = 200

    # Try to get song data
    with pytest.raises(Exception):
        song_data = core.get_song_data('foo', 'bar')

    # Assert request was not called
    core.requests.get.assert_not_called()

def test_get_song_data_not_found(mocker):
    # Mock os.getenv and requests.get
    mocker.patch('songs2slides.core.os.getenv')
    mocker.patch('songs2slides.core.requests.get')
    core.os.getenv.side_effect = [
        'api://lyrics/{artist}/{title}',
        'Bearer secrettoken'
    ]
    core.requests.get.return_value.text = b'{}'
    core.requests.get.return_value.status_code = 200

    # Try to get song data
    with pytest.raises(Exception):
        song_data = core.get_song_data('foo', 'bar')

    # Assert request was called
    core.requests.get.assert_called_with('api://lyrics/bar/foo', headers={
        'Authorization': 'Bearer secrettoken'
    })

def test_parse_song_lyrics_basic():
    # Declare song data and expected slides
    lyrics = 'A\nB\nC\nD\nE\nF\n\nG\nH'
    expected = ['A\nB\nC\nD', 'E\nF', 'G\nH']

    # Get slide content
    result = core.parse_song_lyrics(lyrics, 4)

    # Assert slides are correct
    assert result == expected

def test_parse_song_lyrics_3_lines_per_slide():
    # Declare song data and expected slides
    lyrics = 'A\nB\nC\nD\nE\nF\n\nG\nH'
    expected = ['A\nB\nC', 'D\nE\nF', 'G\nH']

    # Get slide content
    result = core.parse_song_lyrics(lyrics, 3)

    # Assert slides are correct
    assert result == expected

def test_parse_song_lyrics_empty_string():
    # Declare song data and expected slides
    lyrics = ''
    expected = []

    # Get slide content
    result = core.parse_song_lyrics(lyrics, 4)

    # Assert slides are correct
    assert result == expected

def test_parse_song_lyrics_one_line():
    # Declare song data and expected slides
    lyrics = 'A'
    expected = ['A']

    # Get slide content
    result = core.parse_song_lyrics(lyrics, 4)

    # Assert slides are correct
    assert result == expected

def test_parse_song_lyrics_one_slide():
    # Declare song data and expected slides
    lyrics = 'A\nB\nC\nD'
    expected = ['A\nB\nC\nD']

    # Get slide content
    result = core.parse_song_lyrics(lyrics, 4)

    # Assert slides are correct
    assert result == expected

def test_parse_song_lyrics_tripple_newlines():
    # Declare song data and expected slides
    lyrics = 'A\nB\n\n\nC\nD'
    expected = ['A\nB', '', 'C\nD']

    # Get slide content
    result = core.parse_song_lyrics(lyrics, 4)

    # Assert slides are correct
    assert result == expected

def test_parse_song_lyrics_extra_whitespace():
    # Declare song data and expected slides
    lyrics = ' A\n B \nC D\nE '
    expected = ['A\nB\nC D\nE']

    # Get slide content
    result = core.parse_song_lyrics(lyrics, 4)

    # Assert slides are correct
    assert result == expected

def test_parse_song_lyrics_extra_newlines():
    # Declare song data and expected slides
    lyrics = '\n\n\nA\n\n\n\n\nB\n\n\n'
    expected = ['A', '', 'B']

    # Get slide content
    result = core.parse_song_lyrics(lyrics, 4)

    # Assert slides are correct
    assert result == expected

def test_assemble_slides_calls_parse_song_lyrics(mocker):
    # Mock parse_song_lyrics
    mocker.patch('songs2slides.core.parse_song_lyrics')
    core.parse_song_lyrics.side_effect = [['aaa'], ['b1', 'b2']]

    # Declare song data and expected slides
    songs = [
        core.SongData('T1', 'A1', 'l1'),
        core.SongData('T2', 'A3', 'l2'),
        ]
    expected = ['T1', 'aaa', '', 'T2', 'b1', 'b2']

    # Get slides
    slides = core.assemble_slides(songs)

    # Assert slides are correct
    assert slides == expected

    # Assert parse_song_lyrics called
    core.parse_song_lyrics.assert_has_calls([
        mocker.call('L1', 4), mocker.call('L2', 4)
    ])

def test_assemble_slides_default():
    # Declare song data and expected slides
    songs = [
        core.SongData('t1', 'a1', 'l1\nl2\nl3\nl4\nl5'),
        core.SongData('T2', 'A3', 'L6\nL7\n\nL8\n\n\nL9'),
    ]
    expected = [
        'T1', 'L1\nL2\nL3\nL4', 'L5', '',
        'T2', 'L6\nL7', 'L8', '', 'L9',
    ]

    # Get slides
    slides = core.assemble_slides(songs)

    # Assert slides are correct
    assert slides == expected

def test_assemble_slides_custom_lines_per_slide(mocker):
    # Mock parse_song_lyrics
    mocker.patch('songs2slides.core.parse_song_lyrics')
    core.parse_song_lyrics.side_effect = [['aaa'], ['b1', 'b2']]

    # Declare song data and expected slides
    songs = [
        core.SongData('T1', 'A1', 'l1'),
        core.SongData('T2', 'A3', 'l2'),
        ]
    expected = ['T1', 'aaa', '', 'T2', 'b1', 'b2']

    # Get slides
    slides = core.assemble_slides(songs, lines_per_slide = 3)

    # Assert slides are correct
    assert slides == expected

    # Assert parse_song_lyrics called correctly
    core.parse_song_lyrics.assert_has_calls([
        mocker.call('L1', 3), mocker.call('L2', 3)
    ])

def test_assemble_slides_no_title_slides():
    # Declare song data and expected slides
    songs = [
        core.SongData('t1', 'a1', 'l1\nl2\nl3\nl4\nl5'),
        core.SongData('T2', 'A3', 'L6\nL7\n\nL8\n\n\nL9'),
    ]
    expected = [
        'L1\nL2\nL3\nL4', 'L5', '',
        'L6\nL7', 'L8', '', 'L9',
    ]

    # Get slides
    slides = core.assemble_slides(songs, title_slides = False)

    # Assert slides are correct
    assert slides == expected

def test_assemble_slides_no_blank_slides():
    # Declare song data and expected slides
    songs = [
        core.SongData('t1', 'a1', 'l1\nl2\nl3\nl4\nl5'),
        core.SongData('T2', 'A3', 'L6\nL7\n\nL8\n\n\nL9'),
    ]
    expected = [
        'T1', 'L1\nL2\nL3\nL4', 'L5',
        'T2', 'L6\nL7', 'L8', '', 'L9',
    ]

    # Get slides
    slides = core.assemble_slides(songs, blank_slides = False)

    # Assert slides are correct
    assert slides == expected

def test_assemble_slides_no_extra_slides():
    # Declare song data and expected slides
    songs = [
        core.SongData('t1', 'a1', 'l1\nl2\nl3\nl4\nl5'),
        core.SongData('T2', 'A3', 'L6\nL7\n\nL8\n\n\nL9'),
    ]
    expected = [
        'L1\nL2\nL3\nL4', 'L5',
        'L6\nL7', 'L8', '', 'L9',
    ]

    # Get slides
    slides = core.assemble_slides(songs, title_slides = False, blank_slides = False)

    # Assert slides are correct
    assert slides == expected

def test_assemble_slides_no_songs():
    # Declare expected slides
    expected = []

    # Get slides
    slides = core.assemble_slides([])

    # Assert slides are correct
    assert slides == expected

def test_create_pptx(mocker):
    # Mock Presentation.save
    mocker.patch('songs2slides.core.pptx.presentation.Presentation.save')

    # Create PowerPoint
    core.create_pptx(['A', 'B\nC', 'D'], 'test.pptx')

    # Assert PowerPoint was saved
    core.pptx.presentation.Presentation.save.assert_called_with('test.pptx')
