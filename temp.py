import random
from Player import *
from SakClass import *

#for i in range(7):
    #print(i)

letters=['A','B','C','D']
for i in range(2, len(letters)+1):
    perms = [''.join(p) for p in permutations(letters, i)]
    #perms = permutations(letters, i)
   # print(list(perms))
    # TODO ta perms na ginoun string
    #for combination in perms:
        #print(combination)

for i in range(len(letters), 1, -1):
    perms = [''.join(p) for p in permutations(letters, i)]
    #print(list(perms))



greek7 = {}
with open('greek7.txt', 'r', encoding="utf-8") as f:
    #temp = f.read().splitlines()
    for line in f.read().splitlines():
        greek7[line] = len(line)

def valid_word(word):
    return word in greek7


print(greek7)
print(valid_word("ΣΟΥ"))