"""Admin panel: users, orders, places."""
import streamlit as st

from storage import (load_users, save_users, hash_pw, load_orders, save_orders,
                     status_color, load_places_raw, save_places_raw)


def page_admin():
    st.markdown("<div class='logo-banner'><div class='icon'>👑</div><div><div class='title'>Admin Panel</div><div class='sub'>Full System Control</div></div></div>",unsafe_allow_html=True)
    tabs=st.tabs(["👥 Users","➕ Add User","⚙️ Manage Users","🔑 Passwords","📦 All Orders","📍 Places"])

    # ── Users ──
    with tabs[0]:
        users=load_users()
        rp={"ADMIN":"pill-admin","COURIER":"pill-courier","CUSTOMER":"pill-customer"}
        rows="".join(f"<tr><td><b>{u['username']}</b></td><td><span class='{rp.get(u['role'],'')}'>{u['role']}</span></td><td>{u['full_name']}</td><td>{u['phone']}</td><td><span class='{'pill-active' if u['active'] else 'pill-inactive'}'>{'Active' if u['active'] else 'Deactivated'}</span></td></tr>" for u in users)
        st.markdown(f"<div class='rw-card'><table class='user-table'><thead><tr><th>Username</th><th>Role</th><th>Full Name</th><th>Phone</th><th>Status</th></tr></thead><tbody>{rows}</tbody></table></div><p style='font-size:12px;color:#475569;'>Total: {len(users)} user(s)</p>",unsafe_allow_html=True)

    # ── Add User ──
    with tabs[1]:
        with st.form("add_user"):
            c1,c2=st.columns(2)
            with c1: nu=st.text_input("Username"); nr=st.selectbox("Role",["ADMIN","COURIER","CUSTOMER"]); nfn=st.text_input("Full Name")
            with c2: np=st.text_input("Password",type="password"); np2=st.text_input("Confirm",type="password"); nph=st.text_input("Phone")
            if st.form_submit_button("➕ Add User",use_container_width=True):
                users=load_users()
                if not nu.strip(): st.error("Username required.")
                elif any(u["username"]==nu.strip() for u in users): st.error("Username exists.")
                elif len(np)<4: st.error("Password min 4 chars.")
                elif np!=np2: st.error("Passwords don't match.")
                else:
                    users.append({"username":nu.strip(),"password_hash":hash_pw(np),"role":nr,"full_name":nfn.strip() or nu.strip(),"phone":nph.strip(),"active":True})
                    save_users(users); st.success(f"User '{nu}' added as {nr}!"); st.rerun()

    # ── Manage Users ──
    with tabs[2]:
        users=load_users(); unames=[u["username"] for u in users]
        st.markdown("#### Toggle Active/Deactivate")
        with st.form("toggle"):
            tu=st.selectbox("User",unames,key="tgl")
            if st.form_submit_button("Toggle Status"):
                users=load_users()
                for u in users:
                    if u["username"]==tu:
                        if u["role"]=="ADMIN" and u["active"] and sum(1 for x in users if x["role"]=="ADMIN" and x["active"])<=1:
                            st.error("Cannot deactivate sole admin."); break
                        u["active"]=not u["active"]; save_users(users)
                        st.success(f"'{tu}' is now {'ACTIVE' if u['active'] else 'DEACTIVATED'}."); st.rerun(); break
        st.markdown("---"); st.markdown("#### Delete User")
        with st.form("del_user"):
            du=st.selectbox("User to delete",unames,key="dlu"); dc=st.checkbox("Confirm delete")
            if st.form_submit_button("🗑️ Delete"):
                if not dc: st.error("Check confirmation box.")
                else:
                    users=load_users(); t=next((u for u in users if u["username"]==du),None)
                    if t and t["role"]=="ADMIN" and sum(1 for u in users if u["role"]=="ADMIN")<=1:
                        st.error("Cannot delete sole admin.")
                    else:
                        save_users([u for u in users if u["username"]!=du]); st.success(f"'{du}' deleted."); st.rerun()

    # ── Passwords ──
    with tabs[3]:
        with st.form("reset_pw"):
            ru=st.selectbox("User",[u["username"] for u in load_users()],key="rpw")
            rp1=st.text_input("New Password",type="password"); rp2=st.text_input("Confirm",type="password")
            if st.form_submit_button("🔑 Reset"):
                if len(rp1)<4: st.error("Min 4 chars.")
                elif rp1!=rp2: st.error("Don't match.")
                else:
                    users=load_users()
                    for u in users:
                        if u["username"]==ru: u["password_hash"]=hash_pw(rp1); break
                    save_users(users); st.success(f"Password reset for '{ru}'.")

    # ── ALL ORDERS (Admin sees everything + can assign couriers) ──
    with tabs[4]:
        st.markdown("### 📦 All Orders — Manage & Assign Couriers")
        orders=load_orders()
        couriers=[u["username"] for u in load_users() if u["role"]=="COURIER" and u["active"]]
        if not orders:
            st.info("No orders yet. Customers place orders from their panel.")
        else:
            sc_fn=lambda s:status_color(s)
            rows="".join(
                f"<tr>"
                f"<td style='font-family:JetBrains Mono,monospace;font-weight:700;'>{o['id']}</td>"
                f"<td>{o.get('customer','—')}</td>"
                f"<td>{o.get('from_loc','—')}</td>"
                f"<td>{o.get('to_loc','—')}</td>"
                f"<td><span style='background:{sc_fn(o['status'])}22;color:{sc_fn(o['status'])};border:1px solid {sc_fn(o['status'])}55;padding:2px 8px;border-radius:20px;font-size:10px;font-weight:600;'>{o['status']}</span></td>"
                f"<td style='color:#64748b;'>{o.get('courier','Unassigned')}</td>"
                f"</tr>"
                for o in orders)
            st.markdown(f"<div class='rw-card'><table class='user-table'><thead><tr><th>ID</th><th>Customer</th><th>From</th><th>To</th><th>Status</th><th>Courier</th></tr></thead><tbody>{rows}</tbody></table></div>",unsafe_allow_html=True)

            st.markdown("#### ✏️ Assign Courier & Update Status")
            with st.form("admin_update_order"):
                c1,c2,c3=st.columns(3)
                with c1: sel_oid=st.selectbox("Order",[o["id"] for o in orders])
                with c2: sel_status=st.selectbox("Status",["Pending","Assigned","In Transit","Delivered"])
                with c3: sel_courier=st.selectbox("Assign Courier",["Unassigned"]+couriers)
                if st.form_submit_button("✅ Update Order"):
                    orders=load_orders()
                    for o in orders:
                        if o["id"]==sel_oid:
                            o["status"]=sel_status
                            o["courier"]=sel_courier if sel_courier!="Unassigned" else o.get("courier","Unassigned")
                            break
                    save_orders(orders); st.success(f"Order {sel_oid} updated!"); st.rerun()

    # ── Places ──
    with tabs[5]:
        raw=load_places_raw()
        rows="".join(f"<tr><td style='color:#64748b;font-family:JetBrains Mono,monospace;'>{i}</td><td style='font-weight:600;'>{p['name']}</td><td style='font-family:JetBrains Mono,monospace;font-size:11px;color:#64748b;'>{p['lat']:.4f}</td><td style='font-family:JetBrains Mono,monospace;font-size:11px;color:#64748b;'>{p['lon']:.4f}</td></tr>" for i,p in enumerate(raw))
        st.markdown(f"<div class='rw-card'><table class='user-table'><thead><tr><th>#</th><th>Name</th><th>Latitude</th><th>Longitude</th></tr></thead><tbody>{rows}</tbody></table></div><p style='font-size:12px;color:#475569;'>📂 Stored in <code>data/places.json</code> · {len(raw)} locations</p>",unsafe_allow_html=True)
        with st.form("add_place"):
            p1,p2,p3=st.columns(3)
            with p1: pn=st.text_input("Location Name")
            with p2: pla=st.number_input("Latitude",value=30.3200,format="%.4f")
            with p3: plo=st.number_input("Longitude",value=78.0500,format="%.4f")
            if st.form_submit_button("➕ Add Location"):
                if not pn.strip(): st.error("Name required.")
                elif any(p["name"]==pn.strip() for p in raw): st.error("Name exists.")
                else:
                    raw.append({"name":pn.strip(),"lat":pla,"lon":plo}); save_places_raw(raw)
                    st.success(f"'{pn}' added!"); st.rerun()
        with st.form("del_place"):
            dp=st.selectbox("Remove location",[p["name"] for p in raw],key="dlp")
            if st.form_submit_button("🗑️ Remove"):
                save_places_raw([p for p in raw if p["name"]!=dp]); st.success(f"'{dp}' removed."); st.rerun()

    st.markdown("---")
    if st.button("🗺️ Go to Routing Engine"): st.session_state.page="routing"; st.rerun()
