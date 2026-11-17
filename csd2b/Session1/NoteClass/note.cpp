#include <iostream>
#include "note.h"

Note::Note(int noteVal){
    // body of the constructor
    std::cout << "Note::Note() - inside the constructor" << std::endl;
    midiNote = noteVal;
}

int Note::octaveUp(){
    midiNote = midiNote + 12;
    return midiNote;
}