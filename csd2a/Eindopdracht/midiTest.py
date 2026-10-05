#
#   https://pypi.org/project/MIDIUtil
#

from midiutil import MIDIFile

finalBeat = ["kick", [1, 0, 1, 0], [1, 1, 1, 1], [1, 1, 1, 1], [1, 0, 1, 0], [1], "snare", [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0]]

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
    "kick": 35,
    "snare": 38
}


for i, event in enumerate(finalBeat):

    if isinstance(event, str):
        instr_name = event
        print(instr_name)
        timeStamp = 0
        loopIndex = i
    else:
        for ind in event:
            if ind == 1:
                mf.addNote(track, channel, instr_midi_pitch[instr_name], timeStamp, note_value, velocity)
            timeStamp = timeStamp + note_time

with open("events_lists.midi",'wb') as outf:
    mf.writeFile(outf)