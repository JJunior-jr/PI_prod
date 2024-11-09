function charts(data) {
    data.forEach((ghp, index) => {
        const div = document.createElement('div')
        div.id = `graph-${index}`
        document.getElementById('graphs').appendChild(div)
        let chart = new ApexCharts(document.getElementById(`graph-${index}`), ghp);
        chart.render();
    })
}