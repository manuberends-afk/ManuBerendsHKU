#include <iostream>
#include "note.h"

int main(){
    Note note(60);
    Note otherNote(30);
    std::cout << "/nobject note - midiNote: " << note.midiNote << std::endl;
    std::cout << "/nobject otherNote - midiNote: " << otherNote.midiNote << std::endl;
    note.octaveUp();
    otherNote.octaveUp();
    std::cout << "Octave up gives midiNote: " << note.midiNote << std::endl;
    std::cout << "Octave up gives midiNote: " << otherNote.midiNote << std::endl;
    std::cout << "/nReached the end of the application.";
}