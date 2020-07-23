// Updates the interface theme
function UpdateTheme(theme = null) {
    // Get theme from localStorage
    if (theme === null) {
        theme = localStorage.getItem("theme") || "Light";
    }
    
    // Apply theme
    if (theme == "Dark") {
        document.body.classList.add("dark");
    }
    else {
        document.body.classList.remove("dark");
    }

    // Save theme
    localStorage.setItem("theme", theme);
}
