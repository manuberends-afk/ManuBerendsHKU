# timeSignature = 4
# amountOfInstruments = 2
listOfSounds = []

# for i in range(amountOfInstruments):
#     event = {
#         "Sound": input("What is instrument? :  "),
#         "Measures": input("How many measures will we define? "),
#         "noteValue": input("How long is one note? ")
#     }
#     listOfSounds.append(event)

# print(listOfSounds)


import random
from midiutil import MIDIFile

# set the necessary values for MIDI util
velocity=80
track = 0
channel = 9 # corresponds to channel 10 drums
bpm = 120
one_note = 60 / bpm * 2
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


# totalBeats is a list with all instruments, and their generated rythms
totalBeats = []
# finalBeats is a list with all instruments, and their remaining rythms after a certain
finalBeats = []

# Define how many different ellements you want to complete your beat with and return it to user
######## QUESTION TO TEACHER: Hoe dan als ik de max mee wil geven maar niet terug wil krijgen....
def amountOfSounds():
    print("How many sounds do you want in the sequence? press \"ENTER\" for default -> 4: ")
    nmbrOfSounds = tryForInt(4)
    return int(nmbrOfSounds)

# Define how many times we will randomly generate the beat and return it to user
def amountOfGens():
    print("How many times will we generate each rythm? press \"ENTER\" for default -> 100: ")
    beatGens = tryForInt(100)
    return int(beatGens)

# Define what sounds we will put in the beat
def defineInstrument():
    print("Down here is a list of instruments you can choose out! --->")
    print(instr_midi_pitch.items())
    print("Write an exact name so we can add it to the sequence :) ")
    addInstrument = tryForInstrumentName()
    return addInstrument

def amountOfMeasures():
    print("")
    print("For this instrument, how many measures do you want to define? press \"ENTER\" for default -> 1: ")
    measureAmount = tryForInt(1)
    return int(measureAmount)

# Define the amount of steps in one measure
def amountOfSteps(measures):
    print("Enter the number of steps per measure: enter for default 4")
    numberOfSteps = tryForInt(4) * measures
    return numberOfSteps

def noteValue(instr_name):
    print("Enter the length of each step in your measure for the.", instr_name)
    print("imagine 4 kicks to the floor as a length of 1")
    print("If you want to add 4 hihats for every kick, put a 4 here. but remeber your kick will have to look like this: 1000")
    value = float(tryForInt(1))
    note_value = 1.0 / value
    return(note_value)

# Generate a list of random strings, either "1" or "0"
def rythmGenerator(steps):
    beat = []
    for i in range(steps): 
        beat.append(str(random.randint(0, 1)))
    return beat

# check wat gewenst wordt en vergelijk met de beats die gegenereerd zijn, output final beat
def rythmCheck(totalRythms):

    wish = input("Put your wish here, eg(4 steps -> 101~) :  ")
    wish_list = list(wish)
    checkedRythms = []

    # totalRythms is a list that looks like: [['1','0','1','0'], ['0','0','1','0']]
    # Here we start checking each rythm's correctness to the wish
    for beat in totalRythms:        
        # In order to check the user wish with the generated beat, we will reconstruct every beat generated.
        # For example, if the wish is ~~10 and the original generated beat was ['1','0','0','0']
        # The reconstruction will look like ['~','~','0','0']. This new list will be compared with the wish
        # If they are the same, the not formarly generated beat will be added to the final beat.
        # Because the fist in i is the name of the instrument we want to start looking for each generated rythm from i[1] and further so:
        contender = beat.copy()

        for i in range(len(beat)):
            if wish_list[i] == "~":
                beat[i] = "~"

        if beat == wish_list:
            checkedRythms.append(contender)
    
    return (checkedRythms)

def tryForInt(default):
    correctInput = False
    nmbr = default
    while (not correctInput):
        userInput = input("Type an int: ")

        if not userInput:
            correctInput = True
        else:
            try:
                if int(userInput) <= 0:
                    print("VALUE CANT BE NEGATIVE OR ZERO, try again")
                else:
                    nmbr = int(userInput)
                    correctInput = True
            except:
                print("DONT TYPE WORDS OR LETTERS, try again")
    return int(nmbr)


def tryForInstrumentName(): 
    correctInput = False
    stringOut = ""
    while (not correctInput):
        name = input("Type here: ")

        for i in instr_midi_pitch.items():
            if i[0] == name:
                stringOut = name
                correctInput = True
        if (not correctInput):
            print("INSTRUMENT NOT FOUND (YOU IDIOT)")

    return str(stringOut)


soundAmount = range(amountOfSounds())
generations = range(amountOfGens())

for i in soundAmount:
    Sound = defineInstrument()
    Measures = amountOfMeasures()
    Steps = amountOfSteps(Measures)
    Note = Measures / Steps
    Rythms = []
    for i in generations:
        Rythms.append(rythmGenerator(Steps))

    event = {
        "Sound": Sound,
        "Measures": Measures,
        "Steps": Steps,
        "Note": Note,
        "Rythms": Rythms
    }
    print(event)
    print("Thats a bit too random for us! You get to make a wish!")
    print("Tell me, where is a sound REQUIRED (1), where is a sound RANDOM (~) and where will we definitly NOT play anything (0)")
    print("REMEMBER, you are defining ", Measures, " in ", Steps/Measures, " steps")
    print("This means you'll have to define ", Steps, "!!!!")
    event["Rythms"] = rythmCheck(Rythms)
    listOfSounds.append(event)
print(listOfSounds)

# print(totalBeats)
# print(len(totalBeats))

#rythmCheck()

############################

for event in listOfSounds:
    timeStamp = 0
    note_time = one_note * event["Steps"]/4 * event["Measures"]
    start_offset = 0
    maximumReached = False
    for rythm in event["Rythms"]:
        while not maximumReached:
            for step in rythm:
                if step == "1":
                    mf.addNote(track, channel, instr_midi_pitch[event["Sound"]], timeStamp, note_time, velocity)
                timeStamp = timeStamp + note_time + start_offset
                if timeStamp > 1000:
                    maximumReached = True

with open("events_lists.midi",'wb') as outf:
    mf.writeFile(outf)