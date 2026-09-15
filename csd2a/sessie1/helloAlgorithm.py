import numpy as np
import random

kickBeat = np.array([1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0 ,0, 1, 0, 0, 0])
print(kickBeat)
b = kickBeat.astype(bool)
print(b)

# beatLength = int(input('What is the beatlength. --> '))
beatLength = None
while beatLength is None:
    try:
        beatLength = int(input('What is the beatlength. --> '))
    except ValueError:
        print("Not an integer value...")

if beatLength < 100:
    for i in range(beatLength):
        kickBeat[i] = random.getrandbits(1)
        print(kickBeat[i])
print(kickBeat)