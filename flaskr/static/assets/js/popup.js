function popup(name_inputs, values_inputs, name_buttons, title, url, message, status) {
    if (status) {
        if (document.querySelector('header') !== null)
            document.querySelector('header').style.display = 'none'
        const box = document.getElementById('box')
        const popupDiv = document.createElement('div')
        popupDiv.className = 'popup'
        if (document.querySelector('nav').style.left === '-280px') {
            popupDiv.style.width = "100vw"
            popupDiv.style.left = "0"
        }
        const form_content = document.createElement('div')
        form_content.className = 'form-content'
        form_content.innerHTML = `
            <div class="container">
                <div class="title-icon">
                    <h4>${title}</h4>
                    <i class="fa-light fa-xmark" onclick="popup()"></i>
                </div>
                <hr color="C8CBD9" size="1"/>
                <div id="box">    
                </div>
            </div>
        `;
        popupDiv.appendChild(form_content)
        box.appendChild(popupDiv)
        form(name_inputs, values_inputs, name_buttons, url, message,true)
    } else {
        if (document.querySelector('.form-content').querySelector('h4').textContent === "Minha Conta") {
            accountToggle()
        }
        document.querySelector('.popup').remove()
        document.querySelector('header').style.display = 'flex'
    }
}