"""Courier panel: assigned deliveries."""
import streamlit as st

from storage import load_users, save_users, hash_pw, load_orders, save_orders, status_color


def page_courier():
    u=st.session_state.user
    st.markdown(f"<div class='logo-banner'><div class='icon'>🛵</div><div><div class='title'>Courier Panel</div><div class='sub'>{u['full_name']} · {u['phone']}</div></div></div>",unsafe_allow_html=True)

    # Courier sees ALL orders assigned to them (from shared orders file)
    all_orders=load_orders()
    my_orders=[o for o in all_orders if o.get("courier")==u["username"]]

    tab_del,tab_pw=st.tabs(["📦 My Assigned Deliveries","🔑 Change Password"])
    with tab_del:
        if not my_orders:
            st.markdown("<div class='rw-card warn'><h4>No Assigned Deliveries</h4><p>No orders have been assigned to you yet. Ask your admin to assign orders.</p></div>",unsafe_allow_html=True)
        else:
            rows="".join(
                f"<tr>"
                f"<td style='font-family:JetBrains Mono,monospace;font-weight:700;'>{o['id']}</td>"
                f"<td>{o.get('from_loc','—')}</td>"
                f"<td>{o.get('to_loc','—')}</td>"
                f"<td><span style='background:{status_color(o['status'])}22;color:{status_color(o['status'])};border:1px solid {status_color(o['status'])}55;padding:2px 8px;border-radius:20px;font-size:10px;font-weight:600;'>{o['status']}</span></td>"
                f"<td style='color:#64748b;font-size:11px;'>{o.get('customer','—')}</td>"
                f"</tr>" for o in my_orders)
            st.markdown(f"<div class='rw-card'><table class='user-table'><thead><tr><th>Order ID</th><th>Pickup</th><th>Deliver To</th><th>Status</th><th>Customer</th></tr></thead><tbody>{rows}</tbody></table></div><p style='font-size:12px;color:#475569;'>Your assigned orders: {len(my_orders)}</p>",unsafe_allow_html=True)

            st.markdown("#### Update Delivery Status")
            with st.form("update_status"):
                c1,c2=st.columns(2)
                with c1: sel=st.selectbox("Order",[o["id"] for o in my_orders])
                with c2: ns=st.selectbox("New Status",["In Transit","Delivered"])
                if st.form_submit_button("✅ Update Status"):
                    orders=load_orders()
                    for o in orders:
                        if o["id"]==sel: o["status"]=ns; break
                    save_orders(orders); st.success(f"✅ {sel} → {ns}"); st.rerun()

    with tab_pw:
        with st.form("cpw"):
            cp=st.text_input("Current Password",type="password")
            np1=st.text_input("New Password",type="password"); np2=st.text_input("Confirm",type="password")
            if st.form_submit_button("🔑 Update"):
                if hash_pw(cp)!=u["password_hash"]: st.error("Wrong current password.")
                elif len(np1)<4: st.error("Min 4 chars.")
                elif np1!=np2: st.error("Don't match.")
                else:
                    users=load_users()
                    for usr in users:
                        if usr["username"]==u["username"]: usr["password_hash"]=hash_pw(np1); break
                    save_users(users); st.session_state.user["password_hash"]=hash_pw(np1); st.success("Password updated!")

    st.markdown("---")
    if st.button("🗺️ Launch Routing Engine"): st.session_state.page="routing"; st.rerun()
