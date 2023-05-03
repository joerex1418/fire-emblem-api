
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
        } else {
            element.classList.remove("selected")
        }

    });
}

function viewCharacterData(e) {
    
}

// Add event listener

document.querySelectorAll(".btn.character").forEach(element => {
    element.addEventListener("click", characterSelect)
});
