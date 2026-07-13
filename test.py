from mpi4py import MPI

comm = MPI.COMM_WORLD

# Print process information: rank (id) and total number of processes
print(f"Hello, I am process {comm.Get_rank()} / total {comm.Get_size()}")