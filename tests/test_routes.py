import unittest
from unittest.mock import patch, call

from songs2slides import create_app, core

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_lyrics_basic(self):
        with patch('songs2slides.core.get_song_data') as mocked_get, \
            patch('songs2slides.core.parse_song_lyrics') as mocked_parse, \
            patch('songs2slides.routes.render_template') as mocked_render:

            # Mock get_song_data and parse_song_lyrics
            songs = [
                core.SongData('T1', 'A1', 'L1'),
                core.SongData('T2', 'A2', 'L2'),
            ]
            mocked_get.side_effect = songs
            mocked_parse.side_effect = ['L1', 'L2']

            # Send request
            self.client.post('/create/step-2/', data={
                'title-1': 'T1',
                'artist-1': 'A1',
                'title-2': 'T2',
                'artist-2': 'A2',
            })

            # Assert mocks called correctly
            mocked_get.assert_has_calls([call('T1', 'A1'), call('T2', 'A2')])
            mocked_parse.assert_has_calls([call('L1', 4), call('L2', 4)])
            mocked_render.assert_called_with('create-step-2.html', songs=songs, missing=0)

    def test_get_lyrics_one_error(self):
        with patch('songs2slides.core.get_song_data') as mocked_get, \
            patch('songs2slides.core.parse_song_lyrics') as mocked_parse, \
            patch('songs2slides.routes.render_template') as mocked_render:

            # Mock get_song_data and parse_song_lyrics
            songs = [
                core.SongData('T1', 'A1', None),
                core.SongData('T2', 'A2', 'L2'),
            ]
            mocked_get.side_effect = [Exception(), songs[1]]
            mocked_parse.side_effect = ['L1', 'L2']

            # Send request
            self.client.post('/create/step-2/', data={
                'title-1': 'T1',
                'artist-1': 'A1',
                'title-2': 'T2',
                'artist-2': 'A2',
            })

            # Assert mocks called correctly
            mocked_get.assert_has_calls([call('T1', 'A1'), call('T2', 'A2')])
            mocked_parse.assert_has_calls([call('L2', 4)])
            mocked_render.assert_called_with('create-step-2.html', songs=songs, missing=1)

    def test_get_lyrics_missing_artist(self):
        with patch('songs2slides.core.get_song_data') as mocked_get:

            # Send request
            res = self.client.post('/create/step-2/', data={
                'title-1': 'T1',
                'title-2': 'T2',
                'artist-2': 'A2',
            })

            # Assert mocks not called
            mocked_get.assert_not_called()

            # Assert response has 400 status code
            self.assertEqual(res.status_code, 400)

    def test_create_slides_basic(self):
        with patch('songs2slides.core.assemble_slides') as mocked_assemble, \
            patch('songs2slides.core.create_pptx') as mocked_create, \
            patch('songs2slides.routes.send_file') as mocked_send:

            # Send request
            self.client.post('/slides/', data={
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
            mocked_assemble.assert_called_with([
                    core.SongData('T1', 'A1', 'L1'),
                    core.SongData('T2', 'A2', 'L2'),
                ],
                lines_per_slide = None,
                title_slides = True,
                blank_slides = True,
            )
            file = mocked_create.call_args.args[1]
            mocked_send.assert_called_with(file, as_attachment=True,
                                           download_name='slides.pptx')

    def test_create_slides_mising_artist(self):
        with patch('songs2slides.core.assemble_slides') as mocked_assemble:

            # Send request
            res = self.client.post('/slides/', data={
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
            self.assertEqual(res.status_code, 400)

            # Assert assemble_slides not called
            mocked_assemble.assert_not_called()

    def test_create_slides_html_slides(self):
        with patch('songs2slides.core.assemble_slides') as mocked_assemble, \
            patch('songs2slides.core.create_pptx') as mocked_create, \
            patch('songs2slides.routes.render_template') as mocked_render:

            # Mock assemble_slides
            slides = ['T1', 'L1\nL2', 'L3', 'T2', 'L4']
            mocked_assemble.return_value = slides

            # Send request
            self.client.post('/slides/', data={
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
            mocked_assemble.assert_called_with([
                    core.SongData('T1', 'A1', 'L1'),
                    core.SongData('T2', 'A2', 'L2'),
                ],
                lines_per_slide = None,
                title_slides = True,
                blank_slides = True,
            )
            mocked_create.assert_not_called()
            mocked_render.assert_called_with('slides.html', slides=slides)

    def test_create_slides_no_title_slides(self):
        with patch('songs2slides.core.assemble_slides') as mocked_assemble, \
            patch('songs2slides.core.create_pptx') as mocked_create, \
            patch('songs2slides.routes.render_template') as mocked_render:

            # Mock assemble_slides
            slides = ['T1', 'L1\nL2', 'L3', 'T2', 'L4']
            mocked_assemble.return_value = slides

            # Send request
            self.client.post('/slides/', data={
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
            mocked_assemble.assert_called_with([
                    core.SongData('T1', 'A1', 'L1'),
                    core.SongData('T2', 'A2', 'L2'),
                ],
                lines_per_slide = None,
                title_slides = False,
                blank_slides = True,
            )
            mocked_create.assert_not_called()
            mocked_render.assert_called_with('slides.html', slides=slides)

    def test_create_slides_no_blank_slides(self):
        with patch('songs2slides.core.assemble_slides') as mocked_assemble, \
            patch('songs2slides.core.create_pptx') as mocked_create, \
            patch('songs2slides.routes.render_template') as mocked_render:

            # Mock assemble_slides
            slides = ['T1', 'L1\nL2', 'L3', 'T2', 'L4']
            mocked_assemble.return_value = slides

            # Send request
            self.client.post('/slides/', data={
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
            mocked_assemble.assert_called_with([
                    core.SongData('T1', 'A1', 'L1'),
                    core.SongData('T2', 'A2', 'L2'),
                ],
                lines_per_slide = None,
                title_slides = True,
                blank_slides = False,
            )
            mocked_create.assert_not_called()
            mocked_render.assert_called_with('slides.html', slides=slides)
