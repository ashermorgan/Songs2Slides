// Declare global variables
setId = 0;  // Next valid song id number



// Finishes setting up the page
function onLoad() {
    // Load settings
    if (localStorage.getItem("settings") == null) {
        resetSettings();
    }
    else {
        loadSettings(JSON.parse(localStorage.getItem("settings")));
    }

    // Add song
    AddSong();
}



// Shows settings interface
function showSettings() {
    document.getElementById("songs").hidden = true;
    document.getElementById("lyricsContainer").hidden = true;
    document.getElementById("thankyou").hidden = true;
    document.getElementById("settings").hidden = false;
}



// Loads settings
function loadSettings(settings) {
    // Parsing settings
    document.getElementById("title-slides").checked = settings["title-slides"];
    document.getElementById("lines-per-slide").value = settings["lines-per-slide"];
    document.getElementById("remove-parentheses").checked = settings["remove-parentheses"];

    // Slide settings
    document.getElementById("slide-width").value = settings["slide-width"];
    document.getElementById("slide-height").value = settings["slide-height"];
    document.getElementById("slide-color").value = settings["slide-color"];

    // Margin settings
    document.getElementById("margin-left").value = settings["margin-left"];
    document.getElementById("margin-right").value = settings["margin-right"];
    document.getElementById("margin-top").value = settings["margin-top"];
    document.getElementById("margin-bottom").value = settings["margin-bottom"];

    // Font settings
    document.getElementById("font-family").value = settings["font-family"];
    document.getElementById("font-size").value = settings["font-size"];
    document.getElementById("font-bold").checked = settings["font-bold"];
    document.getElementById("font-italic").checked = settings["font-italic"];
    document.getElementById("font-color").value = settings["font-color"];

    // Pharagraph settings
    document.getElementById("vertical-alignment").value = settings["vertical-alignment"];
    document.getElementById("line-spacing").value = settings["line-spacing"];
    document.getElementById("word-wrap").checked = settings["word-wrap"];
}



// Saves settings to local storage
function saveSettings() {
    // Get settings
    const settings = {
        // Parsing settings
        "title-slides": document.getElementById("title-slides").checked,
        "lines-per-slide": Number(document.getElementById("lines-per-slide").value),
        "remove-parentheses": document.getElementById("remove-parentheses").checked,
        
        // Slide settings
        "slide-width": Number(document.getElementById("slide-width").value),
        "slide-height": Number(document.getElementById("slide-height").value),
        "slide-color": document.getElementById("slide-color").value,
        
        // Margin settings
        "margin-left": Number(document.getElementById("margin-left").value),
        "margin-right": Number(document.getElementById("margin-right").value),
        "margin-top": Number(document.getElementById("margin-top").value),
        "margin-bottom": Number(document.getElementById("margin-bottom").value),

        // Font settings
        "font-family": document.getElementById("font-family").value,
        "font-size": Number(document.getElementById("font-size").value),
        "font-bold": document.getElementById("font-bold").checked,
        "font-italic": document.getElementById("font-italic").checked,
        "font-color": document.getElementById("font-color").value,

        // Pharagraph settings
        "vertical-alignment": document.getElementById("vertical-alignment").value,
        "line-spacing": Number(document.getElementById("line-spacing").value),
        "word-wrap": document.getElementById("word-wrap").checked,
    }

    // Save settings
    localStorage.setItem("settings", JSON.stringify(settings));
}



// Resets all settings to their default values
async function resetSettings() {
    // Send POST request
    const rawResponse = await fetch("/settings.json", {
        method: 'GET'
    });
    const json = await rawResponse.json();

    // Load changes
    loadSettings(json);

    // Save changes
    localStorage.setItem("settings", JSON.stringify(json));
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
        }, body: JSON.stringify({"songs":songs,"settings":JSON.parse(localStorage.getItem("settings"))})
    });

    // Download powerpoint
    download(await rawResponse.blob());
    
    // Show and hide elements
    document.getElementById("songs").hidden = true;
    document.getElementById("thankyou").hidden = false;
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
        }, body: JSON.stringify({"songs":songs,"settings":JSON.parse(localStorage.getItem("settings"))})
    });
    const json = await rawResponse.json();

    // Set lyrics
    document.getElementById("lyrics").value = json["lyrics"].join("\n\n")
    
    // Show and hide elements
    document.getElementById("songs").hidden = true;
    document.getElementById("lyricsContainer").hidden = false;
}



// Gets the powerpoint by submitting lyrics
async function SubmitLyrics() {
    // Get lyrics
    lyrics = document.getElementById("lyrics").value.split('\n\n');

    // Send POST request
    const rawResponse = await fetch("/pptx", {
        method: 'POST',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }, body: JSON.stringify({"lyrics":lyrics,"settings":JSON.parse(localStorage.getItem("settings"))})
    });

    // Download powerpoint
    download(await rawResponse.blob());
    
    // Show and hide elements
    document.getElementById("lyricsContainer").hidden = true;
    document.getElementById("thankyou").hidden = false;
}



// Makes the songs div visible
function Back() {
    document.getElementById("songs").hidden = false;
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

    // Add blank song
    AddSong();

    // Makes songs visible
    Back();
}
