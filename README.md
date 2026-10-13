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
