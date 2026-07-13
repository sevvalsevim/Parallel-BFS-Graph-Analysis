import networkx as nx
import time
import matplotlib.pyplot as plt
import os

def analyze_complexity(file_path):
    # Different sampling ratios (e.g., 20%, 40% of the file, etc.)
    ratios = [0.2, 0.4, 0.6, 0.8, 1.0]
    results = []

    # Read all lines from the file (skip comment lines)
    with open(file_path, 'r') as f:
        lines = [line for line in f if not line.startswith('#')]

    total_lines = len(lines)

    for r in ratios:
        num_edges = int(total_lines * r)
        sampled_lines = lines[:num_edges]

        # Create a temporary sampled graph
        G = nx.parse_edgelist(sampled_lines, nodetype=int)

        num_nodes = G.number_of_nodes()
        actual_edges = G.number_of_edges()

        # Calculate density: 2E / (V * (V-1))
        density = (2 * actual_edges) / (num_nodes * (num_nodes - 1)) if num_nodes > 1 else 0

        # Measure BFS execution time (Sequential - base time)
        start_node = list(G.nodes())[0]
        start_time = time.time()
        _ = list(nx.bfs_edges(G, source=start_node))
        exec_time = time.time() - start_time

        results.append({
            'size': actual_edges,
            'density': density,
            'time': exec_time
        })

        print(f"Ratio %{int(r*100)} completed. Edge: {actual_edges}, Time: {exec_time:.4f}")

    # --- PLOT THE GRAPHS ---
    sizes = [res['size'] for res in results]
    densities = [res['density'] for res in results]
    times = [res['time'] for res in results]

    plt.figure(figsize=(12, 5))

    # Graph 1: Execution Time vs Graph Size
    plt.subplot(1, 2, 1)
    plt.plot(sizes, times, marker='o', color='darkblue')
    plt.title('Execution Time vs Graph Size')
    plt.xlabel('Number of Edges (Size)')
    plt.ylabel('Time (seconds)')
    plt.grid(True)

    # Graph 2: Execution Time vs Density
    plt.subplot(1, 2, 2)
    plt.plot(densities, times, marker='s', color='darkgreen')
    plt.title('Execution Time vs Density')
    plt.xlabel('Density')
    plt.ylabel('Time (seconds)')
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('complexity_analysis.png')
    plt.show()


if __name__ == "__main__":
    analyze_complexity("roadNet-PA.txt")