/**
 * Finishes setting up the page
 * @returns {void}
 */
function onLoad() {
    // Load settings
    if (localStorage.getItem("settings") == null) {
        resetSettings();
    }
    else {
        loadSettings(JSON.parse(localStorage.getItem("settings")));
    }
}



// Loads settings
/**
 * Loads settings
 * @param {object} settings - The settings object
 * @returns {void}
 */
function loadSettings(settings) {
    // Interface settings (not stored with other settings)
    UpdateTheme();
    if (document.body.classList.contains("dark")) {
        document.getElementById("theme").value = "Dark";
    }
    else {
        document.getElementById("theme").value = "Light";
    }

    // Parsing settings
    document.getElementById("title-slides").checked = settings["title-slides"];
    document.getElementById("slide-between-songs").checked = settings["slide-between-songs"];
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



/**
 * Saves settings to localStorage
 * @returns {void}
 */
function saveSettings() {
    // Save interface settings and update interface
    UpdateTheme(document.getElementById("theme").value);

    // Get settings
    const settings = {
        // Parsing settings
        "title-slides": document.getElementById("title-slides").checked,
        "slide-between-songs": document.getElementById("slide-between-songs").checked,
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



/**
 * Resets all settings to their default values
 * @returns {void}
 */
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
