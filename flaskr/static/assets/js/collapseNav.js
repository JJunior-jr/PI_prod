function collapseNav() {
    let nav = document.querySelectorAll("nav")[0].style
    let content = document.querySelectorAll(".content")[0].style
    let toggle = document.querySelectorAll(".collapse-toggle")[0].querySelectorAll('i')[0].classList
    if (nav.left !== "-280px") {
        content.width = "100%"
        nav.left = "-280px"
        toggle.replace("fa-xmark", "fa-bars-staggered")
    } else {
        content.width = "calc(100% - 280px)"
        nav.left = "0"
        toggle.replace("fa-bars-staggered","fa-xmark")
    }
}