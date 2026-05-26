from utils.visualization import animate_search, plot_tower, compare_algorithms
from utils.search_types   import BFS, DLS, IDS
from utils.graph_handle   import build_tower, place_goal

#Grupo 05: Emmanuel Aprígio e Luan Motta

if __name__ == "__main__":

    # ── 1. Build the 3-D tower ────────────────────────────────────────────────
    FLOORS = 5
    ROWS   = 3
    COLS   = 3

    G     = build_tower(FLOORS, ROWS, COLS)
    start = (0, 0, 0)
    goal  = place_goal(G, start)

    print(f"Torre  →  {FLOORS} andares  ×  {ROWS} linhas  ×  {COLS} colunas")
    print(f"Nós: {G.number_of_nodes()}  |  Arestas: {G.number_of_edges()}")
    print(f"Start: {start}   |   Goal: {goal}\n")

    # ── 3. Run the algorithms ─────────────────────────────────────────────────
    DLS_LIMIT = 5
    IDS_LIMIT = 15

    bfs_steps = list(BFS(G, start, goal))
    dls_steps = list(DLS(G, start, goal, DLS_LIMIT))
    ids_steps = list(IDS(G, start, goal, IDS_LIMIT))

    print(f"BFS  →  {len(bfs_steps)} passos  |  encontrou: {any(s['encontrou'] for s in bfs_steps)}")
    print(f"DLS  →  {len(dls_steps)} passos  |  encontrou: {any(s['encontrou'] for s in dls_steps)}")
    print(f"IDS  →  {len(ids_steps)} passos  |  encontrou: {any(s['encontrou'] for s in ids_steps)}")

    # ── 4. Animate each algorithm ─────────────────────────────────────────────

    print("\nAnimando BFS…")
    animate_search(G, bfs_steps, goal, algo_name="BFS")

    print("Animando DLS…")
    animate_search(G, dls_steps, goal, algo_name=f"DLS  (limit={DLS_LIMIT})")

    print("Animando IDS…")
    animate_search(G, ids_steps, goal, algo_name=f"IDS  (max depth={IDS_LIMIT})")

    # ── 5. Side-by-side comparison chart ──────────────────────────────────────
    compare_algorithms(
        results={"BFS": bfs_steps, "DLS": dls_steps, "IDS": ids_steps},
        goal=goal,
        G=G,
    )


# ──────────────────────────────────────────────────────────────────────────────────────────────────