function accountToggle() {
    let userToggle = document.querySelectorAll(".account-toggle")[0]
    let toggle = userToggle.querySelectorAll(".fa-light")[0].style
    let boxAccountConfig = document.querySelectorAll(".box-account-config")[0].style
    if (boxAccountConfig.top === "-102px" || boxAccountConfig.top === "") {
        boxAccountConfig.top = "49px"
        userToggle.style.background = "var(--cool-gray)"
        toggle.rotate = "-180deg"
    } else {
        boxAccountConfig.top = "-102px"
        userToggle.style.background = ""
        toggle.rotate = "0deg"
    }
}