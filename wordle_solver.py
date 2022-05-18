from starting_word import *
from collections import Counter

def black_checker(black, green_and_yellow, word, guess):
    for b in black:
        if b in word:
            if b not in green_and_yellow:
                return False
            else:
                # There are too many of this character in this word. 
                # Let n be the number of instances this character is in the GUESS word. All words with n instances of this character must be pruned.
                word_counts = Counter(word)
                guess_counts = Counter(guess)
                if word_counts[b] >= guess_counts[b]:
                    return False
            
    return True

def yellow_checker(yellow, green, word, guess, black):
    word_counts = Counter(word)
    guess_counts = Counter(guess)
    for y in yellow:
        if y[0] not in word_counts:
            return False
        for g in green:
            if y[0] in g:
                # There are greater than 1 instance of this character in this word.
                if (word_counts[y[0]] != guess_counts[y[0]]) and not y[0] in black:
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
    green_and_yellow = []
    for i in range(len(guess)):
        if colors[i] == 'b':
            black.append(guess[i])
        elif colors[i] == 'y':
            yellow.append((guess[i], i))
            green_and_yellow.append(guess[i])
        elif colors[i] == 'g':
            green.append((guess[i], i))
            green_and_yellow.append(guess[i])
        else:
            print("Invalid color input")
            return

    for word in words:
        if green_checker(green, word):
            if yellow_checker(yellow, green, word, guess, black) or len(yellow) == 0:
                if black_checker(black, green_and_yellow, word, guess):
                    new.append(word)

    return new

def solver(words):
    for i in range(6):
        guess = input("Enter your guesss: ")
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
        starting_word(words)

def import_words(file_name):
    with open(file_name) as f:
        words = f.read().splitlines()
    return words

if __name__ == "__main__":
    file_name = "words_accepted.txt"
    print("Welcome to Worldle Solver!")
    print("File name: " + file_name)
    print(f"Generating the top guess(es) for your starting word...")
    words = import_words(file_name)
    starting_word(words)
    solver(words)