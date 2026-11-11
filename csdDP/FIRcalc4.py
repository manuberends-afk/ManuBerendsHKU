import time

# System is y[n] = x[n] - x[n-1]
# This means at a delay of 3 samples, a signal of -2 * input is sent through
# Input [0, 0, 0, -1, 1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0]

delay = 1
multiplier = 1
Yn = [0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0]
Xn = []
delayedSig = []

for i in range(delay):
    delayedSig.append(0)

for i, cur_sig in enumerate(Yn):
    delayedSig.append(cur_sig*multiplier)
    Xn.append(cur_sig+delayedSig[i])

print(Xn)
