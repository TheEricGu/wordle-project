from collections import Counter
import pandas as pd
import string
from tqdm import tqdm
import re
from pyod.models.copod import COPOD

def import_words(file_name):
    with open(file_name) as f:
        words = f.read().splitlines()
    return words

def starting_word(words_accepted, words_solutions, first):
    if first:
        words_accepted = import_words(words_accepted)
        words_solutions = import_words(words_solutions)
        print("Accepted words:", len(words_accepted))
        print("Solution words:", len(words_solutions))

    accepted_word_string = ''.join(words_accepted)
    letter_counts = dict(Counter(accepted_word_string))
    if first: print("Cumulative letter counts:", letter_counts)

    letter_frequencies = {letter:count/len(words_accepted) 
    for letter,count in letter_counts.items()}
    if first: print("Cumulative letter frequencies:", letter_frequencies)

    letter_frequencies = pd.DataFrame({'Letter':list(letter_frequencies.keys()),
    'Frequency':list(letter_frequencies.values())}).sort_values('Frequency',
    ascending=False)

    letter_positions = []
    for letter in list(string.ascii_lowercase):
        for position in range(5):
            letter_positions.append(f'{letter}:{position}')

    letter_positions_df = pd.DataFrame()
    for word in tqdm(words_solutions): 
        letter_position_str = ''.join([f"{letter}:{position}" for position, letter in enumerate(word)])
        letter_position_counter = {}
        for letter_position in letter_positions:
            letter_position_counter[letter_position] = len(re.findall(letter_position, letter_position_str))

        temp_letter_positions_df = pd.DataFrame(letter_position_counter, index=[word])
        letter_positions_df = pd.concat([letter_positions_df, temp_letter_positions_df])
    if first: 
        print("Letter position dataframe:")
        print(letter_positions_df.head(5))

    if first: print("Shape of letter position dataframe:", letter_positions_df.shape)
    for column in letter_positions_df.columns:
        if letter_positions_df[column].sum() == 0:
            letter_positions_df.drop(column, axis=1, inplace=True)
    if first: print("Shape after dropping columns with only zeros:", letter_positions_df.shape)
            
    if first: print("Fitting COPOD model...")
    copod_model = COPOD(contamination=0.01)
    copod_model.fit(letter_positions_df)

    if first: print("Generating decision scores...")
    letter_positions_df['score'] = copod_model.decision_scores_
    letter_positions_df.sort_values('score',inplace=True)

    if first: print("Top 10 words with highest decision scores:")
    letter_positions_df['rank'] = range(1,len(letter_positions_df)+1)
    print(letter_positions_df.head(10)[['score','rank']])
    return letter_positions_df.index[0]