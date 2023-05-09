
// document.getElementById().textContent

// Event handler function
function viewSelect(e) {
    document.querySelectorAll("#viewselect-btns > .btn").forEach(element => {
        if (element == e.target) {
            element.classList.add("selected")
        } else {
            element.classList.remove("selected")
        }
    });
}
document.querySelectorAll("#viewselect-btns > .btn").forEach(element => {
    element.addEventListener("click", viewSelect)
})

function characterSelect(e) {
    document.querySelectorAll("#item-scroller .btn").forEach(element => {
        if (element == e.target) {
            element.classList.add("selected")
        } else {
            element.classList.remove("selected")
        }
    });
}
document.querySelectorAll("#item-scroller .btn").forEach(element => {
    element.addEventListener("click", characterSelect)
});

function viewCharacterData(selected_name) {
    fetch("/api/engage?" + new URLSearchParams({
        "get":"character_data","name":selected_name
    })).then((response) => {return response.json();}).then(data => {
        document.getElementById("character-content").innerHTML = data["html"]
    })
}

document.getElementById("show-hide-btn").addEventListener("click", function(e) {
    if (e.target.textContent == "Show") {
        e.target.textContent = "Hide"
        document.getElementById("item-scroller").classList.remove("hidden")
    } else {
        e.target.textContent = "Show"
        document.getElementById("item-scroller").classList.add("hidden")
    }
})


