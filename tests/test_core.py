import unittest
from unittest.mock import patch

from songs2slides import utils

class TestUtils(unittest.TestCase):
    def test_get_song_data_success(self):
        with patch('songs2slides.utils.os.getenv') as mocked_env, \
            patch('songs2slides.utils.requests.get') as mocked_get:

            # Mock os.getenv and requests.get
            mocked_env.return_value = 'api://lyrics/{artist}/{title}'
            mocked_get.return_value.text = b'{"lyrics":"Test1\nTest2\nTest3\nTest4","title":"Foo","artist":"Bar","image":null}'
            mocked_get.return_value.json.return_value = {
                'lyrics': 'Test1\nTest2\nTest3\nTest4',
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
            self.assertEqual(song_data.lyrics, 'Test1\nTest2\nTest3\nTest4')

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
