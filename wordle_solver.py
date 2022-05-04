from starting_word import *
from collections import Counter

def black_checker(black, word):
    for b in black:
        if b in word:
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

def prune_words(words, guess, colors):
    new = []
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

    for word in words:
        if green_checker(green, word):
            if yellow_checker(yellow, word, guess) or len(yellow) == 0:
                if black_checker(black, word):
                    new.append(word)

    return new

def solver(words, num_guesses):
    for i in range(6):
        guess = input("Enter your guess: ")
        if len(guess) != 5:
            print("Guess length should be 5")
            return
        if guess not in words:
            print("Not a valid guess")
            return
        colors = input("Enter your colors: ")
        if colors == "ggggg":
            print(f"You won in {i+1} guesses!")
            return
        if len(colors) != 5:
            print("Color length should be 5")
            return
        words = prune_words(words, guess, colors)
        starting_word(words, num_guesses)

def import_words(file_name):
    with open(file_name) as f:
        words = f.read().splitlines()
    return words

if __name__ == "__main__":
    file_name = "words_solutions.txt"
    num_guesses = 3

    print("Welcome to Worldle Solver!")
    print("File name: " + file_name)
    print(f"Generating the top {num_guesses} guess(es) for your starting word...")
    words = import_words(file_name) 
    starting_word(words, num_guesses)
    solver(words, num_guesses)