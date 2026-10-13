"""Login page."""
import streamlit as st

from storage import do_login


def page_login():
    st.markdown("<div style='max-width:420px;margin:50px auto 0;text-align:center;margin-bottom:28px;'><div style='font-size:48px;'>🚚</div><h1 style='font-size:26px;font-weight:700;color:#1e293b;margin:8px 0 4px;'>RouteWise</h1><div style='font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:1px;'>Courier Delivery System</div></div>",unsafe_allow_html=True)
    c1,c2,c3=st.columns([1,2,1])
    with c2:
        with st.form("login_form"):
            uname=st.text_input("Username",placeholder="Enter username"); pw=st.text_input("Password",type="password",placeholder="Enter password")
            if st.form_submit_button("Sign In →",use_container_width=True):
                u,err=do_login(uname,pw)
                if u:
                    st.session_state.logged_in=True; st.session_state.user=u
                    st.session_state.page={"ADMIN":"admin","COURIER":"courier","CUSTOMER":"customer"}.get(u["role"],"login")
                    st.rerun()
                else: st.error(err)
