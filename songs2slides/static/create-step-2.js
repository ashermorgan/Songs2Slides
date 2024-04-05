addEventListener('submit', () => {
    // Save settings
    const form = document.getElementById('step-2')
    storage_set('title-slides', form['title-slides'].checked)
    storage_set('blank-slides', form['blank-slides'].checked)
    storage_set('output-type', form['output-type'].value)

    // Redirect to post download message
    if (form['output-type'].value === 'pptx') {
        setTimeout(() => {
            // On Chrome, redirecting after a form submission doesn't work
            // unless setTimeout is used
            // (REDIRECT_URL set in create-step-2.html template)
            window.location.href = REDIRECT_URL
        }, 100)
    }
})

addEventListener('pageshow', () => {
    // Load settings
    const form = document.getElementById('step-2')
    form['title-slides'].checked = storage_get('title-slides', true)
    form['blank-slides'].checked = storage_get('blank-slides', true)
    form['output-type'].value = storage_get('output-type', 'html')
})

// Global Songs2Slides localStorage prefix
const PREFIX = 's2s'

function storage_get(key, default_value) {
    try {
        value = JSON.parse(localStorage.getItem(`${PREFIX}.${key}`))
    } catch {
        return clonedDefault
    }
    return value === null ? default_value : value
}

function storage_set(key, value) {
    localStorage.setItem(`${PREFIX}.${key}`, JSON.stringify(value))
}
