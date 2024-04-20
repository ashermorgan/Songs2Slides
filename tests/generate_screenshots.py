# Run with: pytest tests/generate_screenshots.py
# (not run by default due to lack of test_* filename prefix)

from playwright.sync_api import Page

def test_generate_screenshots(page: Page):
    # Set viewport size
    page.set_viewport_size({'width': 800, 'height': 380})

    # Start on homepage
    page.goto('/')

    # Click 'Create a Slideshow'
    page.get_by_role('link', name='Create a Slideshow').click()

    # Fill in song information
    page.get_by_placeholder('Song title').last.fill('Song 1')
    page.get_by_placeholder('Song artist').last.fill('Artist A')
    page.get_by_role('button', name='Add Song').click()
    page.get_by_placeholder('Song title').last.fill('Song 4')
    page.get_by_placeholder('Song artist').last.fill('Artist C')
    page.get_by_placeholder('Song artist').last.blur()

    # Take step 1 screenshot
    page.screenshot(path='screenshots/step-1.png', full_page=True)

    # Click Next
    page.get_by_role('button', name='Next').click()

    # Uncollapse Song 1
    page.get_by_text('Song 1 (Artist A)').click()

    # Shrink textareas (for a more compact screenshot)
    page.add_style_tag(content='textarea { height: 65px } .missing textarea { height: 40px }')

    # Take step 2 screenshot
    page.screenshot(path='screenshots/step-2.png', full_page=True)

    # Click Next
    page.get_by_role('button', name='Next').click()

    # Fill in slideshow settings
    page.get_by_role('checkbox', name='Include a title slide before each song').uncheck()

    # Take step 3 screenshot
    page.screenshot(path='screenshots/step-3.png', full_page=True)

    # Click create
    page.get_by_role('button', name='Create').click()

    # Hide header (for better screenshot)
    page.add_style_tag(content='header { display: none }')

    # Take slides screenshot
    page.screenshot(path='screenshots/slides.png', full_page=True)
