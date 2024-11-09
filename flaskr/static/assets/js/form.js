function norm(str, lower) {
    let new_str = str.normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "")
        .replace(/ç/g, "c")
        .replace(/[^\w\s-]/g, "")
        .trim()
        .replace(/\s+/g, '-');
    if (lower) {
        new_str.toLowerCase()
    }
    return new_str
}

function form(input, values, buttons, url, message, popupStatus) {
    let box = document.getElementById('box')
    if (popupStatus)
        box = document.querySelector('.form-content').querySelector('#box')

    box.innerHTML = `
        <form action="/${url}" method="post">
            <div class="form-inputs"></div>
            <div class="form-buttons"></div>
        </form>
    `;
    if (message !== '') {
        const span = document.createElement('span')
        span.textContent = message
        document.querySelector('form').insertAdjacentElement('afterbegin', span)
    }

    let inputsContainer = document.querySelector('.form-inputs')
    let buttonsContainer = document.querySelector('.form-buttons')

    if (popupStatus) {
        inputsContainer = document.querySelector('.form-content').querySelector('.form-inputs')
        buttonsContainer = document.querySelector('.form-content').querySelector('.form-buttons')
    }

    const inputsFragment = document.createDocumentFragment()
    if (input.length <= 5) {
        inputsContainer.style.width = '360px'
    }
    input.forEach(({label, type, appear = true}, index) => {
        if (appear) {
            const div = document.createElement('div')
            const labelElement = document.createElement('label')
            let inputElement = document.createElement('input')

            const id = label.toLowerCase()

            if (type === 'select') {
                inputElement = document.createElement('select')
                input[index].options.forEach(value => {
                    const option = document.createElement('option')
                    option.value = value.replace(/[\u0300-\u036f]/g, "")
                    option.textContent = value
                    inputElement.appendChild(option)
                })
                if (values[index] !== undefined) {
                    inputElement.value = values[index].replace(/[\u0300-\u036f]/g, "")
                }
            } else if (type === 'textarea') {
                inputElement = document.createElement('textarea')
                inputElement.maxLength = 1024
            } else {
                inputElement.type = type
                inputElement.maxLength = 120
            }
            inputElement.required = true
            labelElement.htmlFor = inputElement.id = inputElement.name = norm(id)
            if (values[index] !== undefined && type !== 'select') {
                if (type === 'datetime-local') {
                    const [date, time] = values[index].split(' ');
                    let [day, month, year] = date.split('/')
                    let [hour, min] = time.split(':')
                    values[index] = `${year}-${month}-${day}T${hour}:${min}`
                    const date_today = new Date()
                    date_today.setDate(date_today.getUTCDate() + 1)
                    inputElement.min = date_today.toISOString().split('T')[0]
                    inputElement.max = date_today.toISOString().split('T')[0]
                }
                inputElement.value = values[index]
            }
            labelElement.textContent = label
            if (label === 'id') {
                inputElement.type = 'hidden'
                div.style.display = 'none'
                div.append(inputElement)
            } else {
                div.append(labelElement, inputElement)
            }
            if (type === 'textarea') {
                div.style = `flex: 0 0 740px; display: flex; flex-direction: column; flex-wrap: wrap;`
            }
            inputsFragment.appendChild(div)
        }
    })
    inputsContainer.appendChild(inputsFragment)

    buttons.forEach(buttonText => {
        const button = document.createElement('button')
        button.type = "submit"
        button.textContent = buttonText
        buttonsContainer.appendChild(button)
    })

    if (!locale && document.querySelector('.option') === null) {
        const forgotPasswordButton = document.createElement("button")
        forgotPasswordButton.type = 'button'
        forgotPasswordButton.className = 'option'
        forgotPasswordButton.textContent = 'Esqueceu a senha?'
        forgotPasswordButton.addEventListener('click', () => {
            popup([{label: 'Email', type: 'email'}], [], ['Enviar'], 'Esqueci a senha', 'esqueciSenha', '', true)
        })
        inputsContainer.insertAdjacentElement('afterend', forgotPasswordButton)
    }
}
