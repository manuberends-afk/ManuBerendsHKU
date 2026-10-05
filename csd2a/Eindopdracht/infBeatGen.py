import random
from midiutil import MIDIFile

totalBeats = []
finalBeats = []


# Define how many different ellements you want to complete your beat with and return it to user
def amountOfSounds():
    print("How many sounds in the sequence? enter for default 4: ")
    nmbrOfSounds = tryForInt(4)
    return int(nmbrOfSounds)

# Define how many times we will randomly generate the beat and return it to user
def amountOfGens():
    print("How many times will we generate the beat? enter for default 100: ")
    beatGens = tryForInt(100)
    return int(beatGens)

# Define what sounds we will put in the beat
def defineInstrument():
    addInstrument = input("Enter the instrument (e.g., kick, snare, hi-hat): ")
    return addInstrument

def amountOfSteps():
    print("Enter the number of notes per beat: enter for default 4")
    numberOfSteps = tryForInt(4)
    return numberOfSteps

def rythmGenerator(steps):
    beat = []
    for i in range(steps): 
        beat.append(str(random.randint(0, 1)))
    return beat

# check wat gewenst wordt en vergelijk met de beat die gegenereerd zijn, output final beat
def rythmCheck():

    # idx = int(beat.index(input("what instrument are we looking for? ")))
    # wish = input("what steps will DEFINETLY have a sound for this instrument?")
    # #print(total[i+idx, 1])
    # print(total([1, 1]))
    # print(total[2, 2])
    print("welk instrumentje van jouw lijst gaan we organiseren")
    name = tryForInstrumentName()

    for i in totalBeats:
        if i[0] == name:
            wish = input("how shall it be organised? : ")
            wish_list = list(wish)
            finalBeats.append(name)
                    
            # geen idee waarom ik hier enumerate gebruik, miss zoek ik iets als len() maar werkte niet
            for beat in i[1:]:
                contender = beat.copy()
                print(contender)
                for i in range(len(beat)):
                    if wish_list[i] == "~":
                        beat[i] = "~"

                if beat == wish_list:
                    print("we hebben een winner", contender)
                    finalBeats.append(contender)

                else:
                    print("womp womp")
            print(finalBeats)
            print("nu Die andere")
            for i in range(len(finalBeats)):
                print(finalBeats[i])
            return

def tryForInt(default):
    correctInput = False
    nmbr = default
    while (not correctInput):
        userInput = input("Type an int: ")

        if not userInput:
            correctInput = True
        else:
            try:
                nmbr = int(userInput)
                correctInput = True
            except:
                print("DONT TYPE WORDS OR LETTERS")
    return int(nmbr)


def tryForInstrumentName():
    correctInput = False
    stringOut = ""
    print(stringOut)

    while (not correctInput):
        name = input("Type here: ")

        for i in totalBeats:
            if i[0] == name:
                stringOut = name
                correctInput = True
        if (not correctInput):
            print("instrument not found you idiot")

    return str(stringOut)


soundAmount = range(amountOfSounds())
steps = amountOfSteps()
generations = range(amountOfGens())

for i in soundAmount:
    beat = [defineInstrument()]
    for i in generations:
        beat.append(rythmGenerator(steps))
    totalBeats.append(beat)

print(totalBeats)
print(len(totalBeats))

for i in soundAmount:
    rythmCheck()



############################

# set the necessary values for MIDI util
velocity=80
track = 0
channel = 9 # corresponds to channel 10 drums
bpm = 120
note_time = 60 / bpm
note_value = 1
# timeStamp = 0


# create the MIDIfile object, to which we can add notes
mf = MIDIFile(1)
# set name and tempo
time_beginning = 0
mf.addTrackName(track, time_beginning, "Beat Sample Track")
mf.addTempo(track, time_beginning, bpm)

# variables necessary for transforming events to midi output
instr_midi_pitch = {
    "kick": 36,
    "snare": 37,
    "clap": 38,
    "closed hihat": 39,
    "cowbell": 40,
    "tom": 41,
    "wood perc": 42,
    "open hihat": 43
}


for i, event in enumerate(finalBeats):

    if isinstance(event, str):
        instr_name = event
        print(instr_name)
        timeStamp = 0
    else:
        for ind in event:
            if ind == "1":
                mf.addNote(track, channel, instr_midi_pitch[instr_name], timeStamp, note_value, velocity)
            timeStamp = timeStamp + note_time

with open("events_lists.midi",'wb') as outf:
    mf.writeFile(outf)