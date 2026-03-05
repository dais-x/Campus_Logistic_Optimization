# Campus City Logistics Optimization

## Overview
This project designs an **optimal supply distribution network** for essential resources across campus facilities. The objective is to determine the **best warehouse locations and shipment plan** that minimizes total annual logistics cost while satisfying facility demand, warehouse capacity limits, and financial constraints.

The solution uses **Mixed Integer Linear Programming (MILP)** implemented in Python.

---

# Problem Statement

Campus City Logistics currently operates with an inefficient distribution system. The goal of this project is to design an optimized logistics network that determines:

- Which warehouses should be opened
- How supplies should be distributed to facilities
- How to minimize the total operational cost

The optimization must ensure:

- All facility demands are satisfied
- Warehouse capacity limits are respected
- The system operates within the allocated budget
- Exactly two warehouses are selected for redundancy

---

# Project Structure
```
project-root
│
├── data
│ ├── demands.csv
│ ├── facilities.csv
│ ├── geographic_bounds.csv
│ ├── transportation_costs.csv
│ └── warehouses.csv
│
├── src
│ ├── micro.py
│ └── logistics_network.html
│
└── README.md
```

---

# Data Description

## Facilities

Facilities represent locations on campus that require supplies.

| Column | Description |
|------|-------------|
| facility_id | Unique facility identifier |
| facility_name | Name of the facility |
| type | Facility category |
| latitude | Geographic latitude |
| longitude | Geographic longitude |

---

## Demand Data

| Column | Description |
|------|-------------|
| facility_id | Facility identifier |
| daily_demand | Units required per day |

Annual demand is calculated as:
```
annual_demand = daily_demand × 365
```
---

## Warehouses

| Column | Description |
|------|-------------|
| warehouse_id | Unique warehouse identifier |
| warehouse_name | Warehouse name |
| capacity | Maximum units per day |
| construction_cost | Warehouse construction cost |
| operational_cost | Cost per day to operate |
| latitude | Warehouse latitude |
| longitude | Warehouse longitude |

---

## Transportation Costs

| Column | Description |
|------|-------------|
| from_warehouse | Source warehouse |
| to_facility | Destination facility |
| cost_per_unit | Transportation cost per unit |

---

## Geographic Boundary

| Column | Description |
|------|-------------|
| center_lat | Campus center latitude |
| center_lon | Campus center longitude |
| radius_km | Campus service radius |

---

# Optimization Model

## Decision Variables

### Warehouse Selection

Binary variable indicating whether a warehouse is opened.
```
y_w = 1 if warehouse w is selected
y_w = 0 otherwise
```
---

### Shipment Quantity

Amount shipped from warehouse to facility.
```
x_wf = units shipped from warehouse w to facility f
```

---

# Objective Function

Minimize total annual logistics cost:
Minimize:

Transportation Cost

- Warehouse Construction Cost

- Warehouse Operational Cost


---

# Constraints

## Warehouse Selection

Exactly two warehouses must be selected.
```
Σ y_w = 2
```
---

## Demand Satisfaction

Each facility must receive its annual demand.
```
Σ x_wf = demand_f × 365
```
---

## Warehouse Capacity

Shipment from each warehouse must not exceed its annual capacity.
```
Σ x_wf ≤ capacity_w × 365
```
---

## Budget Constraint

Total annual logistics cost must not exceed the allocated budget.
```
Total Cost ≤ $1,500,000
```
---

## Non-Negativity

All shipment quantities must be non-negative.
```
x_wf ≥ 0
```
---

# Technologies Used

| Technology | Purpose |
|-----------|---------|
| Python | Programming language |
| PuLP | Linear programming solver |
| Pandas | Data processing |
| Folium | Interactive geographic visualization |

---

# Visualization

The project generates an **interactive logistics network map** showing:

- Facility locations
- Warehouse locations
- Shipment routes
- Demand-based facility markers
- Warehouse coverage areas
- Interactive map controls

The final map is exported as:
```
src/logistics_network.html
```
Open this file in any browser to explore the optimized supply network.

---

# Installation

Install required Python libraries:
pip install pandas pulp folium

---

# Running the Project

1. Navigate to the project directory.

2. Run the optimization script:
cd src
python micro.py

3. After execution, the script will generate the interactive map:
logistics_network.html

---

# Output

### Console Output

The program prints:

- Optimization status
- Selected warehouses
- Shipment quantities
- Total annual cost

---

### Interactive Map

The generated map allows users to:

- View facility demand levels
- Visualize optimized shipment routes
- Toggle map layers
- Inspect shipment quantities interactively

---

# Learning Outcomes

This project demonstrates key concepts including:

- Mixed Integer Linear Programming (MILP)
- Supply chain network optimization
- Geographic logistics modeling
- Data-driven decision making
- Interactive visualization for logistics systems

---

