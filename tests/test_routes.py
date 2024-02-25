import unittest
from unittest.mock import patch, call

from songs2slides import create_app, core

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_slides_basic(self):
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
            })

            # Assert mocks called correctly
            mocked_assemble.assert_called_with([
                    core.SongData('T1', 'A1', 'L1'),
                    core.SongData('T2', 'A2', 'L2'),
                ],
                lines_per_slide = None
            )
            file = mocked_create.call_args.args[1]
            mocked_send.assert_called_with(file, as_attachment=True,
                                           download_name='slides.pptx')

    def test_slides_mising_artist(self):
        with patch('songs2slides.core.assemble_slides') as mocked_assemble:

            # Send request
            res = self.client.post('/slides/', data={
                'title-1': 'T1',
                'artist-1': 'A1',
                'lyrics-1': 'L1',
                'title-2': 'T2',
                'lyrics-2': 'L2',
            })

            # Assert response has 400 status code
            self.assertEqual(res.status_code, 400)

            # Assert assemble_slides not called
            mocked_assemble.assert_not_called()
