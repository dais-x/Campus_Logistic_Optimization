import pandas as pd
import pulp
import folium

# ---------------------------------------------------
# 1 LOAD DATA
# ---------------------------------------------------

warehouses = pd.read_csv("../data/warehouses.csv")
facilities = pd.read_csv("../data/facilities.csv")
demands = pd.read_csv("../data/demands.csv")
transport = pd.read_csv("../data/transportation_costs.csv")
bounds = pd.read_csv("../data/geographic_bounds.csv")



# ---------------------------------------------------
# 2 MERGE DEMAND DATA
# ---------------------------------------------------

facilities = facilities.merge(demands, on="facility_id")

facilities["annual_demand"] = facilities["daily_demand"] * 365

warehouses["annual_construction"] = warehouses["construction_cost"] / 10
warehouses["annual_operational"] = warehouses["operational_cost"] * 365

# ---------------------------------------------------
# 3 DEFINE SETS
# ---------------------------------------------------

W = warehouses["warehouse_id"].tolist()
F = facilities["facility_id"].tolist()

# dictionaries
demand = dict(zip(facilities.facility_id, facilities.annual_demand))

capacity = {
    row["warehouse_id"]: row["capacity"] * 365
    for _, row in warehouses.iterrows()
}

construction = dict(zip(warehouses.warehouse_id, warehouses.annual_construction))
operational = dict(zip(warehouses.warehouse_id, warehouses.annual_operational))

# filter transportation matrix
transport = transport[
    transport["from_warehouse"].isin(W)
]

transport = transport[
    transport["to_facility"].isin(F)
]

transport_cost = {
    (row["from_warehouse"], row["to_facility"]): row["cost_per_unit"]
    for _, row in transport.iterrows()
}

# ---------------------------------------------------
# 4 CREATE MODEL
# ---------------------------------------------------

model = pulp.LpProblem("Campus_Logistics", pulp.LpMinimize)

x = pulp.LpVariable.dicts(
    "ship",
    [(w, f) for w in W for f in F],
    lowBound=0
)

y = pulp.LpVariable.dicts(
    "open",
    W,
    cat="Binary"
)

# ---------------------------------------------------
# 5 OBJECTIVE FUNCTION
# ---------------------------------------------------

transport_term = pulp.lpSum(
    transport_cost.get((w, f), 0) * x[(w, f)]
    for w in W for f in F
)

warehouse_term = pulp.lpSum(
    (construction[w] + operational[w]) * y[w]
    for w in W
)

model += transport_term + warehouse_term

# ---------------------------------------------------
# 6 CONSTRAINTS
# ---------------------------------------------------

model += pulp.lpSum(y[w] for w in W) == 2

for f in F:
    model += pulp.lpSum(x[(w, f)] for w in W) == demand[f]

for w in W:
    model += pulp.lpSum(x[(w, f)] for f in F) <= capacity[w] * y[w]

model += transport_term + warehouse_term <= 1500000

# ---------------------------------------------------
# 7 SOLVE
# ---------------------------------------------------

model.solve()

print("Status:", pulp.LpStatus[model.status])

selected_warehouses = []
shipments = []

for w in W:
    if y[w].value() == 1:
        selected_warehouses.append(w)

for w in W:
    for f in F:
        qty = x[(w, f)].value()
        if qty is not None and qty > 0:
            shipments.append((w, f, qty))

print("Selected Warehouses:", selected_warehouses)

# ---------------------------------------------------
# 8 CREATE MAP
# ---------------------------------------------------

center_lat = bounds.loc[0, "center_lat"]
center_lon = bounds.loc[0, "center_lon"]
radius = bounds.loc[0, "radius_km"] * 1000

m = folium.Map(location=[center_lat, center_lon], zoom_start=14)

# campus boundary
folium.Circle(
    location=[center_lat, center_lon],
    radius=radius,
    color="blue",
    fill=False
).add_to(m)

# facilities
for _, row in facilities.iterrows():

    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=max(row["daily_demand"]/3, 3),
        color="blue",
        fill=True,
        popup=f"{row['facility_name']} | Demand: {row['daily_demand']}"
    ).add_to(m)

# warehouses
for _, row in warehouses.iterrows():

    color = "red" if row["warehouse_id"] in selected_warehouses else "gray"

    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        icon=folium.Icon(color=color, icon="home"),
        popup=row["warehouse_name"]
    ).add_to(m)

# routes
for w, f, qty in shipments:

    w_row = warehouses[warehouses["warehouse_id"] == w].iloc[0]
    f_row = facilities[facilities["facility_id"] == f].iloc[0]

    folium.PolyLine(
        locations=[
            [w_row["latitude"], w_row["longitude"]],
            [f_row["latitude"], f_row["longitude"]]
        ],
        weight=max(qty/20000, 2),
        color="green",
        tooltip=f"{w} → {f} : {int(qty)} units"
    ).add_to(m)

# save map
m.save("logistics_network.html")

print("Map saved as logistics_network.html")