class Table {
    constructor(data, page = 1, options = {option: false, trash: false, edit: false, formAction: '', title: ''}) {
        this.index = 0;
        this.data = data;
        this.page = page;
        this.options = options;
        this.filteredData = [...data];
        this.init();
    }

    init() {
        const box = document.getElementById('box');
        if (box.querySelectorAll('.table').length !== 0) {
            this.index = box.querySelectorAll('.table').length
        }
        this.createTableContainer(box);
        this.renderTable();
        this.renderPagination();
    }

    createTableContainer(box) {
        const div = document.createElement('div');
        div.className = 'table-container';
        div.innerHTML = `
            <div class="table-options">
                <h6>${this.options.title}</h6>
                <div>
                    <button type="button" class="table-button"></button>
                    <input type="text" class="table-search" placeholder="Pesquisar..." oninput="table.searchTable()"/>
                </div>
            </div>
            <div class="table"></div>
            <div class="table-pagination"></div>
        `;
        box.appendChild(div);
    }

    renderTable() {
        const tableContainer = document.querySelectorAll('.table')[this.index];
        tableContainer.innerHTML = '';

        const table = document.createElement('table');
        const thead = document.createElement('thead');
        const tbody = document.createElement('tbody');

        const headers = this.createHeaders();
        thead.appendChild(this.createHeaderRow(headers));

        const paginatedData = this.paginateData();
        paginatedData.forEach(rowData => {
            tbody.appendChild(this.createDataRow(rowData, headers));
        });

        this.fillEmptyRows(tbody, headers, paginatedData.length);

        table.appendChild(thead);
        table.appendChild(tbody);
        tableContainer.appendChild(table);

        this.adjustColumnWidths(headers.length);
    }

    createHeaders() {
        let headers = Object.keys(this.data[0]);
        if (this.options.trash || this.options.edit) {
            headers.push('Ações');
        }
        if (this.options.option) {
            headers.unshift('|');
        }
        return headers;
    }

    createHeaderRow(headers) {
        const headerRow = document.createElement('tr');
        headers.forEach(header => {
            if (header !== 'detail' && header !== 'id') {
                const th = document.createElement('th');
                th.textContent = header.charAt(0).toUpperCase() + header.slice(1);
                headerRow.appendChild(th);
            }
        });
        return headerRow;
    }

    paginateData() {
        const start = (this.page - 1) * 10;
        return this.filteredData.slice(start, start + 10);
    }

    createDataRow(rowData) {
        const row = document.createElement('tr');
        if (this.options.option) {
            row.appendChild(this.createOptionButton(rowData.detail));
        }
        Object.entries(rowData).forEach(([key, value], index) => {
            if (key !== 'detail') {
                const td = document.createElement('td');
                if (key === 'id') {
                    td.style.display = 'none'
                }
                td.textContent = value;
                row.appendChild(td);
            }
        });
        if (this.options.trash || this.options.edit) {
            row.appendChild(this.createActions(rowData));
        }
        return row;
    }

    createOptionButton(detail) {
        const option = document.createElement('td');
        option.title = 'Detalhes'
        option.innerHTML = `
        <button class="exemption" onclick="popupDetail('${detail}', true)">
            <i class="fa-solid fa-circle-exclamation"></i>
        </button>`;
        return option;
    }

    createActions(rowData) {
        const action = document.createElement('td');
        action.innerHTML = `<div class="table-actions"></div>`;
        const actionsContainer = action.querySelector('.table-actions');
        if (this.options.edit && rowData.id !== '') {
            const editButton = this.createEditButton(rowData);
            actionsContainer.appendChild(editButton);
        }
        if (this.options.trash && rowData.id !== '') {
            const trashButton = this.createTrashButton(rowData);
            actionsContainer.appendChild(trashButton);
        }
        return action;
    }

    createEditButton(rowData) {
        const button = document.createElement('button');
        button.className = 'edit';
        button.title = 'Editar'
        button.setAttribute('onclick',
            `popup(${JSON.stringify(labels).replace(/"/g, "'")}, 
            ${JSON.stringify(Object.values(rowData)).replace(/"/g, "'")}, 
            ['Editar'], 'Editar', '${this.options.formAction}','', true)`);
        button.innerHTML = '<i class="fa-light fa-pencil"></i>';
        return button;
    }

    createTrashButton(rowData) {
        const button = document.createElement('button');
        button.className = 'trash';
        button.title = 'Excluír'
        button.innerHTML = '<i class="fa-light fa-trash"></i>';
        const action = this.options.formAction.replace(/editar/, 'deletar')
        const locale = window.location.href
        button.addEventListener('click', async function () {
            const response = await fetch(`${action}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({id: Object.values(rowData)[0]})
            });

            if (response.ok) {
                window.location.href = locale;
            }
        })
        return button;
    }

    fillEmptyRows(tbody, headers, dataLength) {
        const emptyRows = 10 - dataLength;
        for (let i = 0; i < emptyRows; i++) {
            const emptyRow = document.createElement('tr');
            headers.forEach(() => {
                const emptyTd = document.createElement('td');
                emptyTd.textContent = '';
                emptyRow.appendChild(emptyTd);
            });
            tbody.appendChild(emptyRow);
        }
    }

    adjustColumnWidths(headersLength) {
        document.querySelectorAll('.table')[this.index].querySelectorAll('th').forEach(element => {
            element.style.width = `calc(${100 / headersLength}% - ${(64 / headersLength).toFixed(1)}px)`;
        });
        if (this.options.option) {
            document.querySelectorAll('.table')[this.index].querySelector('th').style.width = '64px'
        }
    }

    renderPagination() {
        const paginationControls = document.querySelectorAll('.table-pagination')[this.index];
        paginationControls.innerHTML = '';
        const totalPages = Math.ceil(this.filteredData.length / 10);

        for (let i = 1; i <= totalPages; i++) {
            const button = document.createElement('button');
            button.textContent = `${i}`;

            button.style = (i === this.page)
                ? 'background: var(--dark-slate); color: var(--white);' : 'background: var(--pale-lavender); color: #000;';

            button.addEventListener('click', () => {
                this.page = i;
                this.renderTable();
                this.renderPagination();
            });
            if (typeof f === 'function') {
                button.setAttribute('onclick', 'f()')
            }

            paginationControls.appendChild(button);
        }
    }


    searchTable() {
        const searchTerm = document.querySelector('.table-search').value.toLowerCase();
        this.filteredData = this.data.filter(row =>
            Object.values(row).some(value =>
                String(value).toLowerCase().includes(searchTerm)
            )
        );
        this.page = 1;
        this.renderTable();
        this.renderPagination();
    }
}
