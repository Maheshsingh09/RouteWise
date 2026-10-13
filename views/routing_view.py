"""Routing engine page: Dijkstra, Yen K=2, TSP, traffic simulation, map."""
import streamlit as st

from config import TRUCK_KMH, BIKE_KMH
from storage import load_places
from routing import (haversine, build_knn_graph, yen_k2, dp_tsp, greedy_tsp,
                     path_real_km, tour_real_km, compute_time)
from map_generator import generate_map_html


def page_routing():
    places = load_places()
    st.markdown("<div class='logo-banner'><div class='icon'>🗺️</div><div><div class='title'>RouteWise Routing Engine</div><div class='sub'>Dijkstra · Yen K=2 · TSP · Traffic Simulation</div></div></div>",unsafe_allow_html=True)
    place_names=[p[0] for p in places]
    col_left,col_right=st.columns([1,2])

    with col_left:
        st.markdown("<div class='rw-card'><h4>🔧 Route Configuration</h4>",unsafe_allow_html=True)
        src_name=st.selectbox("📍 Source (Warehouse / Pickup)",place_names,index=0)
        dst_name=st.selectbox("🏁 Destination",place_names,index=1)
        src=place_names.index(src_name); dst=place_names.index(dst_name)
        st.markdown("**Extra TSP Stops** (multi-delivery tour)")
        extra_names=st.multiselect("Select additional stops",[p for p in place_names if p not in (src_name,dst_name)],max_selections=6)
        extra_stops=[place_names.index(n) for n in extra_names]
        st.markdown("</div>",unsafe_allow_html=True)

        # ── TRAFFIC SIMULATION ──
        st.markdown("""
        <div class='rw-card danger'>
          <h4>🚦 Traffic Simulation</h4>
          <p style='font-size:11px;color:#64748b;margin-bottom:8px;'>
            Congestion multiplier applies to ALL edge weights in Dijkstra, Yen K=2, and TSP.
            Higher value = heavier traffic = routes avoid congested shorter roads.
          </p>
        </div>""",unsafe_allow_html=True)
        cong=st.slider("Congestion Multiplier",1.0,3.0,1.0,0.1,
                       help="1.0=normal  1.5=moderate  2.0=heavy  3.0=gridlock")
        st.session_state.congestion=cong
        if cong==1.0:
            st.markdown("<div style='background:#f0fdf4;border:1px solid #86efac;border-radius:8px;padding:8px 12px;font-size:12px;color:#15803d;'>🟢 Normal traffic — no delay</div>",unsafe_allow_html=True)
        elif cong<1.5:
            st.markdown(f"<div style='background:#fffbeb;border:1px solid #fcd34d;border-radius:8px;padding:8px 12px;font-size:12px;color:#92400e;'>🟡 Light congestion — {int((cong-1)*100)}% slower</div>",unsafe_allow_html=True)
        elif cong<2.0:
            st.markdown(f"<div style='background:#fff7ed;border:1px solid #fb923c;border-radius:8px;padding:8px 12px;font-size:12px;color:#c2410c;'>🟠 Moderate congestion — {int((cong-1)*100)}% slower</div>",unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='background:#fef2f2;border:1px solid #f87171;border-radius:8px;padding:8px 12px;font-size:12px;color:#b91c1c;'>🔴 Heavy congestion — {int((cong-1)*100)}% slower — routes will change!</div>",unsafe_allow_html=True)

        run_btn=st.button("🚀 Run RouteWise",use_container_width=True)

    with col_right:
        if run_btn:
            if src==dst:
                st.error("Source and destination must be different.")
            else:
                with st.spinner("Computing routes with congestion factor..."):
                    adj_local=build_knn_graph(places,k=6)
                    # All algorithms receive the SAME congestion value
                    routes=yen_k2(adj_local,src,dst,places,cong=cong)
                    tsp_stops=list(dict.fromkeys([src,dst]+extra_stops))
                    tsp_n=len(tsp_stops)
                    if tsp_n<=12: tsp_tour,tsp_cost=dp_tsp(adj_local,tsp_stops,cong)
                    else: tsp_tour,tsp_cost=greedy_tsp(adj_local,tsp_stops,cong)
                    # Compute real km (no congestion) for display — congestion cost used for routing only
                    for r in routes:
                        r["real_km"] = path_real_km(adj_local, r["path"])
                    tsp_real_km = tour_real_km(adj_local, tsp_tour, cong) if tsp_tour else 0
                    st.session_state.route_result={"routes":routes,"tsp_tour":tsp_tour,"tsp_cost":tsp_cost,"tsp_real_km":tsp_real_km,"tsp_n":tsp_n,"congestion":cong}
                    r_best=routes[0] if routes else None
                    r_alt=routes[1] if len(routes)>1 else None
                    st.session_state.map_html=generate_map_html(places,r_best,r_alt,tsp_tour,tsp_real_km,cong)

        res=st.session_state.route_result
        if res:
            routes=res["routes"]; tsp_tour=res["tsp_tour"]; tsp_cost=res["tsp_cost"]; cong_used=res["congestion"]

            # Congestion notice at top
            if cong_used>1.0:
                delay=int((cong_used-1)*100)
                # Check if path actually changed vs normal
                normal_routes=yen_k2(build_knn_graph(places,k=6),src,dst,places,cong=1.0)
                path_changed = (normal_routes and routes and
                               normal_routes[0]["path"] != routes[0]["path"])
                change_msg = ("✅ Route path changed from normal traffic — congestion is routing you around busy roads."
                              if path_changed else
                              "ℹ️ Same path as normal traffic — try higher congestion (≥1.8×) to see route changes.")
                st.markdown(f"""<div class='rw-card danger'>
                  <h4>🚦 Traffic Congestion Active — {cong_used:.1f}× multiplier ({delay}% delay)</h4>
                  <p style='font-size:12px;color:#64748b;margin-bottom:6px;'>
                    Each road gets a <b>different</b> congestion penalty based on road type.
                    Heavy arterial roads slow down more; side streets stay relatively free.
                    Dijkstra avoids roads with high per-edge congestion cost.
                  </p>
                  <div style='font-size:11px;color:{"#15803d" if path_changed else "#92400e"};
                    background:{"#f0fdf4" if path_changed else "#fffbeb"};
                    border:1px solid {"#86efac" if path_changed else "#fcd34d"};
                    border-radius:6px;padding:6px 10px;'>
                    {change_msg}
                  </div>
                </div>""",unsafe_allow_html=True)

            if routes:
                bkm=routes[0].get("real_km", routes[0]["cost"])
                m1,m2,m3,m4=st.columns(4)
                m1.metric("📍 Distance",f"{bkm:.2f} km")
                m2.metric("🚛 Truck",f"{compute_time(bkm,TRUCK_KMH):.0f} min")
                m3.metric("🏍️ Bike",f"{compute_time(bkm,BIKE_KMH):.0f} min")
                m4.metric("🚦 Congestion",f"{cong_used:.1f}×")

                r=routes[0]; path_str=" ➜ ".join(places[i][0] for i in r["path"])
                real_bkm=r.get("real_km", r["cost"])
                segs=[(places[r["path"][j]][0],places[r["path"][j+1]][0],haversine(places[r["path"][j]][1],places[r["path"][j]][2],places[r["path"][j+1]][1],places[r["path"][j+1]][2])) for j in range(len(r["path"])-1)]
                seg_rows="".join(f"<tr><td>{a}</td><td>→</td><td>{b}</td><td style='color:#2563eb;font-weight:600;'>{d:.3f} km</td></tr>" for a,b,d in segs)
                cong_note=f"<div style='font-size:10px;color:#dc2626;margin-top:4px;'>⚠️ Routed avoiding high-congestion roads ({cong_used:.1f}× traffic)</div>" if cong_used>1.0 else ""
                st.markdown(f"""<div class='rw-card best'>
                  <h4>🏆 Best Route <span class='badge badge-blue'>Dijkstra</span></h4>
                  <div class='dist-badge blue'>{real_bkm:.3f} km</div>
                  {cong_note}
                  <div class='route-arrow'>{path_str}</div>
                  <details style='margin-top:10px;'><summary style='color:#64748b;font-size:11px;cursor:pointer;'>Segment Breakdown</summary>
                  <table class='seg-table' style='margin-top:8px;'><tr><th>From</th><th></th><th>To</th><th>Dist (km)</th></tr>{seg_rows}</table></details>
                </div>""",unsafe_allow_html=True)

            if len(routes)>1:
                r2=routes[1]; path_str2=" ➜ ".join(places[i][0] for i in r2["path"])
                real_akm=r2.get("real_km", r2["cost"])
                st.markdown(f"""<div class='rw-card alt'>
                  <h4>🔀 Alternative Route <span class='badge badge-orange'>Yen K=2</span></h4>
                  <div class='dist-badge orange'>{real_akm:.3f} km</div>
                  <div class='route-arrow' style='color:#ea580c;'>{path_str2}</div>
                  <div style='color:#64748b;font-size:11px;margin-top:6px;'>
                    🚛 {compute_time(real_akm,TRUCK_KMH):.0f} min truck &nbsp;·&nbsp; 🏍️ {compute_time(real_akm,BIKE_KMH):.0f} min bike
                  </div>
                </div>""",unsafe_allow_html=True)

            if tsp_tour:
                algo="DP (Held-Karp)" if res["tsp_n"]<=12 else "Greedy Nearest-Neighbour"
                tsp_str=" ➜ ".join(places[i][0] for i in tsp_tour)
                tsp_rkm=res.get("tsp_real_km", tsp_cost)
                st.markdown(f"""<div class='rw-card tsp'>
                  <h4>🔄 Multi-Stop TSP Tour <span class='badge badge-teal'>{algo}</span></h4>
                  <div class='dist-badge teal'>{tsp_rkm:.3f} km</div>
                  <div class='route-arrow' style='color:#0d9488;font-size:11px;'>{tsp_str}</div>
                  <div style='color:#64748b;font-size:11px;margin-top:6px;'>
                    🚛 {compute_time(tsp_rkm,TRUCK_KMH):.0f} min truck &nbsp;·&nbsp; 🏍️ {compute_time(tsp_rkm,BIKE_KMH):.0f} min bike
                  </div>
                </div>""",unsafe_allow_html=True)

            if st.session_state.map_html:
                st.markdown("---")
                st.markdown("### 🗺️ Interactive Map")
                st.markdown("<div class='rw-card info'><div style='font-size:12px;color:#64748b;'>📡 Road-snapped via OSRM · Click a card to toggle that route · Grey dots = all delivery stations</div></div>",unsafe_allow_html=True)
                if hasattr(st, "iframe"):          # newer Streamlit
                    st.iframe(st.session_state.map_html, height=560)
                else:                              # older Streamlit
                    st.components.v1.html(st.session_state.map_html, height=560, scrolling=False)
                st.download_button("⬇️ Download Map (HTML)",data=st.session_state.map_html,file_name="routewise_map.html",mime="text/html")
        else:
            st.markdown("<div class='rw-card' style='text-align:center;padding:48px 24px;'><div style='font-size:48px;margin-bottom:12px;'>🗺️</div><div style='font-size:16px;font-weight:600;color:#0f172a;'>Ready to Route</div><div style='color:#64748b;font-size:13px;margin-top:6px;'>Select locations and click <b style='color:#2563eb;'>Run RouteWise</b>.</div></div>",unsafe_allow_html=True)

        with st.expander("📍 All Delivery Points"):
            rows="".join(f"<tr><td style='color:#64748b;font-family:JetBrains Mono,monospace;'>{i}</td><td style='color:#1e293b;'>{p[0]}</td><td style='color:#64748b;font-family:JetBrains Mono,monospace;font-size:11px;'>{p[1]:.4f}, {p[2]:.4f}</td></tr>" for i,p in enumerate(places))
            st.markdown(f"<div class='rw-card'><table class='user-table'><thead><tr><th>#</th><th>Name</th><th>Lat, Lon</th></tr></thead><tbody>{rows}</tbody></table></div>",unsafe_allow_html=True)
