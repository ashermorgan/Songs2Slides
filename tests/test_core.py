import unittest
from unittest.mock import patch, call

from songs2slides import core

class TestCore(unittest.TestCase):
    def test_filter_lyrics_inline(self):
        # Declare raw lyrics and expected cleaned lyrics
        lyrics = 'A[remove]B\nC(remove)D'
        expected = 'AB\nCD'

        # Clean lyrics
        result = core.filter_lyrics(lyrics)

        # Assert slides are correct
        self.assertEqual(result, expected)

    def test_filter_lyrics_whole_lines(self):
        # Declare raw lyrics and expected cleaned lyrics
        lyrics = 'A\n[remove]\nB\n(remove)\nC'
        expected = 'A\nB\nC'

        # Clean lyrics
        result = core.filter_lyrics(lyrics)

        # Assert slides are correct
        self.assertEqual(result, expected)

    def test_filter_lyrics_multiple_lines(self):
        # Declare raw lyrics and expected cleaned lyrics
        lyrics = 'A\n[re\nmove]\nB\n(re\nmove)\nC'
        expected = 'A\nB\nC'

        # Clean lyrics
        result = core.filter_lyrics(lyrics)

        # Assert slides are correct
        self.assertEqual(result, expected)

    def test_filter_lyrics_blank_lines(self):
        # Declare raw lyrics and expected cleaned lyrics
        lyrics = 'A\n[remove]\n\n(remove)\nB'
        expected = 'A\n\nB'

        # Clean lyrics
        result = core.filter_lyrics(lyrics)

        # Assert slides are correct
        self.assertEqual(result, expected)

    def test_filter_lyrics_all(self):
        # Declare raw lyrics and expected cleaned lyrics
        lyrics = 'A[remove]B\n[remove]\n\nC(remove)D\n(re\nmove)'
        expected = 'AB\n\nCD'

        # Clean lyrics
        result = core.filter_lyrics(lyrics)

        # Assert slides are correct
        self.assertEqual(result, expected)

    def test_filter_lyrics_empty_string(self):
        # Clean lyrics
        result = core.filter_lyrics('')

        # Assert slides are correct
        self.assertEqual(result, '')

    def test_get_song_data_success(self):
        with patch('songs2slides.core.os.getenv') as mocked_env, \
            patch('songs2slides.core.requests.get') as mocked_get, \
            patch('songs2slides.core.filter_lyrics') as mocked_clean:

            # Mock os.getenv, requests.get, and core.filter_lyrics
            mocked_env.side_effect = [
                'api://lyrics/{artist}/{title}',
                'Bearer secrettoken'
            ]
            mocked_get.return_value.json.return_value = {
                'lyrics': 'raw',
                'title': 'Foo',
                'artist': 'Bar',
            }
            mocked_get.return_value.status_code = 200
            mocked_clean.return_value = 'clean'

            # Get song data
            song_data = core.get_song_data('foo', 'bar')

            # Assert mocked methods were used correctly
            mocked_env.assert_has_calls([
                call('API_URL'),
                call('API_AUTH', None)
            ])
            mocked_get.assert_called_with('api://lyrics/bar/foo', headers={
                'Authorization': 'Bearer secrettoken'
            })
            mocked_clean.assert_called_with('raw')

            # Assert song data is correct
            self.assertEqual(song_data.title, 'Foo')
            self.assertEqual(song_data.artist, 'Bar')
            self.assertEqual(song_data.lyrics, 'clean')

    def test_get_song_data_no_auth_header(self):
        with patch('songs2slides.core.os.getenv') as mocked_env, \
            patch('songs2slides.core.requests.get') as mocked_get, \
            patch('songs2slides.core.filter_lyrics') as mocked_clean:

            # Mock os.getenv, requests.get, and core.filter_lyrics
            mocked_env.side_effect = [
                'api://lyrics/{artist}/{title}',
                None,
            ]
            mocked_get.return_value.json.return_value = {
                'lyrics': 'raw',
                'title': 'Foo',
                'artist': 'Bar',
            }
            mocked_get.return_value.status_code = 200
            mocked_clean.return_value = 'clean'

            # Get song data
            song_data = core.get_song_data('foo', 'bar')

            # Assert mocked methods were used correctly
            mocked_env.assert_has_calls([
                call('API_URL'),
                call('API_AUTH', None)
            ])
            mocked_get.assert_called_with('api://lyrics/bar/foo', headers={})
            mocked_clean.assert_called_with('raw')

            # Assert song data is correct
            self.assertEqual(song_data.title, 'Foo')
            self.assertEqual(song_data.artist, 'Bar')
            self.assertEqual(song_data.lyrics, 'clean')

    def test_get_song_data_no_url(self):
        with patch('songs2slides.core.os.getenv') as mocked_env, \
            patch('songs2slides.core.requests.get') as mocked_get:

            # Mock os.getenv and requests.get
            mocked_env.return_value = None
            mocked_get.return_value.text = b'{}'
            mocked_get.return_value.status_code = 200

            # Try to get song data
            with self.assertRaises(Exception):
                song_data = core.get_song_data('foo', 'bar')

            # Assert request was not called
            mocked_get.assert_not_called()

    def test_get_song_data_not_found(self):
        with patch('songs2slides.core.os.getenv') as mocked_env, \
            patch('songs2slides.core.requests.get') as mocked_get:

            # Mock os.getenv and requests.get
            mocked_env.side_effect = [
                'api://lyrics/{artist}/{title}',
                'Bearer secrettoken'
            ]
            mocked_get.return_value.text = b'{}'
            mocked_get.return_value.status_code = 200

            # Try to get song data
            with self.assertRaises(Exception):
                song_data = core.get_song_data('foo', 'bar')

            # Assert request was called
            mocked_get.assert_called_with('api://lyrics/bar/foo', headers={
                'Authorization': 'Bearer secrettoken'
            })

    def test_parse_song_lyrics_basic(self):
        # Declare song data and expected slides
        lyrics = 'A\nB\nC\nD\nE\nF\n\nG\nH'
        expected = ['A\nB\nC\nD', 'E\nF', 'G\nH']

        # Get slide content
        result = core.parse_song_lyrics(lyrics, 4)

        # Assert slides are correct
        self.assertEqual(result, expected)

    def test_parse_song_lyrics_3_lines_per_slide(self):
        # Declare song data and expected slides
        lyrics = 'A\nB\nC\nD\nE\nF\n\nG\nH'
        expected = ['A\nB\nC', 'D\nE\nF', 'G\nH']

        # Get slide content
        result = core.parse_song_lyrics(lyrics, 3)

        # Assert slides are correct
        self.assertEqual(result, expected)

    def test_parse_song_lyrics_empty_string(self):
        # Declare song data and expected slides
        lyrics = ''
        expected = []

        # Get slide content
        result = core.parse_song_lyrics(lyrics, 4)

        # Assert slides are correct
        self.assertEqual(result, expected)

    def test_parse_song_lyrics_one_line(self):
        # Declare song data and expected slides
        lyrics = 'A'
        expected = ['A']

        # Get slide content
        result = core.parse_song_lyrics(lyrics, 4)

        # Assert slides are correct
        self.assertEqual(result, expected)

    def test_parse_song_lyrics_one_slide(self):
        # Declare song data and expected slides
        lyrics = 'A\nB\nC\nD'
        expected = ['A\nB\nC\nD']

        # Get slide content
        result = core.parse_song_lyrics(lyrics, 4)

        # Assert slides are correct
        self.assertEqual(result, expected)

    def test_parse_song_lyrics_tripple_newlines(self):
        # Declare song data and expected slides
        lyrics = 'A\nB\n\n\nC\nD'
        expected = ['A\nB', '', 'C\nD']

        # Get slide content
        result = core.parse_song_lyrics(lyrics, 4)

        # Assert slides are correct
        self.assertEqual(result, expected)

    def test_parse_song_lyrics_extra_whitespace(self):
        # Declare song data and expected slides
        lyrics = ' A\n B \nC D\nE '
        expected = ['A\nB\nC D\nE']

        # Get slide content
        result = core.parse_song_lyrics(lyrics, 4)

        # Assert slides are correct
        self.assertEqual(result, expected)

    def test_parse_song_lyrics_extra_newlines(self):
        # Declare song data and expected slides
        lyrics = '\n\n\nA\n\n\n\n\nB\n\n\n'
        expected = ['A', '', 'B']

        # Get slide content
        result = core.parse_song_lyrics(lyrics, 4)

        # Assert slides are correct
        self.assertEqual(result, expected)

    def test_assemble_slides_calls_parse_song_lyrics(self):
        with patch('songs2slides.core.parse_song_lyrics') as mocked_parse:

            # Mock parse_song_lyrics
            mocked_parse.side_effect = [['aaa'], ['b1', 'b2']]

            # Declare song data and expected slides
            songs = [
                core.SongData('T1', 'A1', 'l1'),
                core.SongData('T2', 'A3', 'l2'),
                ]
            expected = ['T1', 'aaa', '', 'T2', 'b1', 'b2']

            # Get slides
            slides = core.assemble_slides(songs)

            # Assert slides are correct
            self.assertEqual(slides, expected)

            # Assert parse_song_lyrics called
            mocked_parse.assert_has_calls([call('L1', 4), call('L2', 4)])

    def test_assemble_slides_default(self):
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
        self.assertEqual(slides, expected)

    def test_assemble_slides_custom_lines_per_slide(self):
        with patch('songs2slides.core.parse_song_lyrics') as mocked_parse:

            # Mock parse_song_lyrics
            mocked_parse.side_effect = [['aaa'], ['b1', 'b2']]

            # Declare song data and expected slides
            songs = [
                core.SongData('T1', 'A1', 'l1'),
                core.SongData('T2', 'A3', 'l2'),
                ]
            expected = ['T1', 'aaa', '', 'T2', 'b1', 'b2']

            # Get slides
            slides = core.assemble_slides(songs, lines_per_slide = 3)

            # Assert slides are correct
            self.assertEqual(slides, expected)

            # Assert parse_song_lyrics called correctly
            mocked_parse.assert_has_calls([call('L1', 3), call('L2', 3)])

    def test_assemble_slides_no_title_slides(self):
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
        self.assertEqual(slides, expected)

    def test_assemble_slides_no_blank_slides(self):
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
        self.assertEqual(slides, expected)

    def test_assemble_slides_no_extra_slides(self):
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
        self.assertEqual(slides, expected)

    def test_assemble_slides_no_songs(self):
        # Declare expected slides
        expected = []

        # Get slides
        slides = core.assemble_slides([])

        # Assert slides are correct
        self.assertEqual(slides, expected)

    def test_create_pptx(self):
        with patch('songs2slides.core.pptx.presentation.Presentation.save') as mocked_save:
            # Create PowerPoint
            core.create_pptx(['A', 'B\nC', 'D'], 'test.pptx')

            # Assert PowerPoint was saved
            mocked_save.assert_called_with('test.pptx')
