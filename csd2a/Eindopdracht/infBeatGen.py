import random

totalBeats = []
finalBeats = []

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

# check wat gewenst wordt en vergelijk met de beat die gegenereerd zijn, output final beat
def beatCheck():

    # idx = int(beat.index(input("what instrument are we looking for? ")))
    # wish = input("what steps will DEFINETLY have a sound for this instrument?")
    # #print(total[i+idx, 1])
    # print(total([1, 1]))
    # print(total[2, 2])
    
    name = input("Which instrument? ")

    for i in totalBeats:
        if i[0] == name:
            wish = input("how shall it be organised? : ")
            wish_list = list(wish)
            finalBeats.append(name)
                    
            # geen idee waarom ik hier enumerate gebruik, miss zoek ik iets als len() maar werkte niet
            for beat in i[1:]:
                contender = beat.copy()
                print(contender)
                for i, step in enumerate(beat):
                    if wish_list[i] == "~":
                        beat[i] = "~"

                if beat == wish_list:
                    print("we hebben een winner", contender)
                    finalBeats.append(contender)

                else:
                    print("womp womp")
            print(finalBeats)
            return
    print("Instrument not found.")

soundAmount = range(nmbrOfSounds())
steps = nmbrOfSteps()
generations = range(nmbrOfGens())

for i in soundAmount:
    beat = [defineInstrument()]
    for i in generations:
        beat.append(beatGen(steps))
    totalBeats.append(beat)

print(totalBeats[i])
print(len(totalBeats))

for i in soundAmount:
    beatCheck()
