"""JSON-file persistence: places, users, orders, auth helpers."""
import hashlib, json, os

from config import USERS_FILE, ORDERS_FILE, PLACES_FILE, PLACES_SEED


def _seed_places():
    """Write PLACES_SEED to places.json ONLY if file doesn't exist."""
    if not os.path.exists(PLACES_FILE):
        with open(PLACES_FILE,"w") as f:
            json.dump(PLACES_SEED, f, indent=2)

def load_places_raw():
    _seed_places()
    with open(PLACES_FILE) as f: return json.load(f)

def save_places_raw(raw):
    with open(PLACES_FILE,"w") as f: json.dump(raw, f, indent=2)

def load_places():
    return [(p["name"],p["lat"],p["lon"]) for p in load_places_raw()]

def hash_pw(pw): return hashlib.sha256(pw.encode()).hexdigest()

def load_users():
    if not os.path.exists(USERS_FILE): return []
    with open(USERS_FILE) as f: return json.load(f)

def save_users(u):
    with open(USERS_FILE,"w") as f: json.dump(u, f, indent=2)

def find_user(uname):
    return next((u for u in load_users() if u["username"]==uname), None)

def bootstrap():
    return os.path.exists(USERS_FILE) and bool(load_users())

def do_login(uname, pw):
    u = find_user(uname)
    if u and u["password_hash"]==hash_pw(pw):
        if not u["active"]: return None,"Account deactivated."
        return u, None
    return None,"Invalid username or password."

def load_orders():
    if not os.path.exists(ORDERS_FILE): return []
    with open(ORDERS_FILE) as f: return json.load(f)

def save_orders(orders):
    with open(ORDERS_FILE,"w") as f: json.dump(orders, f, indent=2)

def next_order_id():
    orders = load_orders()
    if not orders: return "ORD-001"
    nums = []
    for o in orders:
        try: nums.append(int(o["id"].split("-")[1]))
        except: pass
    return f"ORD-{(max(nums)+1):03d}" if nums else "ORD-001"

def status_color(s):
    return {"Pending":"#f59e0b","Assigned":"#6366f1",
            "In Transit":"#2563eb","Delivered":"#22c55e"}.get(s,"#64748b")
