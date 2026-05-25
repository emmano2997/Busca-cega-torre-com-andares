import networkx as nx
from collections import deque

def BFS(G: nx.DiGraph, start: tuple, goal: tuple):
    """
    Busca em Largura (Breadth-First Search).

    Explora os nós camada por camada a partir do nó inicial.
    Garante o menor número de arestas até o objetivo (caminho ótimo em grafos
    sem peso). Usa uma fila (FIFO) como estrutura auxiliar.

    ◦ Inicialização: fila com o nó raiz.
        ↓
    ◦ Expande o primeiro da fila; enfileira seus vizinhos não visitados.
        ↓
    ◦ Repete até encontrar o objetivo ou esvaziar a fila.
    """

    visitados = set()
    fila      = deque([start])
    visitados.add(start)

    while fila:
        node = fila.popleft()

        yield {
            "atual":    node,
            "visitados": set(visitados),
            "encontrou": node == goal,
            "iteração":  f"BFS  |  visiting {node}",
        }

        if node == goal:
            return

        for neighbor in G.successors(node):
            if neighbor not in visitados:
                visitados.add(neighbor)
                fila.append(neighbor)


# ──────────────────────────────────────────────────────────────────────────────────────────────────


def DLS(G: nx.DiGraph, start: tuple, goal: tuple, d_limit: int):
    """
    Busca em Profundidade com Limite (Depth-Limited Search).

    Executa uma DFS, mas para de aprofundar quando atinge o limite d_limit.
    Útil para evitar loops infinitos e controlar o espaço de busca.

    ◦ Inicialização: nó root, limite = d_limit.
        ↓
    ◦ DFS: usa pilha (LIFO); prioriza profundidade.
        ↓
    ◦ Check de nível: se depth atual ≥ d_limit, para de expandir.
        ↓
    ◦ Volta (backtrack) e busca outros caminhos.
        ↓
    ◦ Sucesso quando encontra o objetivo num nível ≤ d_limit.
    """

    visitados = set()
    pilha     = [(start, 0)]      # (nó, profundidade)

    while pilha:
        node, depth = pilha.pop()

        if node in visitados:
            continue

        visitados.add(node)

        yield {
            "atual":    node,
            "visitados": set(visitados),
            "encontrou": node == goal,
            "iteração":  f"DLS  |  depth limit={d_limit}  |  depth={depth}  |  visiting {node}",
        }

        if node == goal:
            return

        if depth < d_limit:
            for neighbor in reversed(list(G.successors(node))):
                if neighbor not in visitados:
                    pilha.append((neighbor, depth + 1))


# ──────────────────────────────────────────────────────────────────────────────────────────────────


def IDS(G: nx.DiGraph, start: tuple, goal: tuple, max_depth: int):
    """
    Busca em Profundidade Iterativa (Iterative Deepening Search).

    Combina a completude/optimalidade da BFS com a eficiência de memória da DFS.
    Repete DLS com limites crescentes (0, 1, 2, …, max_depth) até encontrar
    o objetivo.

    ◦ Para cada limite L de 0 até max_depth:
        ↓
    ◦     Executa DLS(G, start, goal, L)
        ↓
    ◦     Se encontrou → termina.
        ↓
    ◦     Se não → aumenta L e recomeça do nó inicial.

    Custo: O(b^d)  |  Memória: O(b·d)  —  ideal para grafos grandes.
    """

    for depth_limit in range(max_depth + 1):
        for step in DLS(G, start, goal, depth_limit):

            # Relabel the step so the viewer knows which IDS iteration we are in
            step["iteração"] = (
                f"IDS  |  depth limit={depth_limit}/{max_depth}  |  "
                f"visiting {step['atual']}"
            )

            yield step

            if step["encontrou"]:
                return          # stop once the goal is found
