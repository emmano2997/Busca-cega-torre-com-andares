from utils.visualization import *
from utils.search_types import *
from utils.graph_handle import *

# ──────────────────────────────────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    
    FLOORS = 5
    ROWS = 5
    COLS = 2

    G = build_tower(FLOORS, ROWS, COLS)
    start = (0,0,0)
    goal = place_goal(G, start)

    print(f"Start: {start}  |  Goal: {goal}")

    dls_steps = list(DLS(G, start, goal, 5))
    print(f"DLS steps: {len(dls_steps)}")
    #anim = animate_search(G, dls_steps, goal, algo_name="DLS")

    '''
    ids_steps = list(IDS(G, start, goal, 15))
    print(f"IDS steps: {len(ids_steps)}")
    #anim = animate_search(G, ids_steps, goal, algo_name="IDS")
    '''


# ──────────────────────────────────────────────────────────────────────────────────────────────────
