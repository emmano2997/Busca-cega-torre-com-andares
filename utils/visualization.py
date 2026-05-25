import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D   # noqa: F401  (registers the '3d' projection)
import networkx as nx


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────────────────────────────────────────────────────────


def _get_3d_pos(G: nx.DiGraph) -> dict:
    """Map every (floor, row, col) node to an (x=col, y=row, z=floor) world position."""
    return {(f, r, c): (c, r, f) for (f, r, c) in G.nodes}


def _draw_frame(ax, G, pos, step, goal, algo_name: str):
    """Redraw the tower for one animation frame."""
    ax.cla()

    visitados = step["visitados"]
    atual     = step["atual"]
    encontrou = step["encontrou"]
    label     = step["iteração"]

    xs = [pos[n][0] for n in G.nodes]
    ys = [pos[n][1] for n in G.nodes]
    zs = [pos[n][2] for n in G.nodes]

    # ── edges ──────────────────────────────────────────────────────────────────
    for u, v in G.edges():
        # Use a thicker, more visible line for the floor-transition staircase
        same_floor = (u[0] == v[0])
        ax.plot(
            [pos[u][0], pos[v][0]],
            [pos[u][1], pos[v][1]],
            [pos[u][2], pos[v][2]],
            color="gray" if same_floor else "saddlebrown",
            alpha=0.25 if same_floor else 0.55,
            linewidth=0.9 if same_floor else 2.0,
        )

    # ── nodes ──────────────────────────────────────────────────────────────────
    for node in G.nodes:
        x, y, z = pos[node]

        if node == atual and encontrou:
            color, size, marker = "lime",      250, "*"
        elif node == goal:
            color, size, marker = "crimson",   200, "D"
        elif node == atual:
            color, size, marker = "gold",      180, "o"
        elif node in visitados:
            color, size, marker = "steelblue", 80,  "o"
        else:
            color, size, marker = "#d0d0d0",   40,  "o"

        ax.scatter(x, y, z, s=size, c=color, marker=marker,
                   depthshade=True, edgecolors="black", linewidths=0.4, zorder=5)

    # ── labels on goal and current ─────────────────────────────────────────────
    gx, gy, gz = pos[goal]
    ax.text(gx, gy, gz + 0.15, "GOAL", fontsize=7, color="crimson", ha="center")

    cx, cy, cz = pos[atual]
    ax.text(cx, cy, cz + 0.15, "→", fontsize=9, color="gold", ha="center")

    # ── axes decoration ────────────────────────────────────────────────────────
    ax.set_title(f"{algo_name}\n{label}", fontsize=9, pad=6)
    ax.set_xlabel("Col",   fontsize=8)
    ax.set_ylabel("Row",   fontsize=8)
    ax.set_zlabel("Floor", fontsize=8)

    margin = 0.5
    ax.set_xlim(min(xs) - margin, max(xs) + margin)
    ax.set_ylim(min(ys) - margin, max(ys) + margin)
    ax.set_zlim(min(zs) - margin, max(zs) + margin)

    ax.tick_params(labelsize=7)


# ──────────────────────────────────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────────────────────────────────


def plot_tower(G: nx.DiGraph, title: str = "Torre com Andares"):
    """Static 3-D view of the full tower (no search colouring)."""
    pos = _get_3d_pos(G)

    fig = plt.figure(figsize=(9, 7))
    ax  = fig.add_subplot(111, projection="3d")

    for u, v in G.edges():
        same_floor = (u[0] == v[0])
        ax.plot(
            [pos[u][0], pos[v][0]],
            [pos[u][1], pos[v][1]],
            [pos[u][2], pos[v][2]],
            color="gray" if same_floor else "saddlebrown",
            alpha=0.3   if same_floor else 0.7,
            linewidth=0.8 if same_floor else 2.0,
        )

    for node in G.nodes:
        x, y, z = pos[node]
        ax.scatter(x, y, z, s=60, c="steelblue",
                   depthshade=True, edgecolors="black", linewidths=0.4, zorder=5)

    ax.set_title(title, fontsize=11)
    ax.set_xlabel("Col");  ax.set_ylabel("Row");  ax.set_zlabel("Floor")
    plt.tight_layout()
    plt.show()


def animate_search(
    G: nx.DiGraph,
    steps: list,
    goal: tuple,
    algo_name: str = "Search",
    interval: int  = 350,
    save_path: str  = None,       # e.g. "dls_search.gif"  ← optional
) -> animation.FuncAnimation:
    """
    Animate a list of search steps (as produced by the generators in search_types.py).

    Parameters
    ----------
    G          : the tower DiGraph
    steps      : list of step-dicts  {'atual', 'visitados', 'encontrou', 'iteração'}
    goal       : goal node tuple
    algo_name  : label shown on the title
    interval   : ms between frames
    save_path  : if given, saves the animation (requires ffmpeg or pillow)
    """
    if not steps:
        print("Nenhum passo para animar.")
        return None

    pos = _get_3d_pos(G)

    fig = plt.figure(figsize=(11, 8))
    ax  = fig.add_subplot(111, projection="3d")

    def update(frame):
        _draw_frame(ax, G, pos, steps[frame], goal, algo_name)

    anim = animation.FuncAnimation(
        fig, update, frames=len(steps), interval=interval, repeat=False
    )

    if save_path:
        writer = "pillow" if save_path.endswith(".gif") else "ffmpeg"
        anim.save(save_path, writer=writer, dpi=100)
        print(f"Animação salva em: {save_path}")

    plt.tight_layout()
    plt.show()
    return anim


def compare_algorithms(results: dict, goal: tuple, G: nx.DiGraph):
    """
    Bar-chart comparison of the number of steps each algorithm took.

    Parameters
    ----------
    results : { 'DLS': steps_list, 'IDS': steps_list, 'BFS': steps_list, ... }
    goal    : goal node (used in title)
    G       : tower graph (used for node count context)
    """
    names  = list(results.keys())
    counts = [len(v) for v in results.values()]
    found  = [any(s["encontrou"] for s in v) for v in results.values()]

    colors = ["steelblue" if f else "salmon" for f in found]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(names, counts, color=colors, edgecolor="black", width=0.5)

    for bar, count, ok in zip(bars, counts, found):
        label = f"{count} passos" + (" ✓" if ok else " ✗")
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.5,
            label, ha="center", va="bottom", fontsize=10,
        )

    ax.set_title(
        f"Comparação de Algoritmos  |  Goal={goal}  |  Nós={G.number_of_nodes()}",
        fontsize=11,
    )
    ax.set_ylabel("Nós visitados (passos)")
    ax.set_xlabel("Algoritmo")

    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="steelblue", edgecolor="black", label="Encontrou o objetivo"),
        Patch(facecolor="salmon",    edgecolor="black", label="Não encontrou"),
    ]
    ax.legend(handles=legend_elements, loc="upper right")

    plt.tight_layout()
    plt.show()


# ──────────────────────────────────────────────────────────────────────────────────────────────────