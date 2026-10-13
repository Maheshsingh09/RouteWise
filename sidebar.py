"""Sidebar navigation."""
import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.markdown("<div style='padding:8px 0 16px 0;'><div style='font-size:22px;font-weight:700;color:#f1f5f9;'>🚚 RouteWise</div><div style='font-size:10px;color:#64748b;text-transform:uppercase;letter-spacing:1px;'>Courier Delivery System</div></div>",unsafe_allow_html=True)
        st.markdown("---")
        if st.session_state.logged_in:
            u=st.session_state.user
            rc={"ADMIN":"#4f8ef7","COURIER":"#2dd4bf","CUSTOMER":"#a78bfa"}.get(u["role"],"#64748b")
            st.markdown(f"<div style='margin-bottom:16px;'><div style='font-size:13px;color:#94a3b8;'>Signed in as</div><div style='font-size:16px;font-weight:700;color:#fff;'>{u['full_name']}</div><div style='margin-top:6px;'><span style='background:{rc}22;color:{rc};border:1px solid {rc}55;padding:3px 12px;border-radius:20px;font-size:11px;font-weight:600;'>{u['role']}</span></div></div>",unsafe_allow_html=True)
            if u["role"] in ("ADMIN","COURIER"):
                if st.button("🗺️ Routing Engine",use_container_width=True): st.session_state.page="routing"; st.rerun()
            if u["role"]=="ADMIN":
                if st.button("👑 Admin Panel",use_container_width=True): st.session_state.page="admin"; st.rerun()
            if u["role"]=="COURIER":
                if st.button("📦 My Deliveries",use_container_width=True): st.session_state.page="courier"; st.rerun()
            if u["role"]=="CUSTOMER":
                if st.button("🛍️ My Orders",use_container_width=True): st.session_state.page="customer"; st.rerun()
            st.markdown("---")
            if st.button("🚪 Logout",use_container_width=True):
                st.session_state.update({"logged_in":False,"user":None,"page":"login","route_result":None,"map_html":None})
                st.rerun()
        else:
            st.markdown("<div style='color:#64748b;font-size:13px;'>Please log in to continue.</div>",unsafe_allow_html=True)
