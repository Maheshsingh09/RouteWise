# Run from inside this folder:  streamlit run app.py
import streamlit as st

st.set_page_config(
    page_title="RouteWise — Courier Delivery System",
    page_icon="🚚", layout="wide", initial_sidebar_state="expanded",
)

from styles import inject_css
from storage import bootstrap
from sidebar import render_sidebar
from views.setup_view import page_setup
from views.login_view import page_login
from views.admin_view import page_admin
from views.courier_view import page_courier
from views.customer_view import page_customer
from views.routing_view import page_routing

inject_css()


def init_state():
    defaults = {"logged_in": False, "user": None, "page": "login",
                "route_result": None, "map_html": None, "congestion": 1.0}
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()
render_sidebar()

# ── ROUTER ──
if not bootstrap():
    st.session_state.page = "setup"
    st.session_state.logged_in = False
    st.session_state.user = None
elif not st.session_state.logged_in and st.session_state.page not in ("login", "setup"):
    st.session_state.page = "login"

PAGES = {
    "setup": page_setup,
    "login": page_login,
    "admin": page_admin,
    "courier": page_courier,
    "customer": page_customer,
    "routing": page_routing,
}
PAGES.get(st.session_state.page, page_login)()
