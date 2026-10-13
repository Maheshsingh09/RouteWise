# RouteWise — Courier Delivery System

## Run
```
pip install -r requirements.txt
cd routewise
streamlit run app.py
```
First launch shows a setup page to create the admin account.
Data (users, orders, places) is stored as JSON in `data/`.

## Structure
| File | Purpose |
|---|---|
| `app.py` | Entry point, page config, state, page router |
| `config.py` | Paths, speeds, seed places |
| `styles.py` | Global CSS |
| `storage.py` | JSON persistence + auth helpers |
| `routing.py` | Graph, Dijkstra, Yen K=2, TSP |
| `map_generator.py` | Leaflet HTML map |
| `sidebar.py` | Sidebar navigation |
| `views/` | One file per page (setup, login, admin, courier, customer, routing) |

Note: the folder is named `views/` (not `pages/`) on purpose, because Streamlit
auto-creates navigation for a folder called `pages/`.
=======
# 🚚 RouteWise
Courier routing and tracking system

RouteWise is a Python-based courier routing and tracking system designed to simplify delivery management. It helps manage courier assignments, track delivery status, and find efficient routes using graph algorithms.

## 📌 About the Project

RouteWise aims to make courier delivery faster and more organized through route optimization and delivery tracking.

The system provides separate functionalities for administrators, couriers, and customers. It uses routing algorithms to find suitable paths and support efficient delivery planning.

## ✨ Key Features

- **Admin Management:** Manage courier and delivery information.
- **Courier Assignment:** Assign deliveries to couriers.
- **Parcel Tracking:** Track delivery status.
- **Route Optimization:** Find efficient delivery routes.
- **Shortest Path:** Calculate routes using Dijkstra's algorithm.
- **Alternative Routes:** Find alternative paths using Yen's K-Shortest Paths algorithm.
- **Multi-Stop Routing:** Support route planning for multiple delivery stops.
- **Interactive Maps:** Display routes using map integration.

## 🛠️ Tech Stack

- **Programming Language:** Python
- **Frontend and Application Framework:** Streamlit
- **Routing Engine:** OSRM
- **Map Visualization:** Leaflet
- **Core Concepts:** Graph Algorithms and Route Optimization

## 🧠 Algorithms Used

| Algorithm | Purpose |
|---|---|
| Dijkstra's Algorithm | Finds the shortest path |
| Yen's K-Shortest Paths | Finds alternative routes |
| K-Nearest Neighbors (KNN) | Identifies nearby candidates |
| Union-Find | Manages connectivity |
| Traveling Salesperson Problem (TSP) | Supports multi-stop route optimization |

## ⚙️ Installation and Setup

### Prerequisites

- Python installed on your system
- Git installed on your system

### 1. Clone the Repository

Replace Maheshsingh09 with your GitHub username.

```bash
git clone https://github.com/Maheshsingh09/RouteWise
cd RouteWise
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Application

```bash
streamlit run app.py
```

The application should open in your browser.

## 📦 Delivery Status

The system supports the following delivery statuses:

- Pending
- Assigned
- In Transit
- Delivered

## 👥 Team

**Team Name:** Avengers

- Madhvan Sharma
- Mahesh Singh
- Shravan Bali

## 🎯 Project Objective

The objective of RouteWise is to improve courier delivery management by combining route optimization, parcel tracking, and efficient courier assignment in one application.

## 🚀 Future Scope

- Improved route optimization
- Delivery analytics and reports
- Enhanced user interface
- More efficient multi-stop delivery planning

---

**RouteWise — Optimized Routes, Better Deliveries.**
