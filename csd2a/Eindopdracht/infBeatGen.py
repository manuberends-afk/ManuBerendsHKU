import random

total = []

def nmbrOfSounds():
    nmbrOfSounds = input("How many sounds in the sequence? : ")
    return int(nmbrOfSounds)

def nmbrOfGens():
    beatGens = int(input("How many times will we generate the beat? : "))
    return int(beatGens)

def defineInstrument():
    curInstrument = input("Enter the instrument (e.g., kick, snare, hi-hat): ")
    return curInstrument

def nmbrOfSteps():
    numberOfSteps = int(input("Enter the number of notes per beat: "))
    print("Notes per beat: = ", numberOfSteps)
    return numberOfSteps

def beatGen(steps):
    beat = []
    for i in range(steps): 
        beat.append(str(random.randint(0, 1)))
    return beat

def beatCheck():

    # idx = int(beat.index(input("what instrument are we looking for? ")))
    # wish = input("what steps will DEFINETLY have a sound for this instrument?")
    # #print(total[i+idx, 1])
    # print(total([1, 1]))
    # print(total[2, 2])
    
    name = input("Which instrument? ")

    for i in total:
        if i[0] == name:
            wish = input("how shall it be organised? : ")
            for beat in i[1:]:
                if beat == wish
            return

    print("Instrument not found.")

soundAmount = range(nmbrOfSounds())
steps = nmbrOfSteps()
generations = range(nmbrOfGens())

for i in soundAmount:
    beat = [defineInstrument()]
    for i in generations:
        beat.append(beatGen(steps))
    total.append(beat)

for i in soundAmount:
    print(total[i])

beatCheck()
