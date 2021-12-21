Each new generation of the grid will be generated as an image in the newstate directory. 
To run the parallel impelementation, set path of the current direcotry in the terminal and 
run the following commands:

1)	For 4 cores
		
		mpiexec -n 4 python game_life_par.py

2)	For 8 cores

		mpiexec -n 8 python game_life_par.py