// Declare global variables
setId = 0;  // Next valid song id number



// Adds a song
function AddSong() {
    // Create row
    var clone = document.getElementById("songTemplate").content.cloneNode(true);
    
    // Set row id
    clone.children[0].setAttribute("id", `song-${setId}`);
    
    // Add remove button onclick event
    clone.getElementById("remove").setAttribute("onclick", `var element = document.getElementById('song-${setId}'); element.parentNode.removeChild(element);`);
    
    // Add row  
    document.getElementById("songs").appendChild(clone);

    // Increment setId
    setId++;
}



// Gets the list of songs
function getSongs() {
    // Get song info
    var titles = [];
    for (title of document.getElementsByClassName("title")) {
        titles.push(title.value);
    }
    var artists = [];
    for (artist of document.getElementsByClassName("artist")) {
        artists.push(artist.value);
    }

    // Prepare songs
    songs = []
    for (var i = 0; i < titles.length; i++) {
        songs.push([titles[i], artists[i]])
    }

    // Set songs
    return songs
}



// Gets the powerpoint by submitting songs
async function SubmitSongs() {
    // Get songs
    songs = getSongs();

    // Send POST request
    const rawResponse = await fetch("/pptx", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }, body: JSON.stringify({"songs":songs})
    });

    // Download powerpoint
    download(await rawResponse.blob());
}



// Get the parsed lyrics for the user to review
async function ReviewLyrics() {
    // Get songs
    songs = getSongs();

    // Send POST request
    const rawResponse = await fetch("/lyrics", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }, body: JSON.stringify({"songs":songs})
    });
    const json = await rawResponse.json();

    // Set lyrics
    document.getElementById("lyrics").value = json["lyrics"].join("\n\n")
    
    // Show and hide elements
    document.getElementById("songs").hidden = true;
    document.getElementById("lyricsContainer").hidden = false;
}