function popupDetail(value, status) {
    if (status) {
        const box = document.getElementById('box')
        const popupContainer = document.createElement('div')
        popupContainer.innerHTML = `
        <div id="popup-detail-data">
            <div>
                <h5>Detalhes</h5>
                <i class="fa-light fa-xmark" onclick="popupDetail(null, false)"></i>
            </div>
            <p>${value}</p>
        </div>
    `
        popupContainer.addEventListener('click', (e) => {
            if (e.target === popupContainer) {
                popupDetail(null, false)
            }
        })
        popupContainer.className = 'popup-detail-container'
        box.appendChild(popupContainer)
    } else {
        document.querySelector('.popup-detail-container').remove()
    }

}