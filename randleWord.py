import random 
import bisect
import json
from pathlib import Path

class randleWord():
    def __init__(self, seed=None, language="en", **kwargs):
        """
        Languages included are: English- 'en', Spanish- 'sp'. 
        Working to develop data for Mandarin_Chinese- 'ch', and  French- 'fr'. 
        Other languages not currently supported
        """
        valid = { "en", "sp" }

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
            _abs_path = Path("/randleword/dictionaries/english_words.json")
        
        # mandarin chinese
        # elif self.language == "ch":
        #     _relative_path = Path("./dictionaries/chinese_words.json")
        
        # spanish
        elif self.language == "sp":
            _abs_path = Path("/randleword/dictionaries/spanish_words.json")
        
        # french
        # elif self.language == "fr":
        #     _relative_path = Path("./dictionaries/french_words.json")

        with open(_abs_path, 'r') as openfile:
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
        self.__catch_type_and_value_errors(wordLength, minWordLength, maxWordLength, startsWith)

        # Simple case if no wordLength is specified
        if not wordLength:
            # Everything is default
            if minWordLength == 0 and maxWordLength == 32 and startsWith == '': 
                rand_index = random.randrange(0, self.dict_length)
                return self.word_dict[str(rand_index)]
            
            # only minWordLength is specified
            elif minWordLength != 0 and maxWordLength == 32 and startsWith == '':
                sorted_word_array, min_range = self.__sorted_array_and_find_length_range(_minWordLength=minWordLength)
                rand_index = random.randrange(min_range, len(sorted_word_array))
                return sorted_word_array[rand_index]

            # only maxWordLength is specified
            elif maxWordLength != 32 and minWordLength == 0 and startsWith == '':
                sorted_word_array, max_range = self.__sorted_array_and_find_length_range(_maxWordLength=maxWordLength)
                rand_index = random.randrange(0, max_range)
                return sorted_word_array[rand_index]
            
            # minWordLength and or maxWordLength is specified and startsWith is specified
            elif (minWordLength != 0 or maxWordLength != 32) and startsWith != '':
                # find length range
                sorted_word_array, min_range = self.__sorted_array_and_find_length_range(_minWordLength=minWordLength)
                _, max_range = self.__sorted_array_and_find_length_range(_maxWordLength=maxWordLength)

                # find alphabetic range
                sorted_word_array, min_range, max_range = self.__sorted_array_and_find_alph_range(sorted_word_array, _startsWith=startsWith, _minRange=min_range, _maxRange=max_range)

                rand_index = random.randrange(min_range, max_range)
                return sorted_word_array[rand_index]   

        # If wordLength is explicity specified, ignore the ranges
        else:
            if startsWith == '':
                sorted_word_array, min_range = self.__sorted_array_and_find_length_range(_minWordLength=wordLength)
                _, max_range = self.__sorted_array_and_find_length_range(_maxWordLength=wordLength)
                rand_index = random.randrange(min_range, max_range)
                return sorted_word_array[rand_index]
            
            else:
                sorted_word_array, min_range = self.__sorted_array_and_find_length_range(_minWordLength=wordLength)
                _, max_range = self.__sorted_array_and_find_length_range(_maxWordLength=wordLength)

                # return the full range
                sorted_word_array, min_range, max_range = self.__sorted_array_and_find_alph_range(sorted_word_array, startsWith, _minRange=min_range, _maxRange=max_range)

                rand_index = random.randrange(min_range, max_range)
                return sorted_word_array[rand_index]

    def randWordChoices(self, choiceLength, wordLength=None, minWordLength=0, maxWordLength=32, startsWith=''):
        """
        Returns a choice of random words given a sampleLength, or size of array, wordLength, or minWordLength, maxWordLength
        """
        if not isinstance(choiceLength, int):
            raise TypeError(f"sampleLength must be of type int. You supplied {type(choiceLength)}")
        
        self.__catch_type_and_value_errors(wordLength, minWordLength, maxWordLength, startsWith)

        word_choices = set()
        # Simple case if no wordLength is specified
        if not wordLength:
            # Everything is default
            if minWordLength == 0 and maxWordLength == 32 and startsWith == '': 
                while len(word_choices) < choiceLength:
                    rand_index = random.randrange(0, self.dict_length)
                    word_choices.add(self.word_dict[str(rand_index)])
                return word_choices
            
            # only minWordLength is specified
            elif minWordLength != 0 and maxWordLength == 32 and startsWith == '':
                sorted_word_array, min_range = self.__sorted_array_and_find_length_range(_minWordLength=minWordLength)
                while len(word_choices) < choiceLength:
                    rand_index = random.randrange(min_range, len(sorted_word_array))
                    word_choices.add(sorted_word_array[rand_index])
                return word_choices

            # only maxWordLength is specified
            elif maxWordLength != 32 and minWordLength == 0 and startsWith == '':
                sorted_word_array, max_range = self.__sorted_array_and_find_length_range(_maxWordLength=maxWordLength)
                while len(word_choices) < choiceLength:
                    rand_index = random.randrange(0, max_range)
                    word_choices.add(sorted_word_array[rand_index])
                return word_choices
            
            # minWordLength is specified and startsWith is specified
            elif (minWordLength != 0 or maxWordLength != 32) and startsWith != '':
                # find length range
                sorted_word_array, min_range = self.__sorted_array_and_find_length_range(_minWordLength=minWordLength)
                _, max_range = self.__sorted_array_and_find_length_range(_maxWordLength=maxWordLength)
                # find alphabetic range
                sorted_word_array, min_range, max_range = self.__sorted_array_and_find_alph_range(sorted_word_array, _startsWith=startsWith, _minRange=min_range, _maxRange=max_range)
                while len(word_choices) < choiceLength:
                    rand_index = random.randrange(min_range, max_range)
                    word_choices.add(sorted_word_array[rand_index])
                return word_choices
        
        # If wordLength is explicity specified, ignore the ranges
        else:
            if startsWith == '':
                sorted_word_array, min_range = self.__sorted_array_and_find_length_range(_minWordLength=wordLength)
                _, max_range = self.__sorted_array_and_find_length_range(_maxWordLength=wordLength)
                while len(word_choices) < choiceLength:
                    rand_index = random.randrange(min_range, max_range)
                    word_choices.add(sorted_word_array[rand_index])
                return word_choices
            
            else:
                sorted_word_array, min_range = self.__sorted_array_and_find_length_range(_min_wordLength=wordLength)
                _, max_range = self.__sorted_array_and_find_length_range(_maxWordLength=wordLength)
                
                # return the full range
                sorted_word_array, min_range, max_range = self.__sorted_array_and_find_alph_range(sorted_word_array, startsWith, _minRange=min_range, _maxRange=max_range)
                while len(word_choices) < choiceLength:
                    rand_index = random.randrange(min_range, max_range)
                    word_choices.add(sorted_word_array[rand_index])
                return word_choices
    
    def randWordSample(self, choiceLength, wordLength=None, minWordLength=0, maxWordLength=32, startsWith=''):
        if not isinstance(choiceLength, int):
            raise TypeError(f"sampleLength must be of type int. You supplied {type(choiceLength)}")
        
        self.__catch_type_and_value_errors(wordLength, minWordLength, maxWordLength, startsWith)

        word_choices = []
        # Simple case if no wordLength is specified
        if not wordLength:
            # Everything is default
            if minWordLength == 0 and maxWordLength == 32 and startsWith == '': 
                while len(word_choices) < choiceLength:
                    rand_index = random.randrange(0, self.dict_length)
                    word_choices.append(self.word_dict[str(rand_index)])
                return word_choices
            
            # only minWordLength is specified
            elif minWordLength != 0 and maxWordLength == 32 and startsWith == '':
                sorted_word_array, min_range = self.__sorted_array_and_find_length_range(_minWordLength=minWordLength)
                while len(word_choices) < choiceLength:
                    rand_index = random.randrange(min_range, len(sorted_word_array))
                    word_choices.append(sorted_word_array[rand_index])
                return word_choices

            # only maxWordLength is specified
            elif maxWordLength != 32 and minWordLength == 0 and startsWith == '':
                sorted_word_array, max_range = self.__sorted_array_and_find_length_range(_maxWordLength=maxWordLength)
                while len(word_choices) < choiceLength:
                    rand_index = random.randrange(0, max_range)
                    word_choices.append(sorted_word_array[rand_index])
                return word_choices
            
            # minWordLength is specified and startsWith is specified
            elif (minWordLength != 0 or maxWordLength != 32) and startsWith != '':
                # find length range
                sorted_word_array, min_range = self.__sorted_array_and_find_length_range(_minWordLength=minWordLength)
                _, max_range = self.__sorted_array_and_find_length_range(_maxWordLength=maxWordLength)
                # find alphabetic range
                sorted_word_array, min_range, max_range = self.__sorted_array_and_find_alph_range(sorted_word_array, _startsWith=startsWith, _minRange=min_range, _maxRange=max_range)
                while len(word_choices) < choiceLength:
                    rand_index = random.randrange(min_range, max_range)
                    word_choices.append(sorted_word_array[rand_index])
                return word_choices
        
        # If wordLength is explicity specified, ignore the ranges
        else:
            if startsWith == '':
                sorted_word_array, min_range = self.__sorted_array_and_find_length_range(_minWordLength=wordLength)
                _, max_range = self.__sorted_array_and_find_length_range(_maxWordLength=wordLength)
                while len(word_choices) < choiceLength:
                    rand_index = random.randrange(min_range, max_range)
                    word_choices.append(sorted_word_array[rand_index])
                return word_choices
            
            else:
                sorted_word_array, min_range = self.__sorted_array_and_find_length_range(_min_wordLength=wordLength)
                _, max_range = self.__sorted_array_and_find_length_range(_maxWordLength=wordLength)
                
                # return the full range
                sorted_word_array, min_range, max_range = self.__sorted_array_and_find_alph_range(sorted_word_array, startsWith, _minRange=min_range, _maxRange=max_range)
                while len(word_choices) < choiceLength:
                    rand_index = random.randrange(min_range, max_range)
                    word_choices.append(sorted_word_array[rand_index])
                return word_choices

    
    def __find_left_bound(self, _dct_array, _minWordLength, _startsWith):
        """
        Use binary search to find the left insertion position of the minWordLength or the startsWith key.
        Only one of the two will be supplied to this function at a time. The combination cases where both are specified
        by the user will be handled by the parent function to keep this function simpler.
        """
        # If the array is being queried by the _minWordLength
        if _minWordLength:
            _left = bisect.bisect_left(_dct_array, _minWordLength)

        # If the array is being queried by the starting letter, find the alphabetic insertion index
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
    
    # abstract the randword function
    def __sorted_array_and_find_length_range(self, _minWordLength=None, _maxWordLength=None):
        if _minWordLength:
            _sorted_word_array = self.__dct_sorted_array_by_len()
            _sorted_len_array = self.__len_sorted_array_by_len(_sorted_word_array)
            _min_range = self.__find_left_bound(_sorted_len_array, _minWordLength, None)
            return _sorted_word_array, _min_range 
        
        if _maxWordLength:
            _sorted_word_array = self.__dct_sorted_array_by_len()
            _sorted_len_array = self.__len_sorted_array_by_len(_sorted_word_array)
            _max_range = self.__find_right_bound(_sorted_len_array, _maxWordLength, None)
            return _sorted_word_array, _max_range
    
    def __sorted_array_and_find_alph_range(self, _sorted_word_array, _startsWith, _minRange=0, _maxRange=int(500000)):
        _sorted_word_array = self.__dct_sorted_array_by_alph(_sorted_word_array[_minRange:_maxRange])
        _sorted_len_array = self.__alph_sorted_array_by_alph(_sorted_word_array)
        _min_range = self.__find_left_bound(_sorted_len_array, None, _startsWith)
        _max_range = self.__find_right_bound(_sorted_len_array, None, _startsWith)
        return _sorted_word_array, _min_range, _max_range

    def __catch_type_and_value_errors(self, wordLength, minWordLength, maxWordLength, startsWith):
        if wordLength and not isinstance(wordLength, int):
            raise TypeError(f"wordLength must be of type int not {type(wordLength)}")
        
        if not isinstance(minWordLength, int):
            raise TypeError(f"minWordLength must be of type int not {type(wordLength)}")
    
        if not isinstance(maxWordLength, int):
            raise TypeError(f"maxWordLength must be of type int not {type(wordLength)}")
        
        if not isinstance(startsWith, str):
            raise TypeError(f"startsWith must be of type str not {type(startsWith)}")
        
        if (wordLength and wordLength < 0) or maxWordLength < 0 or minWordLength < 0:
            raise ValueError(f"wordLength must be a positive value or 0")
        
        if (wordLength and wordLength > 31) or minWordLength > 31:
            raise ValueError(f"Length {wordLength} exceeds the max length. The longest word in the dictionary is of length 31")
        

    def seed(self, *args, **kwds):
        "Stub method.  Not used for a system random number generator."
        return None


# Follows the random.py method of instantiating a seed 
# using a stub method to make it more user friendly
_inst = randleWord()
seed = _inst.seed
    
"""
______________________________________________________________
"""






    

