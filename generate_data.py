import json
import statistics

# Input values (these can change)
odczyt1 = [60.2702, 60.2706, 60.2710]
odczyt2 = [260.2679, 260.2688, 260.2686]

# Example calculations
differences = [o1 - o2 for o1, o2 in zip(odczyt1, odczyt2)]

v = [-0.67, 1.83, -1.17]
vv = [x**2 for x in v]

mean_v = statistics.mean(v)
sum_vv = sum(vv)

data = {
    "odczyt1": odczyt1,
    "odczyt2": odczyt2,
    "v": v,
    "vv": vv,
    "mean_v": round(mean_v, 2),
    "sum_vv": round(sum_vv, 2)
}

# save JSON
with open("data.json", "w") as f:
    json.dump(data, f, indent=4)

print("data.json generated")