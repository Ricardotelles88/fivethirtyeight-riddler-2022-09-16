A = ord('A')
Z = ord('Z')

# Define a unique hash function that is unique for each possible anagram
# regardless of order
# Make a string or digits of len 26, where each represents the instance of
# that character
def get_word_hash(word):
    d = {chr(c): 0 for c in range(A, Z+1)}

    for c in word:
        d[c] += 1

    num_strings = [str(d[chr(c)]) for c in range(A, Z+1)]
    return "".join(num_strings)


# Build a hashmap that we will use to do a depth first search
def init_hashes(fname):
    f = open(fname)
    words = f.readlines()

    print(f"{len(words)} words read")

    hashes = {}
    
    for word in words:
        word = word.strip().upper()
        hash = get_word_hash(word)
        if hash in hashes:
            hashes[hash].append(word)
        else:
            hashes[hash] = [word]
       
    return hashes

# Use the complete hashset to search for all chains starting from a given anagram
# Returns a tuple of:
#  * the longest chain found from the starting anagram (choses one arbitrarily if there are ties)
#  * the number of total terminated chains starting from the input anagram
#  * the number of chains that reach the longest possible length
def get_longest_chain(hashes, memo, anagram, chain_so_far):
    hash = get_word_hash(anagram)
    if hash not in hashes:
        return ([], 0, 0)

    words = hashes[hash]

    if hash in memo and (len(memo[hash][0]) + len(chain_so_far) < 13):
        return memo[hash]

    longest_chain = [(anagram, words)]
    full_chain = chain_so_far + longest_chain
    if len(full_chain) >= 13:
        print(f"Found chain of len {len(full_chain)}: {full_chain}")

    total_chains = 0
    total_longest_chains = 0

    for c in range(A, Z+1):
        next_anagram = anagram + chr(c) 
        next_chain, num_chains, num_longest_chains  = get_longest_chain(hashes, memo, next_anagram, full_chain)

        if len(next_chain) + 1 > len(longest_chain):
            longest_chain = [(anagram, words)] + next_chain
            total_longest_chains = num_longest_chains
        elif len(next_chain) + 1 == len(longest_chain):
            total_longest_chains += num_longest_chains
        total_chains += num_chains

    # This means this is a leaf of our DFS. 
    # So the total_chains and total_longest_chains = 1
    if total_chains == 0:
        total_chains = 1
        total_longest_chains = 1
    
    memo[hash] = (longest_chain, total_chains, total_longest_chains)
    return (longest_chain, total_chains, total_longest_chains)


#############
## Main   ###
#############
hashes = init_hashes("enable1.txt")

longest_chain = []
total_chains = 0
total_longest_chains = 0
memo = {}

for word_list in hashes.values():
    word = word_list[0]
    if len(word) != 4:
        continue

    next_chain, num_chains, num_longest_chains = get_longest_chain(hashes, memo, word, [])
    total_chains += num_chains

    if len(next_chain) > len(longest_chain):
        longest_chain = next_chain
        total_longest_chains = num_longest_chains
        print(f"Found chain of len {len(next_chain)}: {next_chain}")
    elif len(next_chain) == len(longest_chain):
        total_longest_chains += num_longest_chains
        print(f"Found chain of len {len(next_chain)}: {next_chain}")

print(f"total terminating chains = {total_chains}")
print(f"total chains reaching longest length = {total_longest_chains}")


for (anagram, words) in longest_chain:
    print(anagram)
    print("(" + ", ".join(words) + ")\n")



