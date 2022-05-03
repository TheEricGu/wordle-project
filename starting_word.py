from collections import Counter
import pandas as pd
import string
from tqdm import tqdm

def import_words(file_name):
    with open(file_name) as f:
        words = f.read().splitlines()
    return words

words_accepted = import_words("words_accepted.txt")
words_solutions = import_words("words_solutions.txt")

accepted_word_string = ''.join(words_accepted)
letter_counts = dict(Counter(accepted_word_string))

letter_frequencies = {letter:count/len(words_accepted) 
for letter,count in letter_counts.items()}

letter_frequencies = pd.DataFrame({'Letter':list(letter_frequencies.keys()),
'Frequency':list(letter_frequencies.values())}).sort_values('Frequency',
ascending=False)

letter_positions = []
for letter in list(string.ascii_lowercase):
    for position in range(5):
        letter_positions.append(f'{letter}:{position}')