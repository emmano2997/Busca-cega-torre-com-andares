import networkx as nx


# ──────────────────────────────────────────────────────────────────────────────────────────────────


def DLS(G: nx.DiGraph, start: tuple, goal: tuple, d_limit:int):
    
    '''
    DFS que limita a profundidade.

    Dado um nível de profundidade de limite, o grafo será transversado só
    até aquele nível, culminando em menor processamento e tempo do que se
    houvesse a transversão completa do grafo. 

    O DLS possui como lógica:

    ◦ Inicialização: nó root, limite = x.
        ↓    
    ◦ DFS: algoritmo que valoriza a transversão da profundidade, uso de pilha. 
        ↓
    ◦ Check de nível: se atual > x, pare de cavar e volte.
        ↓
    ◦ Se houve volta, procure em outros caminhos até encontrar.
        ↓
    ◦ Se o objetivo foi encontrado num nó de nível < x, busca teve sucesso.

    '''
    
    visitados = set()
    pilha = [(start, 0)]

    while pilha:
        node, depth = pilha.pop()
        
        if node in visitados:
            continue

        visitados.add(node)

        yield {
            'atual': node,
            'visitados': set(visitados),
            'encontrou':   node == goal,
            'iteração':   f"DLS  |  depth limit={d_limit}  |  visiting {node}",
        }
    
        if node == goal:
            return node
       
        if depth < d_limit:

            for neighbors in reversed(list(G.successors(node))):
                if neighbors not in visitados:
                    pilha.append((neighbors, depth+1))

        print(pilha)
    

def IDS():
    
    return None


# ──────────────────────────────────────────────────────────────────────────────────────────────────
