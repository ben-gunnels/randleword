# randleword
A random word python module

## Synopsis
---

Use this module to generate a randomly generated word from over 300,000 english words, or over 600,000 spanish words.

## How to use this module

1. Clone this repo in its entirety into your working directory.
for https:
```
  git clone https://github.com/miltiades-the-general/randleword.git
```
for ssh:
```
  git@github.com:miltiades-the-general/randleword.git
```
2. In the parent folder of the cloned directory import the module from the file randleWord.py.
```
  from randleword.randleWord import randleWord
```
3. Use the module as suited for your needs! :)

## Methods
Currently there are three methods provided by this module: randword, randWordChoices, randWordSample.

#### randword
Echos the random.choice() function by generating a single random word from the dictionary given user specifications.

###### Parameters:
  wordLength=None: 
  Specifies a length of the word in characters that the user would like generated. Specifying this negates the use of minWordLength and maxWordLength.
 
  minWordLength=0:
  Specifies the minimum length of word that the user would like to generate. Acts as the starting range. Is negated where wordLength is explicitly provided.
  
  maxWordLength=32: 
  Specifies the maximum length of word that the user would like to generate. Acts as the ending range. Is negated where wordLength is explicitly provided.

  startsWith='':
  Specifies the letter that a user would like to begin the word with alphabetically. 
  
###### Returns:
  String
 
#### randWordChoices
Echos the random.choice() function in conjunction with a for loop to populate a set of a specified length given a users specifications. Words in the set will be unique.

##### Parameters:
  choiceLength:
  Specifies the length of the set of words the user would like to populate.
  
  wordLength=None: 
  Specifies a length of the word in characters that the user would like generated for each word in the set. Specifying this negates the use of minWordLength and maxWordLength.
 
  minWordLength=0:
  Specifies the minimum length of word that the user would like to generate for each word in the set. Acts as the starting range. Is negated where wordLength is explicitly provided.
  
  maxWordLength=32:
  Specifies the maximum length of word that the user would like to generate for each word in the set. Acts as the ending range. Is negated where wordLength is      explicitly provided.

  startsWith='':
  Specifies the letter that a user would like to begin the word with alphabetically for each word in the set. 
 
##### Returns:
  Set
  
#### randWordChoices
Echos the random.choice() function in conjunction with a for loop to populate a list of a specified length given a users specifications. Words in the list may not be unique. 

##### Parameters:
  choiceLength:
  Specifies the length of the list of words the user would like to populate.
  
  wordLength=None: 
  Specifies a length of the word in characters that the user would like generated for each word in the list. Specifying this negates the use of minWordLength and maxWordLength.
 
  minWordLength=0:
  Specifies the minimum length of word that the user would like to generate for each word in the list. Acts as the starting range. Is negated where wordLength is explicitly provided.
  
  maxWordLength=32:
  Specifies the maximum length of word that the user would like to generate for each word in the list. Acts as the ending range. Is negated where wordLength is      explicitly provided.

  startsWith='':
  Specifies the letter that a user would like to begin the word with alphabetically for each word in the list. 
 
##### Returns:
  List

## Copyright
Copyright (c) 2023 Benjamin Gunnels

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
