import pytest
from playwright.sync_api import Page, expect
from xprocess import ProcessStarter

@pytest.fixture(autouse=True, scope='session')
def api(xprocess):
    port = '5003'

    class Starter(ProcessStarter):
        pattern = '.*Running.*'
        timeout = 10
        args = ['python3', '-m', 'flask', '--app', '../../../../mock_api.py', 'run']
        env = {
            'FLASK_RUN_PORT': port,
        }

    # Start API
    xprocess.ensure('api', Starter)

    yield f'http://localhost:{port}'

    # Stop API
    xprocess.getinfo('api').terminate()

@pytest.fixture(autouse=True, scope='session')
def server(xprocess, api):
    port = '5002'

    class Starter(ProcessStarter):
        pattern = '.*Running.*'
        timeout = 10
        args = ['python3', '-m', 'flask', '--app', '../../../../songs2slides', 'run']
        env = {
            'API_URL': api + '/{title}/{artist}/',
            'FLASK_RUN_PORT': port,
        }

    # Start server
    xprocess.ensure('server', Starter)

    yield f'http://localhost:{port}'

    # Stop server
    xprocess.getinfo('server').terminate()

@pytest.fixture(autouse=True, scope='session')
def base_url(server):
    return server

def test_basic(page: Page):
    # Start on homepage
    page.goto('/')

    # Click 'Create a Slideshow'
    page.get_by_role('link', name='Create a Slideshow').click()
    expect(page).to_have_url('http://localhost:5002/create/step-1/')

    # Fill in song information
    page.get_by_placeholder('Song title').last.fill('Song 1')
    page.get_by_placeholder('Song artist').last.fill('aRtIsT A')
    page.get_by_role('button', name='Add Song').click()
    page.get_by_placeholder('Song title').last.fill('Song 5')
    page.get_by_placeholder('Song artist').last.fill('')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-2/')

    # Assert missing song message is correct
    expect(page.get_by_text('Lyrics must be entered manually for 1 song.')).to_be_visible()

    # Assert songs are loaded
    expect(page.get_by_text('Song 1 (Artist A)')).to_be_visible()
    expect(page.get_by_text('Song 1 (Artist A) lyrics not found')).to_be_hidden()
    expect(page.get_by_text('Song 5 lyrics not found')).to_be_visible()

    # Assert song lyrics are loaded (Song 1 lyrics still collapsed)
    expect(page.get_by_role('textbox')).to_have_count(1)
    expect(page.get_by_role('textbox').first).to_have_value('')

    # Uncollapse Song 1
    page.get_by_text('Song 1 (Artist A)').click()

    # Assert song lyrics are loaded (Song 1 lyrics uncollapsed)
    expect(page.get_by_role('textbox')).to_have_count(2)
    expect(page.get_by_role('textbox').first).to_have_value('Lyrics to song 1\nby artist A')
    expect(page.get_by_role('textbox').last).to_have_value('')

    # Fill in missing lyrics
    page.get_by_role('textbox').last.fill('custom song 5 lyrics')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-3/')

    # Fill in slideshow settings
    page.get_by_role('checkbox', name='Include a title slide before each song').uncheck()

    # Click create
    page.get_by_role('button', name='Create').click()
    expect(page).to_have_url('http://localhost:5002/slides/')

    # Assert slide content is correct
    expect(page.locator('css=section.present')).to_have_text('LYRICS TO SONG 1\nBY ARTIST A')
    page.keyboard.press('ArrowRight')
    expect(page.locator('css=section.present')).to_have_text('')
    page.keyboard.press('ArrowRight')
    expect(page.locator('css=section.present')).to_have_text('CUSTOM SONG 5 LYRICS')
    page.keyboard.press('ArrowRight')
    expect(page.locator('css=section.present')).to_have_text('CUSTOM SONG 5 LYRICS')

def test_pptx(page: Page):
    # Start on homepage
    page.goto('/')

    # Click 'Create a Slideshow'
    page.get_by_role('link', name='Create a Slideshow').click()
    expect(page).to_have_url('http://localhost:5002/create/step-1/')

    # Fill in song information
    page.get_by_placeholder('Song title').last.fill('Song 1')
    page.get_by_placeholder('Song artist').last.fill('aRtIsT A')
    page.get_by_role('button', name='Add Song').click()
    page.get_by_placeholder('Song title').last.fill('Song 5')
    page.get_by_placeholder('Song artist').last.fill('')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-2/')

    # Fill in missing lyrics
    page.get_by_role('textbox').last.fill('custom song 5 lyrics')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-3/')

    # Fill in slideshow settings
    page.get_by_role('checkbox', name='Include a title slide before each song').uncheck()
    page.get_by_role('radio', name='PowerPoint Download').check()

    # Click create
    with page.expect_download() as download:
        page.get_by_role('button', name='Create').click()

    # Assert PowerPoint was downloaded
    assert download.value.suggested_filename == 'slides.pptx'

    # Assert redirected to post download page
    expect(page).to_have_url('http://localhost:5002/post-download/')

def test_localStorage(page: Page):
    # Start on homepage
    page.goto('/')

    # Click 'Create a Slideshow'
    page.get_by_role('link', name='Create a Slideshow').click()
    expect(page).to_have_url('http://localhost:5002/create/step-1/')

    # Fill in song information
    page.get_by_placeholder('Song title').last.fill('Song 1')
    page.get_by_placeholder('Song artist').last.fill('aRtIsT A')
    page.get_by_role('button', name='Add Song').click()
    page.get_by_placeholder('Song title').last.fill('Song 5')
    page.get_by_placeholder('Song artist').last.fill('')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-2/')

    # Fill in missing lyrics
    page.get_by_role('textbox').last.fill('custom song 5 lyrics')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-3/')

    # Assert slideshow settings have default values
    expect(page.get_by_role('checkbox', name='Include a title slide before each song')).to_be_checked()
    expect(page.get_by_role('checkbox', name='Include a blank slide between each song')).to_be_checked()
    expect(page.get_by_role('radio', name='Web View')).to_be_checked()

    # Fill in slideshow settings
    page.get_by_role('checkbox', name='Include a title slide before each song').uncheck()
    page.get_by_role('radio', name='PowerPoint Download').check()

    # Click create
    page.get_by_role('button', name='Create').click()
    expect(page).to_have_url('http://localhost:5002/post-download/')

    # Return to homepage
    page.goto('/')

    # Click 'Create a Slideshow'
    page.get_by_role('link', name='Create a Slideshow').click()
    expect(page).to_have_url('http://localhost:5002/create/step-1/')

    # Fill in song information
    page.get_by_placeholder('Song title').last.fill('Song 1')
    page.get_by_placeholder('Song artist').last.fill('aRtIsT A')
    page.get_by_role('button', name='Add Song').click()
    page.get_by_placeholder('Song title').last.fill('Song 5')
    page.get_by_placeholder('Song artist').last.fill('')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-2/')

    # Fill in missing lyrics
    page.get_by_role('textbox').last.fill('custom song 5 lyrics')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-3/')

    # Assert slideshow settings have custom values
    expect(page.get_by_role('checkbox', name='Include a title slide before each song')).to_be_checked(checked = False)
    expect(page.get_by_role('checkbox', name='Include a blank slide between each song')).to_be_checked()

def test_back(page: Page):
    # Start on homepage
    page.goto('/')

    # Click 'Create a Slideshow'
    page.get_by_role('link', name='Create a Slideshow').click()
    expect(page).to_have_url('http://localhost:5002/create/step-1/')

    # Fill in bad song information
    page.get_by_placeholder('Song title').last.fill('Song 11')
    page.get_by_placeholder('Song artist').last.fill('aRtIsT Aa')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-2/')

    # Assert songs are loaded
    expect(page.get_by_text('Song 11 (Artist Aa) lyrics not found')).to_be_visible()
    expect(page.get_by_text('Song 5 lyrics not found')).to_be_hidden()

    # Assert song lyrics are loaded
    expect(page.get_by_role('textbox')).to_have_count(1)
    expect(page.get_by_role('textbox').first).to_have_value('')

    # Click Back
    page.get_by_role('button', name='Back').click()
    expect(page).to_have_url('http://localhost:5002/create/step-1/')

    # Assert bad song information is still present
    expect(page.get_by_placeholder('Song title')).to_have_count(1)
    expect(page.get_by_placeholder('Song title').first).to_have_value('Song 11')
    expect(page.get_by_placeholder('Song artist')).to_have_count(1)
    expect(page.get_by_placeholder('Song artist').last).to_have_value('aRtIsT Aa')

    # Fill in correct song information
    page.get_by_placeholder('Song title').last.fill('Song 1')
    page.get_by_placeholder('Song artist').last.fill('aRtIsT A')
    page.get_by_role('button', name='Add Song').click()
    page.get_by_placeholder('Song title').last.fill('Song 5')
    page.get_by_placeholder('Song artist').last.fill('')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-2/')

    # Assert songs are loaded
    expect(page.get_by_text('Song 1 (Artist A)')).to_be_visible()
    expect(page.get_by_text('Song 1 (Artist A) lyrics not found')).to_be_hidden()
    expect(page.get_by_text('Song 5 lyrics not found')).to_be_visible()

    # Uncollapse Song 1
    page.get_by_text('Song 1 (Artist A)').click()

    # Assert songs lyrics are loaded
    expect(page.get_by_role('textbox')).to_have_count(2)
    expect(page.get_by_role('textbox').first).to_have_value('Lyrics to song 1\nby artist A')
    expect(page.get_by_role('textbox').last).to_have_value('')

    # Fill in bad missing lyrics
    page.get_by_role('textbox').last.fill('custom song 5 lyrics (bad)')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-3/')

    # Click Back
    page.get_by_role('button', name='Back').click()
    expect(page).to_have_url('http://localhost:5002/create/step-2/')

    # Uncollapse Song 1
    page.get_by_text('Song 1 (Artist A)').click()

    # Assert bad song lyrics are still loaded
    expect(page.get_by_role('textbox')).to_have_count(2)
    expect(page.get_by_role('textbox').first).to_have_value('Lyrics to song 1\nby artist A')
    expect(page.get_by_role('textbox').last).to_have_value('custom song 5 lyrics (bad)')

    # Fill in correct missing lyrics
    page.get_by_role('textbox').last.fill('custom song 5 lyrics')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-3/')

    # Fill in bad slideshow settings
    page.get_by_role('checkbox', name='Include a blank slide between each song').uncheck()

    # Click create
    page.get_by_role('button', name='Create').click()
    expect(page).to_have_url('http://localhost:5002/slides/')

    # Assert slide content is correct
    expect(page.locator('css=section.present')).to_have_text('SONG 1')
    page.keyboard.press('ArrowRight')
    expect(page.locator('css=section.present')).to_have_text('LYRICS TO SONG 1\nBY ARTIST A')
    page.keyboard.press('ArrowRight')
    expect(page.locator('css=section.present')).to_have_text('SONG 5')
    page.keyboard.press('ArrowRight')
    expect(page.locator('css=section.present')).to_have_text('CUSTOM SONG 5 LYRICS')
    page.keyboard.press('ArrowRight')
    expect(page.locator('css=section.present')).to_have_text('CUSTOM SONG 5 LYRICS')

    # Click back
    page.go_back()
    expect(page).to_have_url('http://localhost:5002/create/step-3/')

    # Assert bad slideshow settings still loaded
    expect(page.get_by_role('checkbox', name='Include a blank slide between each song')).to_be_checked(checked = False)
    expect(page.get_by_role('checkbox', name='Include a title slide before each song')).to_be_checked()

    # Fill in correct slideshow settings
    page.get_by_role('checkbox', name='Include a title slide before each song').uncheck()

    # Click create
    page.get_by_role('button', name='Create').click()
    expect(page).to_have_url('http://localhost:5002/slides/')

    # Assert slide content is correct
    expect(page.locator('css=section.present')).to_have_text('LYRICS TO SONG 1\nBY ARTIST A')
    page.keyboard.press('ArrowRight')
    expect(page.locator('css=section.present')).to_have_text('CUSTOM SONG 5 LYRICS')
    page.keyboard.press('ArrowRight')
    expect(page.locator('css=section.present')).to_have_text('CUSTOM SONG 5 LYRICS')
