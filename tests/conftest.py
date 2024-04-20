import os
import pytest
from xprocess import ProcessStarter

@pytest.fixture(scope='session')
def api(xprocess):
    port = '5003'

    class Starter(ProcessStarter):
        pattern = '.*Running.*'
        timeout = 10
        args = ['python', '-m', 'flask', '--app', '../../../../mock_api.py',
                'run', '--port', port]

    # Start API
    xprocess.ensure('api', Starter)

    yield f'http://localhost:{port}'

    # Stop API
    xprocess.getinfo('api').terminate()

@pytest.fixture(scope='session')
def server(xprocess, api):
    port = '5002'

    class Starter(ProcessStarter):
        pattern = '.*Running.*'
        timeout = 10
        args = ['python', '-m', 'flask', '--app', '../../../../songs2slides',
                'run', '--port', port]
        env = os.environ | { 'API_URL': api + '/{title}/{artist}/' }

    # Start server
    xprocess.ensure('server', Starter)

    yield f'http://localhost:{port}'

    # Stop server
    xprocess.getinfo('server').terminate()

@pytest.fixture(scope='session')
def base_url(server):
    return server
