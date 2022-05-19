from collections import Counter
import pandas as pd
import string
from tqdm import tqdm
import re
from pyod.models.ecod import ECOD
from pyod.models.copod import COPOD
from pyod.models.kde import KDE
from pyod.models.sampling import Sampling
from pyod.models.pca import PCA
from pyod.models.ocsvm import OCSVM
from pyod.models.hbos import HBOS
from pyod.models.iforest import IForest
from pyod.models.so_gaal import SO_GAAL

def starting_word(words, model_type="copod"):
    print(f"{len(words)} words remaining") 

    word_string = ''.join(words)
    letter_counts = dict(Counter(word_string))

    letter_frequencies = {letter:count/len(words) 
    for letter,count in letter_counts.items()}

    letter_frequencies = pd.DataFrame({'Letter':list(letter_frequencies.keys()),
    'Frequency':list(letter_frequencies.values())}).sort_values('Frequency',
    ascending=False)

    letter_positions = []
    for letter in list(string.ascii_lowercase):
        for position in range(5):
            letter_positions.append(f'{letter}:{position}')

    letter_positions_df = pd.DataFrame()
    for word in tqdm(words): 
        letter_position_str = ''.join([f"{letter}:{position}" for position, letter in enumerate(word)])
        letter_position_counter = {}
        for letter_position in letter_positions:
            letter_position_counter[letter_position] = len(re.findall(letter_position, letter_position_str))

        temp_letter_positions_df = pd.DataFrame(letter_position_counter, index=[word])
        letter_positions_df = pd.concat([letter_positions_df, temp_letter_positions_df])

    for column in letter_positions_df.columns:
        if letter_positions_df[column].sum() == 0:
            letter_positions_df.drop(column, axis=1, inplace=True)

    models = {
        "ecod" : ECOD(),
        "copod" : COPOD(),
        "kde" : KDE(),
        "sampling" : Sampling(subset_size=1),
        "pca" : PCA(),
        "ocsvm" : OCSVM(),
        "hbos" : HBOS(),
        "iforest" : IForest(),
        "so_gaal" : SO_GAAL(stop_epochs=2)
    }
    
    model = models[model_type]
    model.fit(letter_positions_df)

    letter_positions_df['score'] = model.decision_scores_
    letter_positions_df.sort_values('score',inplace=True)
    letter_positions_df['rank'] = range(1,len(letter_positions_df)+1)

    print(letter_positions_df.head(5))
    return letter_positions_df.index[0]