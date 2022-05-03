from starting_word import *
from collections import Counter
from tqdm import tqdm

def black_checker(black, word):
    for b in black:
        if b in word and word.count(b) == 1:
            return False
    return True

def yellow_checker(yellow, word, guess):
    word_counts = Counter(word)
    guess_counts = Counter(guess)
    for y in yellow:
        if y[0] not in word_counts:
            return False
        if guess_counts[y[0]] > word_counts[y[0]]:
            return False

    for item in yellow:
        if word[item[1]] == item[0]:
            return False
            
    return True

def green_checker(green, word):
    for letter, position in green:
        if word[position] != letter:
            return False
    return True

def prune_words(accepted, solutions, guess, colors):
    new_accepted = []
    new_solutions = []
    black = []
    yellow = []
    green = []

    for i in range(len(guess)):
        if colors[i] == 'b':
            black.append(guess[i])
        elif colors[i] == 'y':
            yellow.append((guess[i], i))
        elif colors[i] == 'g':
            green.append((guess[i], i))
        else:
            print("Invalid color input")
            return

    # print(black)
    # print(yellow)
    # print(green)

    for word in tqdm(accepted):
        if black_checker(black, word):
            if yellow_checker(yellow, word, guess) or len(yellow) == 0:
                if green_checker(green, word):
                    new_accepted.append(word)
    # print("New accepted:", new_accepted)

    for word in tqdm(solutions):
        if black_checker(black, word):
            if yellow_checker(yellow, word, guess):
                if green_checker(green, word):
                    new_solutions.append(word)
    # print("New solutions:", new_solutions)
        
    return new_accepted, new_solutions

def solver(accepted, solutions):
    for i in range(6):
        guess = input("Enter your guess: ")
        if len(guess) != 5:
            print("Guess length should be 5")
            return
        colors = input("Enter your colors: ")
        if colors == "ggggg":
            print(f"You won in {i+1} guesses!")
            return
        if len(colors) != 5:
            print("Color length should be 5")
            return
        accepted, solutions = prune_words(accepted, solutions, guess, colors)
        starting_word(accepted, solutions, False)

print("Welcome to Worldle Solver!")
print("Generating the top 10 best guesses for your starting word...")
starting_word("words_accepted.txt", "words_solutions.txt", True)
accepted = import_words("words_accepted.txt") 
solutions = import_words("words_solutions.txt") 
solver(accepted, solutions)