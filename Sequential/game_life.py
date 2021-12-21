import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
from numpy.core.fromnumeric import repeat

N = 200 #We alter grid size according to our requirements
ON = 255
OFF = 0
vals = [ON, OFF]
grid = np.random.choice(vals, N*N, p=[0.6, 0.4]).reshape(N, N)

def game_of_life(data):
  global grid
  #Copy grid to a new grid 
  newGrid = grid.copy()
  for i in range(N):   
    for j in range(N):      
      #Taking toroidal boundary conditions
      total = (grid[i, (j-1)%N] + grid[i, (j+1)%N] +
              grid[(i-1)%N, j] + grid[(i+1)%N, j] +
              grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] +
              grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255
      #Rules of the game
      if grid[i, j]  == ON:
        if (total < 2) or (total > 3):
          newGrid[i, j] = OFF
      else:
        if total == 3:
          newGrid[i, j] = ON  
  #Updating grid
  mat.set_data(newGrid)
  grid = newGrid
  return mat

fig, ax = plt.subplots()
mat = ax.matshow(grid)
# ani = animation.FuncAnimation(fig, game_of_life, frames=100, interval=0,
#                               save_count=50, repeat=False)
# plt.show()

tic = time.time()
for i in range(100):
  game_of_life(fig)
toc = time.time()
print('Time taken for Serial Implementation is',toc-tic,'secs')