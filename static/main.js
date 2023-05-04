
// fetch("/path/to/url/endpoint")
// .then((response) => { return response.json(); })
// .then(data => {
//     // do stuff with your JSON data here
// })

// Event handler function
function characterSelect(e) {
    let selected_name = e.target.getAttribute("name")
    document.querySelectorAll(".btn.character").forEach(element => {
        let name = element.getAttribute("name")
        if (selected_name == name) {
            element.classList.add("selected")
            viewCharacterData(selected_name)
        } else {
            element.classList.remove("selected")
        }

    });
}

function viewCharacterData(selected_name) {
    fetch("/api/engage?" + new URLSearchParams({
        "get":"character_data","name":selected_name
    })).then((response) => {return response.json();}).then(data => {
        document.getElementById("character-content").innerHTML = data["html"]
    })
}

// Add event listener

document.querySelectorAll(".btn.character").forEach(element => {
    element.addEventListener("click", characterSelect)
});
