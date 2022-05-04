import random 
from wordle_solver import *

def simulate(words, iterations):
  words = import_words(words)
  results = []
  guess = "saint"
  for i in range(iterations):
    print("Iteration: " + str(i+1))
    solution = random.choice(words)
    print("Solution: " + solution)
    results.append(test_solver(words, guess, solution))

  wins = 0
  turns = 0  
  losses = 0

  for result in results:
    if result > 0:
      wins += 1
      turns += result
    else:
      losses += 1
    
  print(results)
  print(f"Wins: {wins}")
  print(f"Average turns: {turns/wins}")
  print(f"Losses: {losses}")

def find_all_char_positions(word, char):
    positions = []
    pos = word.find(char)
    while pos != -1:
        positions.append(pos)
        pos = word.find(char, pos + 1)
    return positions

def color(guess, solution):
  output = ["b"] * len(solution)
  counted_pos = set()
  for index, (solution_char, guess_char) in enumerate(zip(solution, guess)):
    if solution_char == guess_char:
      output[index] = "g"
      counted_pos.add(index)

  for index, guess_char in enumerate(guess):
    if guess_char in solution and output[index] != "g":
      positions = find_all_char_positions(solution, guess_char)
      for pos in positions:
        if pos not in counted_pos:
          output[index] = "y"
          counted_pos.add(pos)
          break
  return output

def test_solver(words, guess, solution):
    for i in range(6):
        print(f"Guess {i+1}: {guess}")
        colors = "".join(color(guess, solution))
        print(f"Colors: {colors}")
        words = prune_words(words, guess, colors)
        guess = starting_word(words, 1)
        if guess == solution:
            return i+1
    return 0

if __name__ == "__main__":
  iterations = 1
  print(f"Running test simulation with {iterations} iteration(s)")
  simulate("words_solutions.txt", iterations)
