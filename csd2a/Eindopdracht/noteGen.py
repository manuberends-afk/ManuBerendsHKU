import random

def beatGen():
    placement = input("Enter the placement (e.g., 1---1---1---1-1-): ")
    length = len(placement)
    print("Notes per beat:", length)
    beat = []
    for i in range(length): 
        print("on place 1 of beat: ", placement[i])
        if placement[i] == "1":
            beat.append(placement[i])
        if placement[i] == "-":
            beat.append(str(random.randint(0, 1)))
        if placement[i] == "0":
            beat.append("0")
    return beat

def defineInstrument():
    curInstrument = input("Enter the instrument (e.g., kick, snare, hi-hat): ")
    return curInstrument

def nmbrOfSounds():
    nmbrOfSounds = input("How many sounds in the sequence? : ")
    return nmbrOfSounds

instrumentSequence = {
    "instrument": defineInstrument(),
    "beatGrid": beatGen()
}

print(beatPart)
