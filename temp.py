import random

a = ['a', 'b', 'c', 'd']
temp = random.randint(0, len(a)-1)
print(a.pop(temp))
