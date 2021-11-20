import time
import sys
from game import simulate_all_dices

file_number = int(sys.argv[1])
amount_of_simulations = int(sys.argv[2])
start = time.time()
simulate_all_dices(file_number, amount_of_simulations)
print(time.time() - start)
