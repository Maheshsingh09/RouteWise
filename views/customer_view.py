"""Customer panel: place and track orders."""
import streamlit as st

from storage import (load_users, save_users, hash_pw, load_orders, save_orders,
                     next_order_id, status_color, load_places)


def page_customer():
    places = load_places()
    u=st.session_state.user
    st.markdown(f"<div class='logo-banner'><div class='icon'>🛍️</div><div><div class='title'>Customer Panel</div><div class='sub'>{u['full_name']} · {u['phone']}</div></div></div>",unsafe_allow_html=True)

    tab_my,tab_place,tab_track,tab_pw=st.tabs(["📋 My Orders","📝 Place Order","🔍 Track Order","🔑 Password"])

    # Customer sees only THEIR orders from the shared file
    all_orders=load_orders()
    my_orders=[o for o in all_orders if o.get("customer")==u["username"]]

    with tab_my:
        if not my_orders:
            st.markdown("<div class='rw-card info'><h4>No Orders Yet</h4><p>You haven't placed any orders. Go to 'Place Order' tab to get started.</p></div>",unsafe_allow_html=True)
        else:
            rows="".join(
                f"<tr>"
                f"<td style='font-family:JetBrains Mono,monospace;font-weight:700;'>{o['id']}</td>"
                f"<td>{o.get('from_loc','—')}</td>"
                f"<td>{o.get('to_loc','—')}</td>"
                f"<td><span style='background:{status_color(o['status'])}22;color:{status_color(o['status'])};border:1px solid {status_color(o['status'])}55;padding:2px 8px;border-radius:20px;font-size:10px;font-weight:600;'>{o['status']}</span></td>"
                f"<td style='color:#64748b;'>{o.get('courier','Unassigned')}</td>"
                f"<td style='color:#64748b;font-size:10px;'>{o.get('created_at','—')}</td>"
                f"</tr>" for o in my_orders)
            st.markdown(f"<div class='rw-card'><table class='user-table'><thead><tr><th>ID</th><th>Pickup</th><th>Deliver To</th><th>Status</th><th>Courier</th><th>Placed</th></tr></thead><tbody>{rows}</tbody></table></div><p style='font-size:12px;color:#475569;'>Your total orders: {len(my_orders)}</p>",unsafe_allow_html=True)

    with tab_place:
        place_names=[p[0] for p in places]
        st.markdown("<div class='rw-card info'><h4>📝 New Delivery Request</h4></div>",unsafe_allow_html=True)
        with st.form("place_order"):
            c1,c2=st.columns(2)
            with c1: from_sel=st.selectbox("📍 Pickup Location",place_names)
            with c2: to_sel=st.selectbox("🏁 Delivery Location",[p for p in place_names if p!=from_sel] if len(place_names)>1 else place_names)
            notes=st.text_input("Notes (optional)",placeholder="Fragile, call before delivery...")
            if st.form_submit_button("📬 Place Order",use_container_width=True):
                if from_sel==to_sel: st.error("Pickup and delivery must be different locations.")
                else:
                    from datetime import datetime
                    orders=load_orders()
                    new_order={
                        "id": next_order_id(),
                        "customer": u["username"],
                        "from_loc": from_sel,
                        "to_loc": to_sel,
                        "notes": notes.strip(),
                        "status": "Pending",
                        "courier": "Unassigned",
                        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    }
                    orders.append(new_order); save_orders(orders)
                    st.success(f"✅ Order **{new_order['id']}** placed successfully! The admin will assign a courier soon.")
                    st.rerun()

    with tab_track:
        st.markdown("<div class='rw-card'><h4>🔍 Track Your Order</h4></div>",unsafe_allow_html=True)
        with st.form("track"):
            tid=st.text_input("Enter Order ID",placeholder="e.g. ORD-001")
            if st.form_submit_button("🔍 Track"):
                found=next((o for o in load_orders() if o["id"]==tid.strip() and o.get("customer")==u["username"]),None)
                if found:
                    sc=status_color(found["status"])
                    # Status pipeline visualization
                    statuses=["Pending","Assigned","In Transit","Delivered"]
                    cur_idx=statuses.index(found["status"]) if found["status"] in statuses else 0
                    steps_html=""
                    for si,s in enumerate(statuses):
                        if si<cur_idx: col="#22c55e"; icon="✅"
                        elif si==cur_idx: col=sc; icon="🔵"
                        else: col="#e2e8f0"; icon="⚪"
                        steps_html+=f"<div style='display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid #f1f5f9;'><span style='font-size:16px;'>{icon}</span><span style='font-weight:600;color:{col};'>{s}</span></div>"
                    st.markdown(f"""
                    <div class='rw-card info'>
                      <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:12px;'>
                        <div><div style='color:#64748b;font-size:10px;text-transform:uppercase;font-weight:600;'>Order ID</div><div style='color:#1e293b;font-weight:700;font-family:JetBrains Mono,monospace;font-size:16px;'>{found['id']}</div></div>
                        <div><div style='color:#64748b;font-size:10px;text-transform:uppercase;font-weight:600;'>Status</div><span style='background:{sc}22;color:{sc};border:1px solid {sc}55;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:600;'>{found['status']}</span></div>
                        <div><div style='color:#64748b;font-size:10px;text-transform:uppercase;font-weight:600;'>Pickup</div><div style='color:#1e293b;'>{found.get('from_loc','—')}</div></div>
                        <div><div style='color:#64748b;font-size:10px;text-transform:uppercase;font-weight:600;'>Deliver To</div><div style='color:#1e293b;'>{found.get('to_loc','—')}</div></div>
                        <div><div style='color:#64748b;font-size:10px;text-transform:uppercase;font-weight:600;'>Courier</div><div style='color:#1e293b;font-weight:600;'>{found.get('courier','Unassigned')}</div></div>
                        <div><div style='color:#64748b;font-size:10px;text-transform:uppercase;font-weight:600;'>Placed</div><div style='color:#64748b;font-size:12px;'>{found.get('created_at','—')}</div></div>
                      </div>
                      <div style='color:#64748b;font-size:10px;text-transform:uppercase;font-weight:600;margin-bottom:6px;'>Delivery Progress</div>
                      {steps_html}
                    </div>""",unsafe_allow_html=True)
                else:
                    st.error("Order not found or doesn't belong to your account.")

    with tab_pw:
        with st.form("cust_pw"):
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
