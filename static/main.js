document.getElementById("menu-btn").addEventListener("click", function(e) {
    document.getElementById("menu").classList.remove("hidden")
})
document.getElementById("close-menu-btn").addEventListener("click", function(e) {
    document.getElementById("menu").classList.add("hidden")
})


document.querySelectorAll("#menu .menu-list > .btn").forEach(element => {
    let menu_container_id = element.parentElement.id
    element.addEventListener("click", function(e) {
        document.querySelectorAll(`#${menu_container_id} > .btn`).forEach(btn_elem => {
            if (btn_elem == element) {
                btn_elem.classList.add("selected")
                var character_name = btn_elem.dataset.name
                fetch(`/api/engage/character?name=${character_name}`)
                .then((response) => {return response.json()})
                .then(data => {
                    document.getElementById("container-character-data").innerHTML = data.html
                })

            } else {
                btn_elem.classList.remove("selected")
            }
        })

        document.getElementById("close-menu-btn").click()
        document.documentElement.scrollTop = 0;
    })
})