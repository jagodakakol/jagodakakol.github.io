import statistics

# Example input values
odczyt1 = [60.2702, 60.2706, 60.2710]
odczyt2 = [260.2679, 260.2688, 260.2686]

# Calculations
v = [-0.67, 1.83, -1.17]
vv = [round(x**2, 2) for x in v]

mean_v = round(statistics.mean(v), 2)
sum_vv = round(sum(vv), 2)

# Build table rows
rows = ""
for i in range(len(odczyt1)):
    rows += f"""
    <tr>
        <td>{odczyt1[i]}</td>
        <td>{odczyt2[i]}</td>
        <td>{v[i]}</td>
        <td>{vv[i]}</td>
    </tr>
    """

# Full HTML page
html = f"""
<!DOCTYPE html>
<html>
<head>
<title>Dane inklinacja</title>

<style>
body {{
    font-family: Arial;
    padding: 40px;
}}

table {{
    border-collapse: collapse;
}}

th, td {{
    border: 1px solid black;
    padding: 8px 14px;
    text-align: center;
}}

th {{
    background-color: #e6e6e6;
}}
</style>

</head>

<body>

<h1>Dane inklinacja</h1>

<table>
<tr>
<th>Odczyt I</th>
<th>Odczyt II</th>
<th>v</th>
<th>vv</th>
</tr>

{rows}

</table>

<br>

<b>Mean v:</b> {mean_v} <br>
<b>Sum vv:</b> {sum_vv}

</body>
</html>
"""

# Write file
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html generated")