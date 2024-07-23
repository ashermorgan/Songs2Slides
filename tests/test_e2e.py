from playwright.sync_api import Page, expect

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
    expect(page.get_by_text('Lyrics must be entered manually for 1 song(s).')).to_be_visible()

    # Assert songs are loaded
    expect(page.get_by_text('Song 1 (Artist A)')).to_be_visible()
    expect(page.get_by_text('lyrics not found').first).to_be_hidden()
    expect(page.get_by_text('lyrics not found').last).to_be_visible()
    expect(page.get_by_text('Song 5 lyrics not found')).to_be_visible()

    # Assert song lyrics are loaded (Song 1 lyrics still collapsed)
    expect(page.get_by_role('textbox')).to_have_count(1)
    expect(page.get_by_role('textbox').first).to_have_value('')

    # Uncollapse Song 1
    page.get_by_text('Song 1 (Artist A)').click()

    # Assert song lyrics are loaded (Song 1 lyrics uncollapsed)
    expect(page.get_by_role('textbox')).to_have_count(2)
    expect(page.get_by_role('textbox').first).to_have_value('These are the lyrics\nto song 1\nby artist A')
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
    expect(page.locator('css=section.present')).to_have_text('THESE ARE THE LYRICS\nTO SONG 1\nBY ARTIST A')
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

    # Assert song information is not prefilled
    expect(page.get_by_placeholder('Song title')).to_have_count(1)
    expect(page.get_by_placeholder('Song title')).to_have_value('')
    expect(page.get_by_placeholder('Song artist')).to_have_count(1)
    expect(page.get_by_placeholder('Song artist')).to_have_value('')

    # Fill in song information
    page.get_by_placeholder('Song title').last.fill('Song 1')
    page.get_by_placeholder('Song artist').last.fill('aRtIsT A')
    page.get_by_role('button', name='Add Song').click()
    page.get_by_placeholder('Song title').last.fill('Song 5')
    page.get_by_placeholder('Song artist').last.fill('')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-2/')

    # Update lyrics
    page.get_by_text('Song 1 (Artist A)').click()
    page.get_by_role('textbox').first.fill('custom song 1 lyrics')
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

    # Assert song information is prefilled
    expect(page.get_by_placeholder('Song title')).to_have_count(2)
    expect(page.get_by_placeholder('Song title').first).to_have_value('Song 1')
    expect(page.get_by_placeholder('Song title').last).to_have_value('Song 5')
    expect(page.get_by_placeholder('Song artist')).to_have_count(2)
    expect(page.get_by_placeholder('Song artist').first).to_have_value('aRtIsT A')
    expect(page.get_by_placeholder('Song artist').last).to_have_value('')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-2/')

    # Assert song lyrics are collapsed and not missing
    expect(page.get_by_role('textbox')).to_have_count(0)
    expect(page.get_by_text('lyrics not found').first).to_be_hidden()
    expect(page.get_by_text('lyrics not found').last).to_be_hidden()

    # Uncollapse songs
    page.get_by_text('Song 1 (Artist A)').click()
    page.get_by_text('Song 5').click()

    # Assert song lyrics are prefilled
    expect(page.get_by_role('textbox').first).to_have_value('custom song 1 lyrics')
    expect(page.get_by_role('textbox').last).to_have_value('custom song 5 lyrics')

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
    page.get_by_role('button', name='Add Song').click()
    page.get_by_placeholder('Song title').last.fill('Song 55')
    page.get_by_placeholder('Song artist').last.fill('b')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-2/')

    # Assert songs are loaded
    expect(page.get_by_text('Song 11 (Artist Aa) lyrics not found')).to_be_visible()
    expect(page.get_by_text('Song 5 lyrics not found')).to_be_hidden()

    # Assert song lyrics are loaded
    expect(page.get_by_role('textbox')).to_have_count(2)
    expect(page.get_by_role('textbox').first).to_have_value('')
    expect(page.get_by_role('textbox').last).to_have_value('')

    # Click Back
    page.get_by_role('button', name='Back').click()
    expect(page).to_have_url('http://localhost:5002/create/step-1/')

    # Assert bad song information is still present
    expect(page.get_by_placeholder('Song title')).to_have_count(2)
    expect(page.get_by_placeholder('Song title').first).to_have_value('Song 11')
    expect(page.get_by_placeholder('Song title').last).to_have_value('Song 55')
    expect(page.get_by_placeholder('Song artist')).to_have_count(2)
    expect(page.get_by_placeholder('Song artist').first).to_have_value('aRtIsT Aa')
    expect(page.get_by_placeholder('Song artist').last).to_have_value('b')

    # Fill in correct song information
    page.get_by_placeholder('Song title').last.fill('Song 1')
    page.get_by_placeholder('Song artist').last.fill('aRtIsT A')
    page.get_by_role('button', name='Remove').first.click()
    page.get_by_role('button', name='Add Song').click()
    page.get_by_placeholder('Song title').last.fill('Song 5')
    page.get_by_placeholder('Song artist').last.fill('')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-2/')

    # Assert songs are loaded
    expect(page.get_by_text('Song 1 (Artist A)')).to_be_visible()
    expect(page.get_by_text('lyrics not found').first).to_be_hidden()
    expect(page.get_by_text('lyrics not found').last).to_be_visible()
    expect(page.get_by_text('Song 5 lyrics not found')).to_be_visible()

    # Uncollapse Song 1
    page.get_by_text('Song 1 (Artist A)').click()

    # Assert songs lyrics are loaded
    expect(page.get_by_role('textbox')).to_have_count(2)
    expect(page.get_by_role('textbox').first).to_have_value('These are the lyrics\nto song 1\nby artist A')
    expect(page.get_by_role('textbox').last).to_have_value('')

    # Update song lyrics
    page.get_by_role('textbox').first.fill('custom song 1 lyrics')
    page.get_by_role('textbox').last.fill('custom song 5 lyrics')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-3/')

    # Click Back
    page.get_by_role('button', name='Back').click()
    expect(page).to_have_url('http://localhost:5002/create/step-2/')

    # Uncollapse songs
    page.get_by_text('Song 1 (Artist A)').click()
    page.get_by_text('Song 5').click()

    # Assert updated song lyrics are still loaded
    expect(page.get_by_role('textbox')).to_have_count(2)
    expect(page.get_by_role('textbox').first).to_have_value('custom song 1 lyrics')
    expect(page.get_by_role('textbox').last).to_have_value('custom song 5 lyrics')

    # Revert lyrics
    page.get_by_title('Revert lyrics').first.click()
    expect(page.get_by_role('textbox').first).to_have_value('These are the lyrics\nto song 1\nby artist A')
    page.get_by_title('Revert lyrics').last.click()
    expect(page.get_by_role('textbox').last).to_have_value('')

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
    expect(page.locator('css=section.present')).to_have_text('THESE ARE THE LYRICS\nTO SONG 1\nBY ARTIST A')
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
    expect(page.locator('css=section.present')).to_have_text('THESE ARE THE LYRICS\nTO SONG 1\nBY ARTIST A')
    page.keyboard.press('ArrowRight')
    expect(page.locator('css=section.present')).to_have_text('CUSTOM SONG 5 LYRICS')
    page.keyboard.press('ArrowRight')
    expect(page.locator('css=section.present')).to_have_text('CUSTOM SONG 5 LYRICS')

def test_no_javascript(page: Page):
    page.java_script_enabled = False

    # Start on homepage
    page.goto('/')

    # Click 'Create a Slideshow'
    page.get_by_role('link', name='Create a Slideshow').click()
    expect(page).to_have_url('http://localhost:5002/create/step-1/')

    # Fill in song information
    page.get_by_placeholder('Song title').last.fill('Song 1')
    page.get_by_placeholder('Song artist').last.fill('aRtIsT A')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-2/')

    # Assert song is loaded
    expect(page.get_by_text('Song 1 (Artist A)')).to_be_visible()
    expect(page.get_by_text('lyrics not found')).to_be_hidden()

    # Assert song lyrics are loaded
    expect(page.get_by_role('textbox')).to_have_value('These are the lyrics\nto song 1\nby artist A')

    # Update lyrics
    page.get_by_role('textbox').last.fill('custom song 1 lyrics')

    # Click Next
    page.get_by_role('button', name='Next').click()
    expect(page).to_have_url('http://localhost:5002/create/step-3/')

    # Fill in slideshow settings
    page.get_by_role('checkbox', name='Include a title slide before each song').uncheck()

    # Click create
    page.get_by_role('button', name='Create').click()
    expect(page).to_have_url('http://localhost:5002/slides/')

    # Assert slide content is correct
    expect(page.locator('css=section.present')).to_have_text('CUSTOM SONG 1 LYRICS')
