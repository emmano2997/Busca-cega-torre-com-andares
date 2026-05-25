import networkx as nx
import random


# ──────────────────────────────────────────────────────────────────────────────────────────────────


def build_tower(FLOORS:int, ROWS:int, COLS:int) -> nx.DiGraph:

    G = nx.DiGraph()

    for f in range(FLOORS):
        for r in range(ROWS):
            for c in range(COLS):

                node = (f, r, c)
                G.add_node(node, floor=f)

                if c + 1 < COLS:
                    G.add_edge(node, (f, r, c + 1))
                    G.add_edge((f, r, c + 1), node)

                if r + 1 < ROWS:
                    G.add_edge(node, (f, r + 1, c))
                    G.add_edge((f, r + 1, c), node)

        if f + 1 < FLOORS:
            G.add_edge((f, 0, 0), (f + 1, 0, 0))
            G.add_edge((f + 1, 0, 0), (f, 0, 0))

    return G


def place_goal(G: nx.DiGraph, start: tuple) -> tuple:

    candidates = [n for n in G.nodes if n != start]
    return random.choice(candidates)


def floor_layout(current_floor:int, ROWS:int, COLS:int) -> dict:

    return {(current_floor, r, c): (c, ROWS - 1 - r)
            for r in range(ROWS) for c in range(COLS)}

 
# ──────────────────────────────────────────────────────────────────────────────────────────────────
