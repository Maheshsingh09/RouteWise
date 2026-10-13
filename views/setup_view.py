"""First-time setup: create the initial admin."""
import streamlit as st

from storage import save_users, hash_pw


def page_setup():
    st.markdown("<div style='max-width:480px;margin:60px auto 0;'><div class='rw-card info'><h2 style='color:#7c3aed;margin-bottom:6px;'>⚙️ First-Time Setup</h2><p>No users found. Create the initial Admin account.</p></div></div>",unsafe_allow_html=True)
    with st.form("setup_form"):
        uname=st.text_input("Admin Username"); pw=st.text_input("Password (min 4)",type="password")
        pw2=st.text_input("Confirm Password",type="password"); fn=st.text_input("Full Name"); ph=st.text_input("Phone")
        if st.form_submit_button("🚀 Create Admin & Start"):
            if not uname.strip(): st.error("Username required.")
            elif len(pw)<4: st.error("Password min 4 chars.")
            elif pw!=pw2: st.error("Passwords do not match.")
            else:
                save_users([{"username":uname.strip(),"password_hash":hash_pw(pw),"role":"ADMIN","full_name":fn.strip() or uname.strip(),"phone":ph.strip(),"active":True}])
                st.success("Admin created! Please log in."); st.session_state.page="login"; st.rerun()
