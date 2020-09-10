/**
 * Updates the interface theme
 * @param {bool} theme - False for light mode, true for dark mode
 * @returns {void}
 */
function UpdateTheme(theme = null) {
    // Get theme from localStorage
    if (theme === null) {
        theme = localStorage.getItem("theme");
    }

    // Detect preferred color scheme
    if (theme === null) {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            theme = "Dark";
        }
        else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: light)').matches) {
            theme = "Light";
        }
    }
    
    // Apply theme
    if (theme === "Dark") {
        document.body.classList.add("dark");
    }
    else {
        document.body.classList.remove("dark");
    }

    // Save theme
    localStorage.setItem("theme", theme);
}
