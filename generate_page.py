# Generate interactive HTML page for Surveying Calculations

html = """
<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<title>Kalkulator Geodezyjny - Kolimacja, Inklinacja, Atmosfera</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; padding: 20px; background-color: #f4f7f6; color: #333; }
    h1 { color: #2c3e50; }
    
    /* Tabs Styles */
    .tab { overflow: hidden; border: 1px solid #ccc; background-color: #e0e6ed; border-radius: 5px 5px 0 0; }
    .tab button { background-color: inherit; float: left; border: none; outline: none; cursor: pointer; padding: 14px 24px; transition: 0.3s; font-size: 16px; font-weight: bold; color: #555; }
    .tab button:hover { background-color: #cfd9e5; }
    .tab button.active { background-color: #fff; color: #2980b9; border-bottom: 2px solid #2980b9; }
    .tabcontent { display: none; padding: 20px; border: 1px solid #ccc; border-top: none; background-color: #fff; border-radius: 0 0 5px 5px; box-shadow: 0 4px 8px rgba(0,0,0,0.05); }
    
    /* Sub-tabs Styles */
    .sub-tab { overflow: hidden; margin-bottom: 15px; border-bottom: 1px solid #ddd; }
    .sub-tab button { background-color: transparent; float: left; border: none; outline: none; cursor: pointer; padding: 10px 20px; transition: 0.3s; font-size: 14px; color: #666; }
    .sub-tab button.active { color: #e67e22; font-weight: bold; border-bottom: 2px solid #e67e22; }
    .sub-tabcontent { display: none; padding: 15px 0; }

    table { border-collapse: collapse; width: 100%; margin-top: 15px; margin-bottom: 15px; }
    th, td { border: 1px solid #ddd; padding: 10px; text-align: center; }
    th { background-color: #f8f9fa; color: #333; }
    input[type="text"], input[type="number"] { width: 100px; padding: 5px; border: 1px solid #ccc; border-radius: 3px; }
    
    .btn { background-color: #2980b9; color: white; border: none; padding: 10px 20px; cursor: pointer; border-radius: 4px; font-size: 14px; margin: 5px 0; }
    .btn:hover { background-color: #1f6391; }
    .btn-danger { background-color: #e74c3c; }
    .btn-danger:hover { background-color: #c0392b; }
    
    .panel { background: #fdfdfd; padding: 15px; border: 1px solid #eee; border-left: 4px solid #2980b9; margin-bottom: 20px; }
    .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
</style>

<script>
// --- CORE UTILS ---
function switchTab(evt, tabName) {
    let tabcontents = document.getElementsByClassName("tabcontent");
    for (let i = 0; i < tabcontents.length; i++) tabcontents[i].style.display = "none";
    let tablinks = document.getElementsByClassName("tablinks");
    for (let i = 0; i < tablinks.length; i++) tablinks[i].className = tablinks[i].className.replace(" active", "");
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

function switchSubTab(evt, tabName) {
    let subtabcontents = document.getElementsByClassName("sub-tabcontent");
    for (let i = 0; i < subtabcontents.length; i++) subtabcontents[i].style.display = "none";
    let subtablinks = document.getElementsByClassName("sub-tablinks");
    for (let i = 0; i < subtablinks.length; i++) subtablinks[i].className = subtablinks[i].className.replace(" active", "");
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";
}

// --- KOLIMACJA ---
let kolimacjaRowCount = 0;

function addKolimacjaRow(o1 = '', o2 = '') {
    let table = document.getElementById("kolimacja_table").getElementsByTagName('tbody')[0];
    let row = table.insertRow();
    row.id = "k_row_" + kolimacjaRowCount;
    
    row.insertCell(0).innerText = kolimacjaRowCount + 1;
    row.insertCell(1).innerHTML = `<input type="number" step="any" id="k_o1_${kolimacjaRowCount}" value="${o1}">`;
    row.insertCell(2).innerHTML = `<input type="number" step="any" id="k_o2_${kolimacjaRowCount}" value="${o2}">`;
    row.insertCell(3).innerHTML = `<span id="k_c_${kolimacjaRowCount}">-</span>`;
    row.insertCell(4).innerHTML = `<span id="k_v_${kolimacjaRowCount}">-</span>`;
    row.insertCell(5).innerHTML = `<span id="k_vv_${kolimacjaRowCount}">-</span>`;
    row.insertCell(6).innerHTML = `<button class="btn btn-danger" onclick="removeRow('k_row_${kolimacjaRowCount}')">Usuń</button>`;
    
    kolimacjaRowCount++;
}

function removeRow(rowId) {
    let row = document.getElementById(rowId);
    row.parentNode.removeChild(row);
}

function calcKolimacja() {
    let c_values = [];
    let table = document.getElementById("kolimacja_table").getElementsByTagName('tbody')[0];
    let rows = table.rows;
    
    // Calculate C for each row
    for (let i = 0; i < rows.length; i++) {
        let id_num = rows[i].id.split('_')[2];
        let o1 = parseFloat(document.getElementById("k_o1_" + id_num).value);
        let o2 = parseFloat(document.getElementById("k_o2_" + id_num).value);
        
        if (!isNaN(o1) && !isNaN(o2)) {
            // Zakładamy system gradowy (400g). Wzór: c = (O2 - (O1 +/- 200)) / 2
            let o1_opp = o1 < 200 ? o1 + 200 : o1 - 200;
            let c = ((o2 - o1_opp) / 2) * 10000; // konwersja na cc
            c_values.push({id: id_num, c: c});
            document.getElementById("k_c_" + id_num).innerText = c.toFixed(2) + " cc";
        }
    }
    
    if (c_values.length === 0) return;

    let sum_c = 0;
    c_values.forEach(item => sum_c += item.c);
    let mean_c = sum_c / c_values.length;
    
    let sum_vv = 0;
    c_values.forEach(item => {
        let v = item.c - mean_c;
        let vv = v * v;
        sum_vv += vv;
        document.getElementById("k_v_" + item.id).innerText = v.toFixed(2);
        document.getElementById("k_vv_" + item.id).innerText = vv.toFixed(2);
    });
    
    let n = c_values.length;
    let m_c = n > 1 ? Math.sqrt(sum_vv / (n * (n - 1))) : 0;
    
    document.getElementById("k_mean_c").innerText = mean_c.toFixed(2) + " cc";
    document.getElementById("k_m_c").innerText = m_c.toFixed(2) + " cc";
    
    // Przekaż kolimację do zakładki Inklinacja i poprawki kątów
    document.getElementById("ink_kolimacja_input").value = mean_c.toFixed(2);
    window.currentKolimacjaCC = mean_c;
}

function correctAngles() {
    let hz = parseFloat(document.getElementById("k_input_hz").value);
    let v = parseFloat(document.getElementById("k_input_v").value);
    let c_cc = window.currentKolimacjaCC || 0;
    
    if (isNaN(hz) || isNaN(v)) {
        alert("Wprowadź poprawne kąty Hz i V."); return;
    }
    
    let c_grad = c_cc / 10000;
    let v_rad = v * Math.PI / 200; // Konwersja grad na rad
    
    // Poprawka kolimacyjna: H = H' +/- c * cosec(z)
    let poprawka = c_grad / Math.sin(v_rad);
    let hz_corr = hz + poprawka; // Uproszczone dodawanie, znak zależy od położenia
    
    document.getElementById("k_corrected_hz").innerText = hz_corr.toFixed(4) + " g";
}

function loadKolimacjaFile(event) {
    let file = event.target.files[0];
    if (!file) return;
    let reader = new FileReader();
    reader.onload = function(e) {
        let lines = e.target.result.split('\\n');
        lines.forEach(line => {
            let parts = line.split(/[\\s,;]+/);
            if (parts.length >= 2) {
                let o1 = parseFloat(parts[0]);
                let o2 = parseFloat(parts[1]);
                if (!isNaN(o1) && !isNaN(o2)) addKolimacjaRow(o1, o2);
            }
        });
    };
    reader.readAsText(file);
}

// --- INKLINACJA ---
let inklinacjaRowCount = 0;

function addInklinacjaRow() {
    let table = document.getElementById("inklinacja_table").getElementsByTagName('tbody')[0];
    let row = table.insertRow();
    row.id = "i_row_" + inklinacjaRowCount;
    
    row.insertCell(0).innerText = "Cel Wysoki";
    row.insertCell(1).innerHTML = `<input type="number" step="any" id="i_o1_${inklinacjaRowCount}">`;
    row.insertCell(2).innerHTML = `<input type="number" step="any" id="i_o2_${inklinacjaRowCount}">`;
    row.insertCell(3).innerHTML = `<span id="i_v_${inklinacjaRowCount}">-</span>`;
    row.insertCell(4).innerHTML = `<span id="i_vv_${inklinacjaRowCount}">-</span>`;
    row.insertCell(5).innerHTML = `<button class="btn btn-danger" onclick="removeRow('i_row_${inklinacjaRowCount}')">Usuń</button>`;
    
    inklinacjaRowCount++;
}

function calcInklinacja() {
    let z_grad = parseFloat(document.getElementById("ink_z").value);
    let c_cc = parseFloat(document.getElementById("ink_kolimacja_input").value) || 0;
    
    if (isNaN(z_grad)) { alert("Podaj kąt zenitalny Z."); return; }
    
    let z_rad = z_grad * Math.PI / 200;
    let c_grad = c_cc / 10000;
    let table = document.getElementById("inklinacja_table").getElementsByTagName('tbody')[0];
    let rows = table.rows;
    let i_values = [];
    
    for (let idx = 0; idx < rows.length; idx++) {
        let id_num = rows[idx].id.split('_')[2];
        let o1 = parseFloat(document.getElementById("i_o1_" + id_num).value);
        let o2 = parseFloat(document.getElementById("i_o2_" + id_num).value);
        
        if (!isNaN(o1) && !isNaN(o2)) {
            // Ze wzoru: i = ((O_II - O_I +/- 200) / 2) * tg(z) - c / cos(z)
            let diff = o2 - o1;
            let corrected_diff = diff < 0 ? diff + 200 : (diff > 200 ? diff - 200 : diff);
            let i_val = (corrected_diff / 2) * Math.tan(z_rad) - (c_grad / Math.cos(z_rad));
            i_values.push({id: id_num, i: i_val * 10000}); // na cc
        }
    }
    
    if (i_values.length === 0) return;
    
    let sum_i = 0;
    i_values.forEach(item => sum_i += item.i);
    let mean_i = sum_i / i_values.length;
    
    let sum_vv = 0;
    i_values.forEach(item => {
        let v = item.i - mean_i;
        let vv = v * v;
        sum_vv += vv;
        document.getElementById("i_v_" + item.id).innerText = v.toFixed(2);
        document.getElementById("i_vv_" + item.id).innerText = vv.toFixed(2);
    });
    
    let n = i_values.length;
    let m_i = n > 1 ? Math.sqrt(sum_vv / (n * (n - 1))) : 0;
    
    document.getElementById("i_mean").innerText = mean_i.toFixed(2) + " cc";
    document.getElementById("i_error").innerText = m_i.toFixed(2) + " cc";
}

// --- ATMOSFERA ---
function calcAtmosfera() {
    let lambda_nm = parseFloat(document.getElementById("atm_lambda").value);
    let t_dry = parseFloat(document.getElementById("atm_t_dry").value);
    let t_wet_str = document.getElementById("atm_t_wet").value;
    let p = parseFloat(document.getElementById("atm_p").value);
    let d0 = parseFloat(document.getElementById("atm_d0").value) || 1000; // default 1km
    
    if (isNaN(lambda_nm) || isNaN(t_dry) || isNaN(p)) {
        alert("Wypełnij wymagane pola (Długość fali, Temp sucha, Ciśnienie)."); return;
    }
    
    // 1. Przeliczenie temp na Kelviny
    let T = t_dry + 273.15;
    
    // 2. Długość fali na mikrometry
    let lambda_um = lambda_nm / 1000.0;
    
    // 3. Wzór empiryczny Ciddora na Ng0 (atmosfera normalna)
    let Ng0 = 287.6155 + (4.8866 / Math.pow(lambda_um, 2)) + (0.0680 / Math.pow(lambda_um, 4));
    
    // 4. Ciśnienie pary wodnej (e)
    let e = 0;
    if (t_wet_str !== "") {
        let t_wet = parseFloat(t_wet_str);
        let Ew = 6.1078 * Math.exp((17.269 * t_wet) / (237.30 + t_wet));
        e = Ew - 0.000662 * p * (t_dry - t_wet);
    } // Jeżeli puste, e zostaje 0 (przeliczanie bez pomiaru wilgotności)
    
    // 5. Ng rzeczywiste
    let Ng = Ng0 * 0.269578 * (p / T) - 11.27 * (e / T);
    
    // 6. Poprawka (ppm)
    // Zakładamy Ng standardowe z pdf jako odniesienie dla danego sprzętu, tu podajemy różnicę.
    // Albo bezwzględne Ng i poprawkę względem próżni. Typowo: Delta D = D0 * (N_standard - N_rzeczywiste) * 10^-6
    // Użyjemy domyślnego Ngs = 280.43 (dla standardowej atm z pdf) jako bazy do poprawki.
    let Ngs = 280.43; 
    let delta_ppm = Ngs - Ng;
    
    let poprawka_mm = (d0 / 1000) * delta_ppm; // d0 w metrach
    let d_skorygowane = d0 + (poprawka_mm / 1000);
    
    document.getElementById("atm_res_ng0").innerText = Ng0.toFixed(2);
    document.getElementById("atm_res_ng").innerText = Ng.toFixed(2);
    document.getElementById("atm_res_ppm").innerText = delta_ppm.toFixed(2) + " ppm";
    document.getElementById("atm_res_poprawka").innerText = poprawka_mm.toFixed(2) + " mm na " + (d0/1000).toFixed(2) + " km";
    document.getElementById("atm_res_d_corr").innerText = d_skorygowane.toFixed(4) + " m";
}

let atmChart = null;
function drawAtmChart() {
    let ctx = document.getElementById('atmCanvas').getContext('2d');
    let labels = [];
    let data = [];
    
    for(let w = 400; w <= 1500; w += 50) {
        labels.push(w);
        let um = w / 1000.0;
        let ng0 = 287.6155 + (4.8866 / Math.pow(um, 2)) + (0.0680 / Math.pow(um, 4));
        data.push(ng0);
    }
    
    if(atmChart) atmChart.destroy();
    
    atmChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Ng0 względem λ (nm)',
                data: data,
                borderColor: '#2980b9',
                backgroundColor: 'rgba(41, 128, 185, 0.2)',
                borderWidth: 2,
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            scales: {
                x: { title: { display: true, text: 'Długość fali λ (nm)' } },
                y: { title: { display: true, text: 'Ng0' } }
            }
        }
    });
}
</script>
</head>
<body onload="addKolimacjaRow(); addInklinacjaRow();">

<h1>Kalkulator Geodezyjny</h1>

<div class="tab">
  <button class="tablinks active" onclick="switchTab(event, 'Kolimacja')">Kolimacja</button>
  <button class="tablinks" onclick="switchTab(event, 'Inklinacja')">Inklinacja</button>
  <button class="tablinks" onclick="switchTab(event, 'Atmosfera')">Atmosfera</button>
</div>

<div id="Kolimacja" class="tabcontent" style="display:block;">
    <h2>Obliczenia Kolimacji</h2>
    
    <div class="panel">
        <strong>Wczytaj z pliku (CSV/TXT - format: Odczyt_I Odczyt_II):</strong><br><br>
        <input type="file" id="k_file" accept=".txt,.csv" onchange="loadKolimacjaFile(event)">
    </div>

    <table id="kolimacja_table">
        <thead>
            <tr>
                <th>Seria</th>
                <th>Odczyt I [g]</th>
                <th>Odczyt II [g]</th>
                <th>Kolimacja (c) [cc]</th>
                <th>v</th>
                <th>vv</th>
                <th>Akcja</th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
    
    <button class="btn" onclick="addKolimacjaRow()">+ Dodaj Serię</button>
    <button class="btn" onclick="calcKolimacja()" style="background-color: #27ae60;">Oblicz Kolimację</button>
    
    <div class="panel" style="margin-top: 20px;">
        <h3>Wyniki:</h3>
        <b>Średnia kolimacja:</b> <span id="k_mean_c" style="color:red; font-weight:bold;">-</span><br>
        <b>Błąd kolimacji (mc):</b> <span id="k_m_c" style="color:red; font-weight:bold;">-</span>
    </div>

    <div class="panel">
        <h3>2. Parametry do poprawki</h3>
        Kąt poziomy (Hz) [g]: <input type="number" step="any" id="k_input_hz" value="159.9900"><br><br>
        Kąt pionowy (V) [g]: <input type="number" step="any" id="k_input_v" value="100.0000"><br><br>
        <button class="btn" onclick="correctAngles()">Oblicz Poprawiony Odczyt Hz</button><br><br>
        <b>Poprawiony kąt Hz:</b> <span id="k_corrected_hz" style="color:blue; font-size:18px; font-weight:bold;">-</span>
    </div>
</div>

<div id="Inklinacja" class="tabcontent">
    <h2>Obliczenia Inklinacji</h2>
    
    <div class="panel">
        <strong>Kąt zenitalny do celu wysokiego Z [g]:</strong> 
        <input type="number" step="any" id="ink_z" value="81.9768"><br><br>
        
        <strong>Pobrana kolimacja [cc]:</strong> 
        <input type="number" step="any" id="ink_kolimacja_input" value="0">
    </div>

    <table id="inklinacja_table">
        <thead>
            <tr>
                <th>Cel</th>
                <th>Odczyt I [g]</th>
                <th>Odczyt II [g]</th>
                <th>v</th>
                <th>vv</th>
                <th>Akcja</th>
            </tr>
        </thead>
        <tbody>
        </tbody>
    </table>
    
    <button class="btn" onclick="addInklinacjaRow()">+ Dodaj Cel</button>
    <button class="btn" onclick="calcInklinacja()" style="background-color: #27ae60;">Oblicz Inklinację</button>

    <div class="panel" style="margin-top: 20px;">
        <h3>Wyniki:</h3>
        <b>Inklinacja (i):</b> <span id="i_mean" style="color:red; font-weight:bold;">-</span><br>
        <b>Błąd inklinacji (mi):</b> <span id="i_error" style="color:red; font-weight:bold;">-</span>
    </div>
</div>

<div id="Atmosfera" class="tabcontent">
    <h2>Korekcja Atmosferyczna</h2>
    
    <div class="sub-tab">
      <button class="sub-tablinks active" onclick="switchSubTab(event, 'Atm_Obliczenia')">1. Obliczenia</button>
      <button class="sub-tablinks" onclick="switchSubTab(event, 'Atm_Plik')">2. Wczytaj z Pliku</button>
      <button class="sub-tablinks" onclick="switchSubTab(event, 'Atm_Wykres')" onclick="drawAtmChart()">3. Wykres Ng0</button>
      <button class="sub-tablinks" onclick="switchSubTab(event, 'Atm_Funkcje')">4. Funkcje i Łata</button>
    </div>

    <div id="Atm_Obliczenia" class="sub-tabcontent" style="display:block;">
        <div class="grid-2">
            <div class="panel">
                <h3>Parametry Środowiska</h3>
                Długość fali λ [nm]: <input type="number" id="atm_lambda" value="633"><br><br>
                Temp. sucha t [°C]: <input type="number" step="any" id="atm_t_dry" value="15"><br><br>
                Temp. mokra t' [°C] <i>(opcjonalnie)</i>: <input type="number" step="any" id="atm_t_wet" placeholder="brak = 0 wilg."><br><br>
                Ciśnienie p [hPa]: <input type="number" step="any" id="atm_p" value="1013.25"><br><br>
                Zmierzona odległość [m]: <input type="number" step="any" id="atm_d0" value="1000"><br><br>
                <button class="btn" onclick="calcAtmosfera()" style="background-color: #27ae60;">Oblicz Poprawkę</button>
            </div>
            <div class="panel">
                <h3>Wyniki</h3>
                Współczynnik Ng0: <b id="atm_res_ng0">-</b><br><br>
                Współczynnik Ng rzeczywisty: <b id="atm_res_ng">-</b><br><br>
                Różnica (ΔD): <b id="atm_res_ppm">-</b><br><br>
                Poprawka długości: <b id="atm_res_poprawka" style="color:red;">-</b><br><br>
                <b>Poprawiona długość:</b> <span id="atm_res_d_corr" style="color:blue; font-size:18px;">-</span>
            </div>
        </div>
    </div>

    <div id="Atm_Plik" class="sub-tabcontent">
        <div class="panel">
            <h3>Wczytaj dane z pliku (p, t_sucha, t_mokra)</h3>
            <input type="file" id="atm_file" accept=".txt,.csv"><br><br>
            <i>Funkcjonalność przygotowana pod import masowy. Wypełni pola w zakładce Obliczenia po podpięciu skryptu.</i>
        </div>
    </div>

    <div id="Atm_Wykres" class="sub-tabcontent">
        <div class="panel">
            <h3>Wykres dyspersji (Ng0 względem λ 400-1500 nm)</h3>
            <button class="btn" onclick="drawAtmChart()">Generuj Wykres</button>
            <canvas id="atmCanvas" width="600" height="300" style="margin-top:20px;"></canvas>
        </div>
    </div>

    <div id="Atm_Funkcje" class="sub-tabcontent">
        <div class="panel">
            <h3>Funkcje z łatą kodową</h3>
            <p>Wczytaj plik z pełnymi danymi i popraw kąty automatycznie uwzględniając kolimację, inklinację i atmosferę.</p>
            <input type="file"><br><br>
            <button class="btn">Uruchom korektę masową</button>
        </div>
    </div>
</div>

</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Wygenerowano plik: index.html")
print("Otwórz ten plik w przeglądarce, aby korzystać z nowego interfejsu.")