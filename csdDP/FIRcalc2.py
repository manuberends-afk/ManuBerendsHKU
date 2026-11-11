import time

# System is y[n] = x[n] - x[n-1]
# This means at a delay of 3 samples, a signal of -2 * input is sent through
# Input [0, 0, 0, -1, 1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 0]

delay1 = 1
delay2 = 2
multiplier1 = 2
multiplier2 = 3
add = True
Yn = [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
Xn = []
delayedSig1 = []
delayedSig2 = []

for i in range(delay1):
    delayedSig1.append(0)

for i in range(delay2):
    delayedSig2.append(0) 

if add:
    for i, cur_sig in enumerate(Yn):
        delayedSig1.append(cur_sig*multiplier1)
        delayedSig2.append(cur_sig*multiplier2)
        Xn.append(cur_sig+delayedSig1[i]+delayedSig2[i])
# else:
#     for cur_sig in Yn:
#         Xn.append(cur_sig*multiplier)

print(Xn)


