from mpi4py import MPI
import networkx as nx
import time


def parallel_bfs(file_path, start_node):
    # MPI setup
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    # 1. Load graph (every process reads it)
    if rank == 0:
        print(f"Loading graph: {file_path}")

    # Read with NetworkX (skips comment lines starting with '#')
    G = nx.read_edgelist(
        file_path,
        comments='#',
        create_using=nx.Graph(),
        nodetype=int
    )

    # BFS initialization
    visited = {start_node}
    frontier = [start_node]
    level = 0

    # Only Rank 0 measures total execution time
    if rank == 0:
        start_time = time.time()

    # 2. BFS loop (level-by-level)
    while frontier:
        # Distribute current frontier across processes
        # Example: if there are 100 nodes and 4 processes,
        # each process gets 25 nodes
        my_frontier = [
            frontier[i] for i in range(len(frontier))
            if i % size == rank
        ]

        my_next_frontier = set()
        for node in my_frontier:
            for neighbor in G.neighbors(node):
                if neighbor not in visited:
                    my_next_frontier.add(neighbor)

        # 3. SYNCHRONIZATION
        # Each process sends newly discovered nodes to others
        all_new_nodes = comm.allgather(my_next_frontier)

        # Update frontier and visited list
        frontier = []
        for node_set in all_new_nodes:
            for node in node_set:
                if node not in visited:
                    visited.add(node)
                    frontier.append(node)

        level += 1
        if rank == 0 and level % 10 == 0:
            print(
                f"Level {level} completed. "
                f"Current frontier size: {len(frontier)}"
            )

    if rank == 0:
        end_time = time.time()
        print(f"\n--- Parallel BFS Completed ---")
        print(f"Total Time ({size} Processes): {end_time - start_time:.4f} seconds")
        print(f"Total Visited Nodes: {len(visited)}")


if __name__ == "__main__":
    DATA_PATH = "roadNet-PA.txt"  # Make sure the file is in the correct location
    parallel_bfs(DATA_PATH, 0)