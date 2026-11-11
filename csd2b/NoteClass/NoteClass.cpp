#include <iostream>



class Note {
public:
    // constructor::
    Note();
    int midiNote;
};

Note::Note(){
    // body of the constructor
    std::cout << "Note::Note() - inside the constructor" << std::endl;
}

int main(){
    Note note;
    std::cout << "/nobject note - midiNote: " << note.midiNote << std::endl;
    std::cout << "/nReached the end of the application. /n";
}