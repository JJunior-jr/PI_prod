function flash(route, url, sessionFlash, sessionIdItem) {
    let message = sessionFlash !== null && route === window.location.href.split('/')[3] ? sessionFlash : ''
    const tableButton = document.querySelector('.table-button');
    if (tableButton !== undefined) {
        tableButton.textContent = 'Cadastrar';
        tableButton.setAttribute('onclick',
            `popup(${JSON.stringify(labels).replace(/"/g, "'")},
        '',
        ['Cadastrar'],
        'Cadastrar',
        '${url}','${message}', true);`
        );
    }
    if (message !== '') {
        if (sessionIdItem !== null) {
            document.querySelectorAll('tr').forEach(e => {
                e.querySelectorAll('td').forEach(j => {
                    if (j.textContent === sessionIdItem) {
                        const element = e.lastElementChild.querySelector('.edit')
                        const newAction = element.attributes[2].nodeValue.replace("'', true", `'${message}', true`)
                        element.setAttribute('onclick', newAction);
                        element.click()
                    }
                })
            })
        } else {
            tableButton.click()
        }
    }
}