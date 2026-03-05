fetch("data.json")
.then(response => response.json())
.then(data => {

    let table = document.querySelector("#dataTable tbody");

    for (let i = 0; i < data.odczyt1.length; i++) {

        let row = document.createElement("tr");

        row.innerHTML = `
            <td>${data.odczyt1[i]}</td>
            <td>${data.odczyt2[i]}</td>
            <td>${data.v[i]}</td>
            <td>${data.vv[i]}</td>
        `;

        table.appendChild(row);
    }

    document.getElementById("mean_v").textContent = data.mean_v;
    document.getElementById("sum_vv").textContent = data.sum_vv;

});