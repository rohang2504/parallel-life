import numpy
import sys
from matplotlib import pyplot as plt
from mpi4py import MPI
import time

prob = [0.6]
COLS = ROWS = 200 #We alter grid size according to our requirements
generations = 100

comm = MPI.COMM_WORLD
size = comm.Get_size()
rank = comm.Get_rank()
stat = MPI.Status()

subROWS = ROWS//size+2

def msgUp(subGrid):
        # Sends and Recvs rows with Rank+1
        comm.send(subGrid[subROWS-2,:],dest=rank+1)
        subGrid[subROWS-1,:]=comm.recv(source=rank+1)
        return 0

def msgDn(subGrid):
        # Sends and Recvs rows with Rank-1
        comm.send(subGrid[1,:],dest=rank-1)
        subGrid[0,:] = comm.recv(source=rank-1)
        return 0

def newGenetation(subGrid):
    intermediateG = numpy.copy(subGrid)
    for ROWelem in range(1,subROWS-1):
        for COLelem in range(1,COLS-1):
            neighbour_sum = ( subGrid[ROWelem-1,COLelem-1]+subGrid[ROWelem-1,COLelem]+subGrid[ROWelem-1,COLelem+1]
                            +subGrid[ROWelem,COLelem-1]+subGrid[ROWelem,COLelem+1]
                            +subGrid[ROWelem+1,COLelem-1]+subGrid[ROWelem+1,COLelem]+subGrid[ROWelem+1,COLelem+1] )
            if subGrid[ROWelem,COLelem] == 1:
                if neighbour_sum < 2:
                    intermediateG[ROWelem,COLelem] = 0
                elif neighbour_sum > 3:
                    intermediateG[ROWelem,COLelem] = 0
                else:
                    intermediateG[ROWelem,COLelem] = 1
            if subGrid[ROWelem,COLelem] == 0:
                if neighbour_sum == 3:
                    intermediateG[ROWelem,COLelem] = 1
                else:
                    intermediateG[ROWelem,COLelem] = 0
    subGrid = numpy.copy(intermediateG)
    return subGrid

for p in prob:
    N=numpy.random.binomial(1,p,size=(subROWS+2)*COLS)
    subGrid = numpy.reshape(N,(subROWS+2,COLS))

    # BC for all ranks.
    subGrid[:,0] = 0
    subGrid[:,-1] = 0

tic = time.time()
#compute new grid and pass rows to neighbors
oldGrid=comm.gather(subGrid[1:subROWS-1,:],root=0)
for i in range(1,generations+1):
    subGrid = newGenetation(subGrid)
#exhange edge rows for next interation
    if rank == 0:
        msgUp(subGrid)
    elif rank == size-1:
        msgDn(subGrid)
    else:
        msgUp(subGrid)
        msgDn(subGrid)
    newGrid=comm.gather(subGrid[1:subROWS-1,:],root=0)
    if rank == 0: 
        result= numpy.vstack(newGrid)
        print('Generation {} running ...'.format(i))
        plt.imsave('new_state/temp'+str(i)+'.jpg',result)
        plt.show()
toc = time.time()
print('Time taken for parallel implementation is',toc-tic,'secs')