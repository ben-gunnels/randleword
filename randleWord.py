import random 
import collections
import bisect
import numpy
import math
import json
import os
from pathlib import Path

class randleWord():
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

    def randword(self, wordLength=None, minWordLength=0, maxWordLength=32, startsWith=''):
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
        
        if not isinstance(startsWith, str):
            raise TypeError(f"startsWith must be of type str not {type(startsWith)}")
        
        if wordLength < 0:
            raise ValueError(f"wordLength must be a positive value or 0")
        
        if wordLength > 31:
            raise ValueError(f"Length {wordLength} exceeds the max length. The longest word in the dictionary is of length 31")

        # Simple case if no wordLength is specified
        if wordLength == 0:
            # Everything is default
            if minWordLength == 0 and maxWordLength == 32 and startsWith == '': 
                _rand_index = random.randrange(0, self.dict_length)
                return self.word_dict[str(_rand_index)]
            
            # only minWordLength is specified
            elif minWordLength != 0 and maxWordLength == 32 and startsWith == '':
                _sorted_word_array = self.__dct_sorted_array_by_len()
                _sorted_len_array = self.__len_sorted_array_by_len(_sorted_word_array)
                _min_range = self.__find_left_bound(_sorted_len_array, minWordLength, None)
                _rand_index = random.randrange(_min_range, len(_sorted_word_array))
                return _sorted_word_array[_rand_index]

            # only maxWordLength is specified
            elif maxWordLength != 32 and minWordLength == 0 and startsWith == '':
                _sorted_word_array = self.__dct_sorted_array_by_len()
                _sorted_len_array = self.__len_sorted_array_by_len(_sorted_word_array)
                _max_range = self.__find_right_bound(_sorted_len_array, maxWordLength, None)
                _rand = random.seed(self.seed)
                _rand_index = _rand.randrange(0, _max_range)
                return _sorted_word_array[_rand_index]
            
            # minWordLength is specified and startsWith is specified
            elif minWordLength != 0 and startsWith != '' and maxWordLength == 0:
                # find length range
                _sorted_word_array = self.__dct_sorted_array_by_len()
                _sorted_len_array = self.__len_sorted_array_by_len(_sorted_word_array)
                _min_range = self.__find_left_bound(_sorted_len_array, minWordLength, None)
                
                # find alphabetic range
                _sorted_word_array = self.__dct_sorted_array_by_alph(_sorted_word_array[_min_range:])
                _sorted_len_array = self.__alph_sorted_array_by_alph(_sorted_word_array)
                _min_range = self.__find_left_bound(_sorted_len_array, None, startsWith)

                _rand_index = random.randrange(_min_range, self.dict_length)
                return _sorted_word_array[_rand_index]
            
            # minWordLength is specified and startsWith is specified
            elif maxWordLength != 32 and startsWith != '' and minWordLength == 0:
                _sorted_word_array = self.__dct_sorted_array_by_len()
                _sorted_len_array = self.__len_sorted_array_by_len(_sorted_word_array)
                _max_range = self.__find_right_bound(_sorted_len_array, maxWordLength, None)
                
                _sorted_word_array = self.__dct_sorted_array_by_alph(_sorted_word_array[:_max_range])
                _sorted_len_array = self.__alph_sorted_array_by_alph(_sorted_word_array)
                _max_range = self.__find_right_bound(_sorted_len_array, None, startsWith)

                _rand_index = random.randrange(0, _max_range)
                return _sorted_word_array[_rand_index]
        
        # If wordLength is explicity specified, ignore the ranges
        else:
            if startsWith == '':
                _sorted_word_array = self.__dct_sorted_array_by_len()
                _sorted_len_array = self.__len_sorted_array_by_len(_sorted_word_array)
                _min_range = self.__find_left_bound(_sorted_len_array, wordLength, None)
                _max_range = self.__find_right_bound(_sorted_len_array, wordLength, None)
                _rand_index = random.randrange(_min_range, _max_range)
                return _sorted_word_array[_rand_index]
            
            else:
                _sorted_word_array = self.__dct_sorted_array_by_len()
                _sorted_len_array = self.__len_sorted_array_by_len(_sorted_word_array)
                _min_range = self.__find_left_bound(_sorted_len_array, wordLength, None)
                _max_range = self.__find_right_bound(_sorted_len_array, wordLength, None)
                
                _sorted_word_array = self.__dct_sorted_array_by_alph(_sorted_word_array[_min_range:_max_range])
                _sorted_len_array = self.__alph_sorted_array_by_alph(_sorted_word_array)
                _min_range = self.__find_left_bound(_sorted_len_array, None, startsWith)
                _max_range = self.__find_right_bound(_sorted_len_array, None, startsWith)

                _rand_index = random.randrange(_min_range, _max_range)
                return _sorted_word_array[_rand_index]

    def randWordSample(self, sampleLength, wordLength, minWordLength, maxWordLength, startsWith):
        """
        Returns a sample of random words given a sampleLength, or size of array, wordLength, or minWordLength, maxWordLength
        """
        if not isinstance(sampleLength, int):
            raise TypeError(f"sampleLength must be of type int. You supplied {type(sampleLength)}")
        
        if not isinstance(wordLength, int):
            raise TypeError(f"wordLength must be of type int not {type(wordLength)}")
        
        if not isinstance(minWordLength, int):
            raise TypeError(f"minWordLength must be of type int not {type(wordLength)}")
    
        if not isinstance(maxWordLength, int):
            raise TypeError(f"maxWordLength must be of type int not {type(wordLength)}")
        
        if not isinstance(startsWith, str):
            raise TypeError(f"startsWith must be of type str not {type(startsWith)}")
    
    def __find_left_bound(self, _dct_array, _minWordLength, _startsWith):
        """
        Use binary search to find the left insertion position of the minWordLength or the startsWith key.
        Only one of the two will be supplied to this function at a time. The combination cases where both are specified
        by the user will be handled by the parent function to keep this function simpler.
        """
        # If the array is being queried by the _minWordLength
        if _minWordLength:
            _left = bisect.bisect_left(_dct_array, _minWordLength)

        # If the array is being queried by the starting letter
        else: 
            _startsWith = ord(_startsWith) - ord("a")
            _left = bisect.bisect_left(_dct_array, _startsWith)
        return _left
    
    def __find_right_bound(self, _dct_array, _maxWordLength, _startsWith):
        """
        Use binary search to find the right insertion position of the maxWordLength or the startsWith key.
        Only one of the two will be supplied to this function at a time. The combination cases where both are specified
        by the user will be handled by the parent function to keep this function simple
        """
        if _maxWordLength:
            _right = bisect.bisect_right(_dct_array, _maxWordLength)

        else:
            _startsWith = ord(_startsWith) - ord("a")
            _right = bisect.bisect_right(_dct_array, _startsWith)
        return _right + 1
    
    def __dct_sorted_array_by_len(self):
        """
        Turns the wordDict into a sorted array by length of the word
        """
        _dct_array = list(self.word_dict.values())

        # sort the array by the length of the word len(smallest) -> len(largest)
        _dct_array.sort(key=len)

        return _dct_array

    def __dct_sorted_array_by_alph(self, _dct_array):
        """
        Turns the wordDict into a sorted array by the alphabetical order of the words
        """
        _dct_array.sort()

        return _dct_array
    
    def __len_sorted_array_by_len(self, _dct_array):
        """
        Produces an array of the word lengths from the sorted _dct_array
        """
        _len_array = [len(_i) for _i in _dct_array]

        return _len_array
    
    def __alph_sorted_array_by_alph(self, _dct_array):
        """
        Produces an array of the alphabetical ordering of the first letter of words from the _dct_array
        """
        _alph_array = []

        for _word in _dct_array:
            # get the ordinate value of the first letter
            _ord = ord(_word[0]) - ord("a")
            _alph_array.append(_ord)
        
        return _alph_array

    def seed(self, *args, **kwds):
        "Stub method.  Not used for a system random number generator."
        return None


# Follows the random.py method of instantiating a seed 
# using a stub method to make it more user friendly
_inst = randleWord()
seed = _inst.seed
    







    

