# Requires songs2slides to be using mock_api.py and running on localhost:5000

from playwright.sync_api import Page, expect

def test_basic(page: Page):
    # Start on homepage
    page.goto("http://localhost:5000")

    # Click "Create a Slideshow"
    page.get_by_role("link", name="Create a Slideshow").click()
    expect(page).to_have_url("http://localhost:5000/create/step-1/")

    # Fill in song information
    page.get_by_placeholder("Song title").last.fill("Song 1")
    page.get_by_placeholder("Song artist").last.fill("aRtIsT A")
    page.get_by_role("button", name="Add Song").click()
    page.get_by_placeholder("Song title").last.fill("Song 5")
    page.get_by_placeholder("Song artist").last.fill("")

    # Click Next
    page.get_by_role("button", name="Next").click()
    expect(page).to_have_url("http://localhost:5000/create/step-2/")

    # Assert missing song message is correct
    expect(page.get_by_text("Lyrics must be entered manually for 1 song.")).to_be_visible()

    # Assert songs are loaded
    expect(page.get_by_text("Song 1 (Artist A)")).to_be_visible()
    expect(page.get_by_text("Song 1 (Artist A) lyrics not found")).to_be_hidden()
    expect(page.get_by_text("Song 5 lyrics not found")).to_be_visible()

    # Assert song lyrics are loaded (Song 1 lyrics still collapsed)
    expect(page.get_by_role("textbox")).to_have_count(1)
    expect(page.get_by_role("textbox").first).to_have_value('')

    # Uncollapse Song 1
    page.get_by_text("Song 1 (Artist A)").click()

    # Assert song lyrics are loaded (Song 1 lyrics uncollapsed)
    expect(page.get_by_role("textbox")).to_have_count(2)
    expect(page.get_by_role("textbox").first).to_have_value('Lyrics to song 1\nby artist A')
    expect(page.get_by_role("textbox").last).to_have_value('')

    # Fill in missing lyrics
    page.get_by_role("textbox").last.fill('custom song 5 lyrics')

    # Click Next
    page.get_by_role("button", name="Next").click()
    expect(page).to_have_url("http://localhost:5000/create/step-3/")

    # Fill in slideshow settings
    page.get_by_role("checkbox", name="Include a title slide before each song").uncheck()
    page.get_by_role("radio", name="Web View").check()

    # Click create
    page.get_by_role("button", name="Create").click()
    expect(page).to_have_url("http://localhost:5000/slides/")

    # Assert slide content is correct
    expect(page.locator("css=section.present")).to_have_text('LYRICS TO SONG 1\nBY ARTIST A')
    page.keyboard.press("ArrowRight")
    expect(page.locator("css=section.present")).to_have_text('')
    page.keyboard.press("ArrowRight")
    expect(page.locator("css=section.present")).to_have_text('CUSTOM SONG 5 LYRICS')
    page.keyboard.press("ArrowRight")
    expect(page.locator("css=section.present")).to_have_text('CUSTOM SONG 5 LYRICS')
