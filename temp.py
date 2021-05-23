import random
from Player import *
from SakClass import *

letters = ['A', 'A', 'A', 'A', 'B', 'B', 'C', 'C']

a = []
with open('greek7.txt', 'r+') as f:
    for line in f.readlines():
        a.append(line.strip('\n'))

print(a)



