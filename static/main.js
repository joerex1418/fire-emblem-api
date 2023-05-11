document.getElementById("menu-btn").addEventListener("click", function(e) {
    // document.getElementById("menu-overlay").classList.remove("hidden")
    document.getElementById("character-menu").classList.remove("hidden")
})
document.getElementById("close-menu-btn").addEventListener("click", function(e) {
    document.getElementById("character-menu").classList.add("hidden")
})