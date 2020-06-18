// Declare global variables
setId = 0;  // Next valid song id number



// Finishes setting up the page
function onLoad() {
    // Add song
    AddSong();
}



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



// Get the parsed lyrics for the user to review
async function ReviewLyrics() {
    // Show and hide elements
    document.getElementById("rawLyrics").value = "Loading lyrics...";
    document.getElementById("rawLyrics").readOnly = true;
    document.getElementById("errors").textContent = "";
    document.getElementById("songsContainer").hidden = true;
    document.getElementById("lyricsContainer").hidden = false;

    // Get songs
    songs = getSongs();

    // Send POST request
    const rawResponse = await fetch("/lyrics", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }, body: JSON.stringify({"songs":songs,"settings":JSON.parse(localStorage.getItem("settings"))})
    });
    const json = await rawResponse.json();

    // Set lyrics
    document.getElementById("rawLyrics").value = json["lyrics"].join("\n\n")
    document.getElementById("rawLyrics").readOnly = false;

    // Set errors
    if (json["errors"].length != 0)
    {
        errors = "The lyrics to the following songs could not be found: ";
        for (error of json["errors"]) {
            errors += `"${error[0]}" by "${error[1]}", `;
        }
        errors = errors.slice(0, -2); // Remove trailing ', '
        document.getElementById("errors").textContent = errors;
    }
}



// Gets the powerpoint by submitting lyrics
async function SubmitLyrics() {
    // Get lyrics
    lyrics = document.getElementById("rawLyrics").value.split('\n\n');

    // Set hidden form values
    document.getElementById("pptxSettingsField").value = localStorage.getItem("settings");
    document.getElementById("lyricsField").value = JSON.stringify(lyrics);
    
    // Show and hide elements
    document.getElementById("lyricsContainer").hidden = true;
    document.getElementById("thankyou").hidden = false;
}



// Makes the songs div visible
function Back() {
    document.getElementById("songsContainer").hidden = false;
    document.getElementById("lyricsContainer").hidden = true;
    document.getElementById("thankyou").hidden = true;
    document.getElementById("settings").hidden = true;
}



// Makes the songs div visible and removes songs
function Reset() {
    // Remove songs
    songs = document.getElementsByClassName("song");
    while (songs.length > 0) {
        // Get song
        songs[0].parentNode.removeChild(songs[0]);
    }

    // Reset pptx file input
    document.getElementsByName("pptxFile")[0].value = null;

    // Add blank song
    AddSong();

    // Makes songs visible
    Back();
}
