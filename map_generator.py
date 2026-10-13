"""Builds the standalone Leaflet HTML map (embedded and downloadable)."""
from config import TRUCK_KMH, BIKE_KMH
from routing import compute_time


def generate_map_html(places,route_best,route_alt,tsp_tour,tsp_cost,cong=1.0):
    def nodes_js(arr,vn):
        if not arr: return f"var {vn}=null;\n"
        items=",".join(f'{{lat:{places[i][1]},lon:{places[i][2]},name:"{places[i][0]}"}}' for i in arr)
        return f"var {vn}=[{items}];\n"
    all_st="var allSt=["+",".join(f'{{lat:{p[1]},lon:{p[2]},name:"{p[0]}"}}' for p in places)+"];\n"
    bkm=route_best.get("real_km",route_best["cost"]) if route_best else 0
    btruck=compute_time(bkm,TRUCK_KMH); bbike=compute_time(bkm,BIKE_KMH)
    tkm=tsp_cost; ttruck=compute_time(tkm,TRUCK_KMH); tbike=compute_time(tkm,BIKE_KMH)
    cidx=route_best["path"][0] if route_best else 0
    # congestion badge html
    cong_banner=""
    if cong>1.0:
        delay_pct=int((cong-1)*100)
        cong_banner=f"""<div style='background:#fef2f2;color:#dc2626;border:1px solid #fecaca;
            padding:8px 12px;border-radius:8px;font-size:11px;margin-bottom:10px;font-weight:600;'>
            ⚠️ Traffic Congestion Active — {cong:.1f}× slower ({delay_pct}% delay)<br/>
            <span style='font-weight:400;color:#7f1d1d;'>Routes recalculated with congestion penalty applied to all edge weights.</span>
        </div>"""

    html=f"""<!doctype html><html><head><meta charset='utf-8'/>
<meta name='viewport' content='width=device-width,initial-scale=1'/>
<title>RouteWise Map</title>
<link rel='stylesheet' href='https://unpkg.com/leaflet@1.9.4/dist/leaflet.css'/>
<script src='https://unpkg.com/leaflet@1.9.4/dist/leaflet.js'></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
*{{box-sizing:border-box;margin:0;padding:0}}
html,body,#map{{height:100%;font-family:'Space Grotesk',sans-serif;}}
.panel{{position:absolute;left:12px;top:12px;z-index:9999;background:#fff;color:#1e293b;
  border-radius:14px;box-shadow:0 4px 24px rgba(0,0,0,.13);padding:16px;width:320px;
  max-height:calc(100vh - 24px);overflow-y:auto;border:1px solid #e2e8f0;}}
.logo{{display:flex;align-items:center;gap:9px;margin-bottom:14px;border-bottom:1px solid #e2e8f0;padding-bottom:12px;}}
.logo-icon{{font-size:20px;background:#dbeafe;border-radius:8px;padding:6px;}}
.logo-title{{font-size:15px;font-weight:700;color:#1e293b;}}
.logo-sub{{font-size:9px;color:#94a3b8;letter-spacing:.5px;text-transform:uppercase;margin-top:1px;}}
.hint{{font-size:10px;color:#94a3b8;margin-bottom:8px;font-style:italic;}}
.card{{background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:10px 12px;margin-bottom:7px;cursor:pointer;transition:all .2s;}}
.card:hover{{transform:translateY(-1px);box-shadow:0 2px 8px rgba(0,0,0,.08);}}
.card.best{{border-color:#2563eb;background:#eff6ff;}}
.card.best.active{{background:#2563eb;color:#fff;box-shadow:0 4px 14px rgba(37,99,235,.35);}}
.card.alt{{border-color:#ea580c;background:#fff7ed;}}
.card.alt.active{{background:#ea580c;color:#fff;box-shadow:0 4px 14px rgba(234,88,12,.35);}}
.card.tsp{{border-color:#0d9488;background:#f0fdfa;}}
.card.tsp.active{{background:#0d9488;color:#fff;box-shadow:0 4px 14px rgba(13,148,136,.35);}}
.card-hdr{{display:flex;align-items:center;justify-content:space-between;margin-bottom:5px;}}
.lbl{{font-size:9px;font-weight:700;text-transform:uppercase;letter-spacing:1px;}}
.card.best .lbl{{color:#1d4ed8;}}.card.best.active .lbl{{color:#bfdbfe;}}
.card.alt  .lbl{{color:#c2410c;}}.card.alt.active  .lbl{{color:#fed7aa;}}
.card.tsp  .lbl{{color:#0f766e;}}.card.tsp.active  .lbl{{color:#99f6e4;}}
.pill{{font-size:9px;padding:2px 7px;border-radius:10px;font-weight:600;}}
.card.best .pill{{background:#dbeafe;color:#1d4ed8;}}.card.best.active .pill{{background:#1d4ed8;color:#bfdbfe;}}
.card.alt  .pill{{background:#ffedd5;color:#c2410c;}}.card.alt.active  .pill{{background:#c2410c;color:#fed7aa;}}
.card.tsp  .pill{{background:#ccfbf1;color:#0f766e;}}.card.tsp.active  .pill{{background:#0f766e;color:#99f6e4;}}
.dist{{font-size:17px;font-weight:700;font-family:'JetBrains Mono',monospace;margin:2px 0 6px;}}
.card.best .dist{{color:#2563eb;}}.card.best.active .dist{{color:#fff;}}
.card.alt  .dist{{color:#ea580c;}}.card.alt.active  .dist{{color:#fff;}}
.card.tsp  .dist{{color:#0d9488;}}.card.tsp.active  .dist{{color:#fff;}}
.modes{{display:flex;gap:5px;margin-bottom:6px;}}
.mode{{flex:1;padding:5px 3px;background:rgba(255,255,255,.6);border:1px solid rgba(0,0,0,.07);border-radius:6px;text-align:center;}}
.card.active .mode{{background:rgba(255,255,255,.18);border-color:rgba(255,255,255,.3);}}
.mode .ico{{font-size:12px;}}.mode .num{{font-size:12px;font-weight:700;font-family:'JetBrains Mono',monospace;}}
.mode .ml{{font-size:8px;color:#64748b;margin-top:1px;}}
.card.active .mode .num,.card.active .mode .ml{{color:#fff!important;}}
.steps{{font-size:10px;line-height:1.7;font-family:'JetBrains Mono',monospace;word-break:break-word;color:#475569;}}
.card.active .steps{{color:rgba(255,255,255,.85);}}
.all-btn{{width:100%;padding:8px;background:#f1f5f9;border:1px solid #e2e8f0;border-radius:8px;
  font-size:11px;font-weight:600;color:#475569;cursor:pointer;margin-top:6px;text-align:center;transition:all .15s;}}
.all-btn:hover{{background:#e2e8f0;}}
#legend{{position:absolute;right:12px;bottom:28px;z-index:9999;background:#fff;color:#475569;
  padding:10px 14px;border-radius:10px;border:1px solid #e2e8f0;font-size:11px;box-shadow:0 2px 8px rgba(0,0,0,.1);}}
#legend div{{display:flex;align-items:center;gap:7px;margin-bottom:4px;}}
#legend span{{display:inline-block;width:24px;height:4px;border-radius:2px;}}
</style></head><body><div id='map'></div>
<div class='panel'>
  <div class='logo'><div class='logo-icon'>🚚</div>
    <div><div class='logo-title'>RouteWise</div>
    <div class='logo-sub'>Courier Delivery System</div></div></div>
  {cong_banner}
  <div class='hint'>Click a card to show that route on map</div>
"""
    if route_best:
        html+=f"""<div class='card best' id='card-r0' onclick='toggleRoute("r0")'>
  <div class='card-hdr'><span class='lbl'>Best Route</span><span class='pill'>Dijkstra</span></div>
  <div class='dist'>{bkm:.3f} km</div>
  <div class='modes'>
    <div class='mode'><div class='ico'>🚛</div><div class='num'>{btruck:.0f}</div><div class='ml'>min truck</div></div>
    <div class='mode'><div class='ico'>🏍️</div><div class='num'>{bbike:.0f}</div><div class='ml'>min bike</div></div>
  </div>
  <div class='steps'>{" &rarr; ".join(places[i][0] for i in route_best["path"])}</div>
</div>\n"""
    if route_alt:
        akm=route_alt.get("real_km",route_alt["cost"]); at=compute_time(akm,TRUCK_KMH); ab=compute_time(akm,BIKE_KMH)
        html+=f"""<div class='card alt' id='card-r1' onclick='toggleRoute("r1")'>
  <div class='card-hdr'><span class='lbl'>Alternative</span><span class='pill'>Yen K=2</span></div>
  <div class='dist'>{akm:.3f} km</div>
  <div class='modes'>
    <div class='mode'><div class='ico'>🚛</div><div class='num'>{at:.0f}</div><div class='ml'>min truck</div></div>
    <div class='mode'><div class='ico'>🏍️</div><div class='num'>{ab:.0f}</div><div class='ml'>min bike</div></div>
  </div>
  <div class='steps'>{" &rarr; ".join(places[i][0] for i in route_alt["path"])}</div>
</div>\n"""
    if tsp_tour:
        html+=f"""<div class='card tsp' id='card-tsp' onclick='toggleRoute("tsp")'>
  <div class='card-hdr'><span class='lbl'>TSP Tour</span><span class='pill'>DP/Greedy</span></div>
  <div class='dist'>{tkm:.3f} km</div>
  <div class='modes'>
    <div class='mode'><div class='ico'>🚛</div><div class='num'>{ttruck:.0f}</div><div class='ml'>min truck</div></div>
    <div class='mode'><div class='ico'>🏍️</div><div class='num'>{tbike:.0f}</div><div class='ml'>min bike</div></div>
  </div>
  <div class='steps'>{" &rarr; ".join(places[i][0] for i in tsp_tour)}</div>
</div>\n"""
    html+="""<div class='all-btn' onclick='showAll()'>Show All Routes</div>
</div>
<div id='legend'>
  <div><span style='background:#2563eb'></span> Best (Dijkstra)</div>
  <div><span style='background:#ea580c'></span> Alternative (Yen K=2)</div>
  <div><span style='background:#0d9488'></span> TSP Tour</div>
  <div><span style='background:#64748b;border-radius:50%;width:10px;height:10px;'></span> Station</div>
</div>
"""
    # ── Tiles: standard OpenStreetMap look. OSM's own server blocks file:// pages,
    # so a downloaded copy defaults to OSM France (same style) and the user can switch.
    html+=f"""<script>
var map=L.map('map').setView([{places[cidx][1]},{places[cidx][2]}],13);
var osmStd=L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png',
  {{maxZoom:19,attribution:'&copy; OpenStreetMap contributors'}});
var osmFr=L.tileLayer('https://{{s}}.tile.openstreetmap.fr/osmfr/{{z}}/{{x}}/{{y}}.png',
  {{maxZoom:20,attribution:'&copy; OpenStreetMap France | &copy; OpenStreetMap contributors'}});
var esri=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{{z}}/{{y}}/{{x}}',
  {{maxZoom:19,attribution:'Tiles &copy; Esri'}});
(location.protocol==='file:'?osmFr:osmStd).addTo(map);
L.control.layers({{'Street (OSM)':osmStd,'Street (OSM France)':osmFr,'Street (Esri)':esri}},null,{{position:'topright'}}).addTo(map);
"""
    html+=nodes_js(route_best["path"] if route_best else [],"r0")
    html+=nodes_js(route_alt["path"] if route_alt else [],"r1")
    html+=nodes_js(tsp_tour if tsp_tour else [],"tsp")
    html+=all_st
    html+=R"""
allSt.forEach(function(n){
  var ic=L.divIcon({html:'<div style="width:10px;height:10px;border-radius:50%;background:#64748b;border:2px solid #fff;box-shadow:0 1px 4px rgba(0,0,0,.3);"></div>',
    iconSize:[10,10],iconAnchor:[5,5],className:''});
  L.marker([n.lat,n.lon],{icon:ic}).addTo(map).bindPopup('<b>'+n.name+'</b>');
});
var rL={r0:null,r1:null,tsp:null},mL={r0:[],r1:[],tsp:[]},active=null;
async function osrm(a,b){
  var r=await fetch('https://router.project-osrm.org/route/v1/driving/'+a.lon+','+a.lat+';'+b.lon+','+b.lat+'?overview=full&geometries=geojson');
  if(!r.ok)throw 0; var j=await r.json();
  return j.routes[0].geometry.coordinates.map(c=>[c[1],c[0]]);
}
async function buildPoly(nodes,color,dash){
  if(!nodes||nodes.length<2)return null; var all=[];
  for(var i=0;i<nodes.length-1;i++){
    try{var seg=await osrm(nodes[i],nodes[i+1]);
      if(all.length&&seg.length&&all[all.length-1][0]===seg[0][0])seg.shift();
      all=all.concat(seg);}
    catch(e){all.push([nodes[i].lat,nodes[i].lon],[nodes[i+1].lat,nodes[i+1].lon]);}
  }
  var opt={weight:5,color:color,opacity:.95}; if(dash)opt.dashArray=dash;
  return L.polyline(all,opt);
}
function mkMark(n,col,ico){
  var s='width:28px;height:28px;border-radius:50%;background:'+col+'22;border:2.5px solid '+col+';display:flex;align-items:center;justify-content:center;font-size:13px;box-shadow:0 2px 8px '+col+'44';
  var ic=L.divIcon({html:'<div style="'+s+'">'+ico+'</div>',iconSize:[28,28],iconAnchor:[14,14],className:''});
  return L.marker([n.lat,n.lon],{icon:ic}).bindPopup('<b>'+n.name+'</b>');
}
function hideAll(){['r0','r1','tsp'].forEach(function(k){
  if(rL[k])map.removeLayer(rL[k]);
  mL[k].forEach(function(m){map.removeLayer(m);});
  var c=document.getElementById('card-'+k); if(c)c.classList.remove('active');
});}
async function showRoute(k){
  var nodes=k==='r0'?r0:k==='r1'?r1:tsp; if(!nodes)return;
  var col=k==='r0'?'#2563eb':k==='r1'?'#ea580c':'#0d9488';
  var dash=k==='r0'?null:k==='r1'?'8,5':'4,3';
  if(!rL[k])rL[k]=await buildPoly(nodes,col,dash);
  if(rL[k])rL[k].addTo(map);
  if(mL[k].length===0)nodes.forEach(function(n,i){
    var ico=k==='r0'?(i===0?'🏭':'📦'):(i===0?'🏁':String(i));
    mL[k].push(mkMark(n,col,ico));});
  mL[k].forEach(function(m){m.addTo(map);});
  var c=document.getElementById('card-'+k); if(c)c.classList.add('active');
  map.fitBounds(nodes.map(function(n){return[n.lat,n.lon];}),{padding:[40,40]});
}
async function toggleRoute(k){if(active===k){hideAll();active=null;return;}hideAll();active=k;await showRoute(k);}
async function showAll(){
  hideAll();active=null;var pts=[];
  for(var k of['r0','r1','tsp']){var nodes=k==='r0'?r0:k==='r1'?r1:tsp;if(!nodes)continue;
    await showRoute(k);nodes.forEach(function(n){pts.push([n.lat,n.lon]);});
    var c=document.getElementById('card-'+k);if(c)c.classList.add('active');}
  if(pts.length)map.fitBounds(pts,{padding:[30,30]});
}
(async function(){if(r0){await showRoute('r0');active='r0';}})();
</script></body></html>"""
    return html
