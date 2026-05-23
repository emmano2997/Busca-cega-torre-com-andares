# Busca Cega em Espaço 3D - Torre com Andares

## (Grupo 5)
---
* Emmanuel Aprígio 
* Luan Motta

Este repositório contém a implementação de um sistema de busca em um grafo tridimensional que simula uma **Torre com Andares**, desenvolvido como atividade prática para a disciplina de **Introdução à Inteligência Artificial**.

O objetivo principal é avaliar e visualizar o comportamento de algoritmos de **Busca Cega ** navegando verticalmente entre diferentes níveis para encontrar um objetivo específico.

## 📌 Escopo do Projeto 
* **Algoritmos Focados:** * **DLS** (Depth-Limited Search / Busca em Profundidade Limitada) * **IDS** (Iterative Deepening Search / Busca Iterativa em Profundidade)
* **Objetivo:** Encontrar o caminho mais eficiente do primeiro andar (Térreo) até ao objetivo.

## 📌 Conceitos Estudados

### Busca em Profundidade Limitada (DLS)
Uma variação da Busca em Profundidade (DFS) que contorna o problema de loops infinitos ao estipular um limite máximo de profundidade $L$. Se o objetivo não for encontrado até o nível $L$, o algoritmo realiza o *backtracking*.

### Busca Iterativa em Profundidade (IDS)
Combina a eficiência de memória da DFS com a otimalidade de caminhos da BFS. O algoritmo executa a DLS repetidamente, incrementando o limite de profundidade ($L = 0, 1, 2, \dots$) a cada iteração até que a solução seja encontrada.

---

## 📌 Tecnologias Utilizadas
* **Python 3**
* **NetworkX:** Para modelagem do grafo 3D e manipulação de nós/arestas.
* **Matplotlib (mpl_toolkits.mplot3d):** Para a renderização e visualização espacial do cenário da torre.

---

## 📌 Como Executar o Projeto

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git](https://github.com/SEU-USUARIO/NOME-DO-REPOSITORIO.git)
   cd NOME-DO-REPOSITORIO
