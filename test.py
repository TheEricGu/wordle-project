import random 
from starting_word import *
from wordle_solver import *

def simulate(accepted, solutions, iterations):
  solutions = import_words(solutions)
  accepted = import_words(accepted)
  results = []
  for i in range(iterations):
    solution = random.choice(solutions)
    results.append(test_solver(accepted, solutions, guess, solution))
  wins = 0
  turns = 0  
  losses = 0

  for result in results:
    if result > 0:
      wins += 1
      turns += result
    else:
      losses += 1
    
  print(f"Wins: {wins}")
  print(f"Average turns: {turns/wins}")
  print(f"Losses: {losses}")

simulate("words_accepted.txt", "words_solutions.txt", 3)