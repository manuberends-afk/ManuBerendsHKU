
import random

# Begin
print('What will be your beat length person?')
beatLength = input('Tell me !"."! —>  ')

print('And what will be your beat signature, PERSON?')
beatSignature = input('Tell me !"."! —>  ')

print('What is your desired kick CHANCE PER STEP?')
kickChance = input('Tell me !"."! —>  ')
print('Now put a 1 where you DO need a kick, a 0 where you DONt want a kick, and leave it blank for its own chance')
print('Like this! ->> 1, , ,0,1, , , ,1, , ,0,1,0, , ,1, , , ,')
kickDesires = input('Tell me !"."! —>  ')


for index in beatLength:
randNm = random.randrange(beatLength)
if randNm < kickChance:
	stepOfBeat = 1;
else:
    stepOfBeat = 0;

if (index == beatLength)