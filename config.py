"""Project-wide constants and file paths."""
import os

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(BASE_DIR, "data")
USERS_FILE  = os.path.join(DATA_DIR, "users.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")   # single shared orders file
PLACES_FILE = os.path.join(DATA_DIR, "places.json")

os.makedirs(DATA_DIR, exist_ok=True)

TRUCK_KMH = 60.0
BIKE_KMH  = 25.0
INF       = float("inf")

PLACES_SEED = [
    {"name":"Warehouse_ClockTower","lat":30.3248,"lon":78.0429},
    {"name":"Paltan_Bazaar","lat":30.3198,"lon":78.0467},
    {"name":"Rajpur_Road","lat":30.3468,"lon":78.0524},
    {"name":"ISBT_Dehradun","lat":30.3189,"lon":78.0319},
    {"name":"Prem_Nagar","lat":30.2977,"lon":77.9962},
    {"name":"Ballupur_Chowk","lat":30.3361,"lon":77.9981},
    {"name":"Dalanwala","lat":30.3100,"lon":78.0650},
    {"name":"Niranjanpur","lat":30.3432,"lon":78.0105},
    {"name":"GMS_Road","lat":30.2748,"lon":78.0219},
    {"name":"Sahastradhara_Road","lat":30.3672,"lon":78.0812},
    {"name":"Indira_Nagar","lat":30.3553,"lon":78.0627},
    {"name":"Race_Course","lat":30.3163,"lon":77.9925},
    {"name":"Kargi_Chowk","lat":30.3481,"lon":78.0270},
    {"name":"Mothrowala","lat":30.2623,"lon":78.0054},
    {"name":"Shimla_Bypass","lat":30.3728,"lon":78.0341},
    {"name":"Kandoli","lat":30.3812,"lon":78.0751},
    {"name":"Sewla_Kalan","lat":30.2859,"lon":78.0489},
    {"name":"Jakhan","lat":30.3601,"lon":78.0903},
    {"name":"Raipur","lat":30.3944,"lon":78.0632},
    {"name":"Doiwala","lat":30.1847,"lon":78.1218},
]
