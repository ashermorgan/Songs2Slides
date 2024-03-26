addEventListener('submit', () => {
    if (document.getElementById('step-1').hidden == false) {
        // Show step 1 spinner
        document.getElementById('post-step-1').hidden = false
    } else if (document.querySelector('input[value=pptx]').checked) {
        // Show step 2 downloading message
        document.getElementById('step-2').hidden = true
        document.getElementById('post-step-2').hidden = false
    }
});

/* step 1 functions */
function add_song() {
    let row = document.getElementById('row-template').content.children[0].cloneNode(true)
    document.getElementById('songs').appendChild(row)
    renumber_songs()
}

function remove_song(n) {
    document.getElementsByTagName('tr')[n].remove()
    renumber_songs()
    if (document.getElementsByTagName('tr').length === 1) add_song()
}

function renumber_songs() {
    const songs = document.getElementsByTagName('tr')
    for (let i = 1; i < songs.length; i++) {
        songs[i].children[0].textContent = `${i}.`
        songs[i].children[1].children[0].name = `title-${i}`
        songs[i].children[2].children[0].name = `artist-${i}`
        songs[i].children[3].children[0].onclick = () => remove_song(i)
    }
}

/* step 2 functions */
function back() {
    document.getElementById('step-1').hidden = false
    document.getElementById('post-step-1').hidden = true
    document.getElementById('step-2').hidden = true
    document.getElementById('post-step-2').hidden = true
}
