import time

# System is y[n] = -2x[n-3]
# This means at a delay of 3 samples, a signal of -2 * input is sent through
# Input [0, 0, 0, -1, 1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0]

delay = 3
multiplier = -2
Yn = [0, 0, 0, -1, 1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0]
Xn = []
delayedSig = []

print(Yn)

for i in range(delay):
    Xn.append(0)

for cur_sig in Yn:
    Xn.append(cur_sig*multiplier)

print(Xn)


