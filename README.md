This code and accompanying dictionary solve the fivethirtyeight.com riddler problem having to do with "anagram chains": 
https://fivethirtyeight.com/features/can-you-build-the-biggest-anigram/

The process is fairly straightforward: 
* Each word in the dictionary is translated into a hash string that is independent of letter order. Each hash the represents a unique collection of letters. If two words are an anagram of each other, they will have the same hash.
* The hashes are stored in a hash-map mapping hash strings to the set of words that have that set of letters. 
* Then, starting with each 4-letter-word, we do a depth first search over the set of hashes. 
* For performance, we memoize hashes that have already been visited to avoid redendant computation. 