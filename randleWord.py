import random 
import collections
import numpy
import math
import json
import os
from pathlib import Path

class RandleWord():
    def __init__(self, seed=None, language="en", **kwargs):
        """
        Languages included are: English- 'en', Mandarin_Chinese- 'ch', Spanish- 'sp', French- 'fr'
        """
        valid = { "en", "ch", "sp", "fr" }

        if not isinstance(seed, (type(None), int, float, str, bytes, bytearray)):
            raise TypeError(f"{seed} is not of type Nonetype, int, float, str, bytes, bytearray")
        
        if language not in valid:
            raise ValueError(f"{language} not an accepted language. Please choose one of the following: 'en', 'ch', 'sp', 'fr'.")
        
        self.seed = seed

        random.seed(self.seed)

        self.language = language

        self.word_dict = self.__loadDict()

        self.dict_length = self.__getDictLength()

    def __loadDict(self):
        """
        Return a dictionary object of the word dictionary based on the language chosen on construction.
        Dictionary keys are str(int) for range of len(word dictionary). 
        """
        # english
        if self.language == "en":
            _relative_path = Path("./dictionaries/english_words.json")
        # mandarin chinese
        elif self.language == "ch":
            _relative_path = Path("./dictionaries/chinese_words.json")
        # spanish
        elif self.language == "sp":
            _relative_path = Path("./dictionaries/spanish_words.json")
        # french
        elif self.language == "fr":
            _relative_path = Path("./dictionaries/french_words.json")

        with open(_relative_path, 'r') as openfile:
            dict_object = json.load(openfile)

        return dict_object
    
    def __getDictLength(self):
        """
        Returns the length of the word dict being used
        """
        return len(self.word_dict)

    def randword(self, wordLength=0, minWordLength=0, maxWordLength=1000):
        """
        Returns a single word from the word_dict given a query of wordLength, or from minWordLength - maxWordLength.
        If wordLength is specified then the range from minWordLength, maxWordLength is ignored
        """
        if not isinstance(wordLength, int):
            raise TypeError(f"wordLength must be of type int not {type(wordLength)}")
        
        if not isinstance(minWordLength, int):
            raise TypeError(f"minWordLength must be of type int not {type(wordLength)}")
    
        if not isinstance(maxWordLength, int):
            raise TypeError(f"maxWordLength must be of type int not {type(wordLength)}")

        # Simple case if no wordLength is specified and no word range is specified
        if wordLength == 0:
            if minWordLength == 0 and maxWordLength == 1000: 
                _rand = random.seed(self.seed) 
                _rand_index = _rand.randrange(0, self.dict_length)
                word = self.word_dict[str(_rand_index)]
                return word
        
        # perform binary search on a list sorted by word lengths to find lower and upper bounds
        else:
            pass
        return 

    def randWordList(self, listLength, wordLength, minWordLength, maxWordLength):
        if not isinstance(listLength, int):
            raise TypeError(f"listLength must be of type int. You supplied {type(listLength)}")
    
    def __find_left_bound(self):
        return
    
    def __find_right_bound(self):
        return
    
    def __sorted_array(self):
        return
    
    def __dct_sorted_array(self):
        return 

    def seed(self, *args, **kwds):
        "Stub method.  Not used for a system random number generator."
        return None


# Follows the random.py method of instantiating a seed 
# using a stub method to make it more user friendly
_inst = RandleWord()
seed = _inst.seed
    







    

