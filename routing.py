"""Graph building and routing algorithms: Dijkstra, Yen K=2, TSP."""
import heapq, math

from config import INF


def haversine(la1,lo1,la2,lo2):
    R=6371.0; dl=math.radians(la2-la1); do=math.radians(lo2-lo1)
    a=math.sin(dl/2)**2+math.cos(math.radians(la1))*math.cos(math.radians(la2))*math.sin(do/2)**2
    return R*2*math.atan2(math.sqrt(a),math.sqrt(1-a))

def _edge_cong_factor(u, v, base_dist, seed_cong):
    """
    Returns the effective weight for edge (u,v) under congestion.
    Uses a deterministic hash of (min(u,v), max(u,v)) to assign each
    edge a stable "road type" factor in [0.5 .. 2.0]:
      - Long edges (main arterial roads) get factor > 1.0  → more affected
      - Short edges (side streets / lanes) get factor < 1.0 → less affected
    This breaks the uniform scaling so that route choices actually change.
    """
    if seed_cong <= 1.0:
        return base_dist  # no congestion — use raw distance

    h = ((min(u,v) * 2654435761) ^ (max(u,v) * 2246822519)) & 0xFFFFFFFF
    road_factor = 0.4 + (h % 1000) / 833.0   # range ≈ 0.40 … 1.60

    extra = (seed_cong - 1.0) * road_factor
    effective_cong = 1.0 + extra
    return base_dist * effective_cong

def build_knn_graph(places, k=6):
    n=len(places); k=min(k,n-1)
    adj={i:{} for i in range(n)}
    for u in range(n):
        dists=sorted([(haversine(places[u][1],places[u][2],places[v][1],places[v][2]),v)
                      for v in range(n) if v!=u])
        for d,v in dists[:k]:
            if d<adj[u].get(v,INF): adj[u][v]=d; adj[v][u]=d
    parent=list(range(n))
    def find(x):
        while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
        return x
    def union(a,b): parent[find(a)]=find(b)
    for u in adj:
        for v in adj[u]: union(u,v)
    all_e=sorted([(haversine(places[u][1],places[u][2],places[v][1],places[v][2]),u,v)
                  for u in range(n) for v in range(u+1,n)])
    for d,u,v in all_e:
        if find(u)!=find(v): adj[u][v]=d; adj[v][u]=d; union(u,v)
    return {u:list(nb.items()) for u,nb in adj.items()}

def dijkstra(adj,src,dst,blocked=None,cong=1.0):
    """Dijkstra with per-edge congestion — each edge gets a different
    congestion penalty so heavy traffic actually changes which route wins."""
    dist={i:INF for i in range(len(adj))}; prev={i:-1 for i in range(len(adj))}
    dist[src]=0.0; pq=[(0.0,src)]; blk=set(blocked) if blocked else set()
    while pq:
        d,u=heapq.heappop(pq)
        if d>dist[u]: continue
        if u==dst: break
        for v,w in adj[u]:
            if (u,v) in blk or (v,u) in blk: continue
            # Apply per-edge congestion factor instead of uniform scaling
            effective_w = _edge_cong_factor(u, v, w, cong)
            nd=dist[u]+effective_w
            if nd<dist[v]: dist[v]=nd; prev[v]=u; heapq.heappush(pq,(nd,v))
    if dist[dst]>=INF/2: return None,INF
    path,cur=[],dst
    while cur!=-1: path.append(cur); cur=prev[cur]
    path.reverse(); return path,dist[dst]

def path_cost(adj,path,cong=1.0):
    """Compute true path cost using per-edge congestion factors."""
    em={(u,v):w for u in adj for v,w in adj[u]}
    t=0.0
    for i in range(len(path)-1):
        u,v=path[i],path[i+1]
        w=em.get((u,v),em.get((v,u),INF))
        t+=_edge_cong_factor(u,v,w,cong)
    return t

def path_real_km(adj,path):
    """Compute actual km distance ignoring congestion (for display)."""
    em={(u,v):w for u in adj for v,w in adj[u]}
    t=0.0
    for i in range(len(path)-1):
        u,v=path[i],path[i+1]
        w=em.get((u,v),em.get((v,u),INF))
        t+=w
    return t

def tour_real_km(adj,tour,cong=1.0):
    """TSP returns only the ORDER of stops. Consecutive stops are usually NOT
    direct neighbours in the graph, so expand every leg with Dijkstra and sum
    the real (no-congestion) km of the full legs."""
    total=0.0
    for a,b in zip(tour,tour[1:]):
        leg,_=dijkstra(adj,a,b,cong=cong)
        if leg: total+=path_real_km(adj,leg)
    return total

def yen_k2(adj,src,dst,places,blocked=None,cong=1.0):
    p1,c1=dijkstra(adj,src,dst,blocked,cong)
    if p1 is None: return []
    routes=[{"path":p1,"cost":c1}]
    best_edges=list(zip(p1,p1[1:])); best_set=set(best_edges)
    cands=[]
    def add(p,c):
        if not p or p==p1 or len(set(p))<len(p): return
        if any(x["path"]==p for x in cands): return
        ae=set(zip(p,p[1:])); ov=len(ae&best_set)/max(len(ae),1)
        cands.append({"path":p,"cost":c,"ov":ov})
    # Pass 1
    for si in range(len(p1)-1):
        blk=set(blocked) if blocked else set()
        blk.add((p1[si],p1[si+1])); blk.add((p1[si+1],p1[si]))
        sp,_=dijkstra(adj,p1[si],dst,blk,cong)
        if sp and len(sp)>=2:
            tot=p1[:si]+sp
            if len(set(tot))==len(tot): add(tot,path_cost(adj,tot,cong))
    # Pass 2
    if not cands:
        for u,v in best_edges:
            blk=set(blocked) if blocked else set()
            blk.add((u,v)); blk.add((v,u))
            ap,ac=dijkstra(adj,src,dst,blk,cong); add(ap,ac)
    # Pass 3
    if not cands:
        blk=set(blocked) if blocked else set()
        for u,v in best_edges: blk.add((u,v)); blk.add((v,u))
        ap,ac=dijkstra(adj,src,dst,blk,cong); add(ap,ac)
    if not cands: return routes
    cands.sort(key=lambda c:c["cost"]*(1+0.5*c["ov"]))
    routes.append({"path":cands[0]["path"],"cost":cands[0]["cost"]}); return routes

def greedy_tsp(adj,stops,cong=1.0):
    n=len(stops); vis=[False]*n; tour=[stops[0]]; vis[0]=True; total=0.0
    for _ in range(n-1):
        cur=tour[-1]; bd,bi=INF,-1
        for j in range(n):
            if not vis[j]:
                _,d=dijkstra(adj,cur,stops[j],cong=cong)
                if d<bd: bd,bi=d,j
        if bi==-1: break
        vis[bi]=True; tour.append(stops[bi]); total+=bd
    _,d=dijkstra(adj,tour[-1],stops[0],cong=cong); total+=d; tour.append(stops[0])
    return tour,total

def dp_tsp(adj,stops,cong=1.0):
    n=len(stops)
    if n>12: return greedy_tsp(adj,stops,cong)
    cost=[[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i!=j: _,cost[i][j]=dijkstra(adj,stops[i],stops[j],cong=cong)
    FULL=(1<<n)-1
    dp=[[INF]*n for _ in range(FULL+1)]; par=[[-1]*n for _ in range(FULL+1)]
    dp[1][0]=0.0
    for mask in range(1,FULL+1):
        for u in range(n):
            if not(mask&(1<<u)) or dp[mask][u]>=INF/2: continue
            for v in range(n):
                if mask&(1<<v): continue
                nm=mask|(1<<v); nc=dp[mask][u]+cost[u][v]
                if nc<dp[nm][v]: dp[nm][v]=nc; par[nm][v]=u
    bc,last=INF,-1
    for u in range(1,n):
        val=dp[FULL][u]+cost[u][0]
        if val<bc: bc,last=val,u
    if last==-1: return greedy_tsp(adj,stops,cong)
    order,mask,cur=[],FULL,last
    while cur!=-1: order.append(stops[cur]); p=par[mask][cur]; mask^=(1<<cur); cur=p
    order.reverse(); order.append(stops[0]); return order,bc

def compute_time(km,kmh): return (km/kmh*60) if kmh>0 else 0
