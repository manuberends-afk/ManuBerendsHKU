import pygame
import time
import random
from midiutil import MIDIFile

kickname = "../Soundsmp3/kick.mp3"
fileLocation = "Soundsmp3/"
fileType = ".mp3"
pygame.init()

# set the necessary values for MIDI util
velocity=80
track = 0
channel = 9 # corresponds to channel 10 drums
bpm = 120
oneNote = 60 / bpm * 2
noteValue = 1

# create the MIDIfile object, to which we can add notes
mf = MIDIFile(1)

# set name and tempo
timeBeginning = 0
mf.addTrackName(track, timeBeginning, "Beat Sample Track")
mf.addTempo(track, timeBeginning, bpm)


# variables necessary for transforming events to midi output and knowing what sounds we can choose from!
instrMidiPitch = {
    "kick": 36,
    "snare": 37,
    "clap": 38,
    "closed hihat": 39,
    "cowbell": 40,
    "tom": 41,
    "wood perc": 42,
    "open hihat": 43,
    "bass": 44
}


# List that will get filled with every instrument and its notes
listOfSounds = []

# Time signature gets changed first time stepamount is filled in
userTimeSignature = 1

# ask for bpm
def BPM():
    print(("What would you like the bpm to be? -->  "))
    bpm = tryForInt(120, 20, 300, 1)
    return bpm

# Ask for timeSignature
def timeSignature(timeSig):
    print("What would you like the time signature to be? choose: 2-8 (/4) ")
    userTimeSignature = tryForInt(timeSig, 2, 8, 1)
    return userTimeSignature


# Define how many different ellements you want to complete your beat with and return it to user
def amountOfSounds():
    print("How many sounds do you want in the sequence? press \"ENTER\" for default -> 4: ")

    # Check correctness of input
    nmbrOfSounds = tryForInt(4, 1, len(instrMidiPitch), 1)

    return int(nmbrOfSounds)

# Define how many times we will randomly generate the beat and return it to user
def amountOfGens():

    print("How many times will we generate each rythm? press \"ENTER\" for default -> 1000: ")

    # Check correctness of input
    beatGens = tryForInt(1000, 10, 10000000, 1)

    return int(beatGens)

# Define what sounds we will put in the beat
def defineInstrument():

    print("Down here is a list of instruments you can choose out! --->")
    print(instrMidiPitch.items())
    print("Write an exact name so we can add it to the sequence :) ")

    # Check correctness of input
    addInstrument = tryForInstrumentName()
    testSound = fileLocation + addInstrument + fileType
    sample = pygame.mixer.Sound(testSound)
    sample.play()

    return addInstrument

# Ask user how many measures he wants to define.
def amountOfMeasures():
    print("")
    print("For this instrument, how many measures do you want to define? press \"ENTER\" for default -> 1: ")

    # Check correctness of input
    measureAmount = tryForInt(1, 1, 16, 1)

    return int(measureAmount)

# Define the amount of steps in one measure
def amountOfSteps(timeSig):

    print("Enter the number of steps per measure: enter for default", userTimeSignature)
    numberOfSteps = tryForInt(userTimeSignature, 1, 32, userTimeSignature)

    return numberOfSteps

# Generate a list of random strings, either "1" or "0"
def rythmGenerator(steps):

    beat = []
    for i in range(steps): 
        beat.append(str(random.randint(0, 1)))

    return beat

# check wat gewenst wordt en vergelijk met de beats die gegenereerd zijn, output final beat
def rythmCheck(totalRythms, totalSteps):

    correctInput = False

    while not correctInput:

        wish = input("Put your wish here, eg(4 steps -> 101~) :  ")
        wishList = list(wish)

        if len(wishList) == totalSteps:
            correctInput = True
        else:
            print("Input doesn't match the amount of steps you should define")

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
            if wishList[i] == "~":
                beat[i] = "~"

        # if correct add to list of correct rythms
        if beat == wishList:
            checkedRythms.append(contender)
    
    return (checkedRythms)

# Check if input is what we wished for, if time signature doesn't matter the 
def tryForInt(default, min, max, signature):
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
                elif int(userInput) < min:
                    print("Give me a number higher than ", min)
                elif int(userInput) > max:
                    print("Give a number lower than ", max)
                elif int(userInput) % signature > 0:
                    print("input doesn't match current time signature (", signature, "/4)")
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

        for i in instrMidiPitch.items():
            if i[0] == name:
                stringOut = name
                correctInput = True
        if (not correctInput):
            print("INSTRUMENT NOT FOUND (YOU IDIOT)")

    return str(stringOut)

# For playback we need to find the smallest note in the sequence
def smallestNoteTime():
    smalNote = 10
    for event in listOfSounds:
        if event["Note"] <= smalNote:
            smalNote = event["Note"]
    print(smalNote)
    return smalNote

def maxTime():
    print("How long in seconds would you like the beat to take (maximum)")
    maxtime = tryForInt(60, 10, 600, 1)
    return maxtime

        

bpm = BPM()
userTimeSignature = timeSignature(userTimeSignature)
soundAmount = range(amountOfSounds())
generations = range(amountOfGens())

# Every sound will be generated with this for loop, and added to the listOfSounds
for i in soundAmount:
    # Definitions for event that will be added to listOfSounds
    Sound = defineInstrument()
    Measures = 1
    Steps = amountOfSteps(userTimeSignature)

    # Define first step amount as time signature
    if timeSignature == 1:
        timeSignature = Steps

    # This is how many steps the user will define
    totalSteps = Steps * Measures
    noteTime = 4.0 / Steps * (60.0/bpm)

    # Rythms will be saved here
    Rythms = []

    for i in generations:
        Rythms.append(rythmGenerator(totalSteps))

    event = {
        "Sound": Sound,
        "Measures": Measures,
        "Steps": Steps,
        "totalSteps": totalSteps,
        "Note": noteTime,
        "Rythms": Rythms
    }

    # print(event)
    print("Thats a bit too random for us! You get to make a wish!")
    print("Tell me, where is a sound REQUIRED (1), where is a sound RANDOM (~) and where will we definitly NOT play anything (0)")
    print("REMEMBER, you are defining ", Measures, " in ", Steps, " steps")
    print("This means you'll have to define ", totalSteps, "!!!!")

    # Generated rythms will be checked according to wish of user
    event["Rythms"] = rythmCheck(Rythms, totalSteps)

    # All info of a sound is added to the final list
    listOfSounds.append(event)

# print(listOfSounds)

############################

# MIDI GENERATION

for event in listOfSounds:
    timeStamp = 0.0
    noteTime = event["Note"] * 2.0
    print("Time of ", event["Sound"], " note ", noteTime)
    start_offset = 0

    for rythm in event["Rythms"]:
        for step in rythm:
            if step == "1":
                mf.addNote(track, channel, instrMidiPitch[event["Sound"]], timeStamp, noteValue, velocity)
            timeStamp = timeStamp + noteTime


with open("events_lists.midi",'wb') as outf:
    mf.writeFile(outf)




####### Here comes the ugly playback part, sorry! Ran out of time so had to improvise and got this at the end...



# Get smalles note value, important for playback.
smallest = smallestNoteTime()
print("the smallest notetime is: ", smallest)

# Some values
counter = 0
timeStamp = 0
measure = 0
halfMeasure = 0
halfStepCounter = 0
thirdMeasure = 0
thirdStepCounter = 0
qMeasure = 0
qStepCounter = 0
stepCounter = 0
programTime = maxTime()

# Playback loop for every instrument in max time
while timeStamp < programTime:
    for event in listOfSounds:

        if event["Note"] == smallest:
            totalSmalStep = event["Steps"]
            for i, rythms in enumerate(event["Rythms"]):
                if i == measure and rythms[stepCounter] == "1":
                    sound = fileLocation + event["Sound"] + fileType
                    sample = pygame.mixer.Sound(sound)
                    sample.play()

        if event["Note"] == smallest * 2 and counter % 2 == 0:
            for i, rythms in enumerate(event["Rythms"]):
                if i == halfMeasure and rythms[halfStepCounter] == "1":
                    sound = fileLocation + event["Sound"] + fileType
                    sample = pygame.mixer.Sound(sound)
                    sample.play()

# This doesnt work and i dont know why, or do i have time to fix it
        if event["Note"] == smallest * 3 and counter % 3 == 0:
            # halfStep = event["Steps"]
            for i, rythms in enumerate(event["Rythms"]):
                if i == thirdMeasure and rythms[thirdStepCounter] == "1":
                    sound = fileLocation + event["Sound"] + fileType
                    sample = pygame.mixer.Sound(sound)
                    sample.play()

        if event["Note"] == smallest * 4 and counter % 4 == 0:
            # halfStep = event["Steps"]
            for i, rythms in enumerate(event["Rythms"]):
                if i == qMeasure and rythms[qStepCounter] == "1":
                    sound = fileLocation + event["Sound"] + fileType
                    sample = pygame.mixer.Sound(sound)
                    sample.play()

    counter += 1
    stepCounter += 1
    print("step up")

    # I know this could be done waaaay better but this is how the program counts the steps....
    if stepCounter % 2 == 0 and stepCounter > 0:
        halfStepCounter += 1

    if stepCounter % 3 == 0 and stepCounter > 0:
        thirdStepCounter += 1

    if stepCounter % 4 == 0 and stepCounter > 0:
        qStepCounter += 1

    if halfStepCounter >= totalSmalStep:
        halfStepCounter = 0

    if thirdStepCounter >= totalSmalStep:
        thirdStepCounter = 0

    if qStepCounter >= totalSmalStep:
        qStepCounter = 0    

    if stepCounter >= totalSmalStep:
        stepCounter = 0
        halfStepCounter = 0
        thirdStepCounter = 0
        qStepCounter = 0
        measure += 1
        if measure % 2 == 0:
            halfMeasure += 1
        if measure % 3 == 0:
            thirdMeasure += 1
        if measure % 4 == 0:
            qMeasure += 1

    timeStamp = timeStamp + smallest
    print("Time: ", timeStamp, " of total ", programTime)
    time.sleep(smallest)

                




########### Finishing work: make it play
        #   Add more comments
        #   Add looping stuff
        