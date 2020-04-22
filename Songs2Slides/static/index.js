// Declare global variables
setId = 0;  // Next valid song id number



// Adds a song
function Add() {
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



// Prepares form data for a POST request
function PrepareForm() {
    // Get song info
    var titles = [];
    for (title of document.getElementsByClassName("title")) {
        titles.push(title.value);
    }
    var artists = [];
    for (artist of document.getElementsByClassName("artist")) {
        artists.push(artist.value);
    }

    // Prepare data
    data = []
    for (var i = 0; i < titles.length; i++) {
        data.push([titles[i], artists[i]])
    }

    // Set data
    document.getElementsByName("data")[0].value = JSON.stringify(data)
}