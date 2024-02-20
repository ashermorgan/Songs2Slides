import unittest
from unittest.mock import patch

from songs2slides import utils

class TestUtils(unittest.TestCase):
    def test_get_song_data_success(self):
        with patch('songs2slides.utils.os.getenv') as mocked_env, \
            patch('songs2slides.utils.requests.get') as mocked_get:

            # Mock os.getenv and requests.get
            mocked_env.return_value = 'api://lyrics/{artist}/{title}'
            mocked_get.return_value.text = b'{"lyrics":"A\nB\nC\nD","title":"Foo","artist":"Bar","image":null}'
            mocked_get.return_value.json.return_value = {
                'lyrics': 'A\nB\nC\nD',
                'title': 'Foo',
                'artist': 'Bar',
            }
            mocked_get.return_value.status_code = 200

            # Get song data
            song_data = utils.get_song_data('foo', 'bar')

            # Assert song data is correct
            mocked_get.assert_called_with('api://lyrics/bar/foo')
            self.assertEqual(song_data.title, 'Foo')
            self.assertEqual(song_data.artist, 'Bar')
            self.assertEqual(song_data.lyrics, 'A\nB\nC\nD')

    def test_get_song_data_no_url(self):
        with patch('songs2slides.utils.os.getenv') as mocked_env, \
            patch('songs2slides.utils.requests.get') as mocked_get:

            # Mock os.getenv and requests.get
            mocked_env.return_value = None
            mocked_get.return_value.text = b'{}'
            mocked_get.return_value.status_code = 200

            # Try to get song data
            with self.assertRaises(Exception):
                song_data = utils.get_song_data('foo', 'bar')

            # Assert request was not called
            mocked_get.assert_not_called()

    def test_get_song_data_not_found(self):
        with patch('songs2slides.utils.os.getenv') as mocked_env, \
            patch('songs2slides.utils.requests.get') as mocked_get:

            # Mock os.getenv and requests.get
            mocked_env.return_value = 'api://lyrics/{artist}/{title}'
            mocked_get.return_value.text = b'{}'
            mocked_get.return_value.status_code = 200

            # Try to get song data
            with self.assertRaises(Exception):
                song_data = utils.get_song_data('foo', 'bar')

            # Assert request was called
            mocked_get.assert_called_with('api://lyrics/bar/foo')

    def test_get_slide_contents_default(self):
        # Declare song data and expected slides
        lyrics = 'A\nB\nC\nD\nE\nF\n\nG\nH'
        expected = ['A\nB\nC\nD', 'E\nF', 'G\nH']

        # Get slide content
        result = utils.get_slide_contents(lyrics)

        self.assertEqual(result, expected)

    def test_get_slide_contents_3_lines_per_slide(self):
        # Declare song data and expected slides
        lyrics = 'A\nB\nC\nD\nE\nF\n\nG\nH'
        expected = ['A\nB\nC', 'D\nE\nF', 'G\nH']

        # Get slide content
        result = utils.get_slide_contents(lyrics, lines_per_slide = 3)

        self.assertEqual(result, expected)

    def test_get_slide_contents_empty_string(self):
        # Declare song data and expected slides
        lyrics = ''
        expected = []

        # Get slide content
        result = utils.get_slide_contents(lyrics, lines_per_slide = 3)

        self.assertEqual(result, expected)

    def test_get_slide_contents_one_line(self):
        # Declare song data and expected slides
        lyrics = 'A'
        expected = ['A']

        # Get slide content
        result = utils.get_slide_contents(lyrics)

        self.assertEqual(result, expected)

    def test_get_slide_contents_one_slide(self):
        # Declare song data and expected slides
        lyrics = 'A\nB\nC\nD'
        expected = ['A\nB\nC\nD']

        # Get slide content
        result = utils.get_slide_contents(lyrics)

        self.assertEqual(result, expected)

    def test_get_slide_contents_tripple_newlines(self):
        # Declare song data and expected slides
        lyrics = 'A\nB\n\n\nC\nD'
        expected = ['A\nB', '', 'C\nD']

        # Get slide content
        result = utils.get_slide_contents(lyrics)

        self.assertEqual(result, expected)

    def test_get_slide_contents_extra_whitespace(self):
        # Declare song data and expected slides
        lyrics = ' A\n B \nC D\nE '
        expected = ['A\nB\nC D\nE']

        # Get slide content
        result = utils.get_slide_contents(lyrics)

        self.assertEqual(result, expected)
