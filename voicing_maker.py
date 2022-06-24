from midiutil import MIDIFile
from pprint import pprint
import random

maj = [
    (0, 4, 7, 11),
    (0, 6, 9, 14),
    (2, 4, 7, 11),
    (4, 9, 14, 19),
    (4, 7, 9, 14),
    (7, 11, 12, 16),
    (11, 12, 16, 19)
]

minor = [
    (0, 3, 7, 10),
    (0, 3, 7, 9),
    (0, 5, 10, 15),
    (3, 7, 10, 14),
    (5, 10, 15, 19),
    (10, 14, 15, 19)
]

dom = [
    (0, 4, 7, 10),
    (4, 9, 10, 14),
    (4, 8, 10, 13),
    (5, 11, 16, 21),
    (10, 14, 15, 19),
    (10, 14, 15, 21),
    (10, 15, 16, 20)
]

midlib = {
    "C": 48,
    "Db": 49,
    "D": 50,
    "Eb": 51,
    "E": 52,
    "F": 53,
    "Gb": 54,
    "G": 55,
    "Ab": 56,
    "A": 57,
    "Bb": 58,
    "B": 59
}

backref = {
    0: "C",
    1: "Db",
    2: "D",
    3: "Eb",
    4: "E",
    5: "F",
    6: "Gb",
    7: "G",
    8: "Ab",
    9: "A",
    10: "Bb",
    11: "B",
}

keyref = {
    48: 'a',
    49: 'b',
    50: 'c',
    51: 'd',
    52: 'e',
    53: 'f',
    54: 'g',
    55: 'h',
    56: 'i',
    57: 'j',
    58: 'k',
    59: 'l',
    60: 'm',
    61: 'n',
    62: 'o',
    63: 'p',
    64: 'q',
    65: 'r',
    66: 's',
    67: 't',
    68: 'u',
    69: 'v',
    70: 'w',
    71: 'x',
    72: 'y',
    73: 'z',
    74: '0',
    75: '1',
    76: '2',
    77: '3',
    78: '4',
    79: '5',
    80: '6',
    81: '7',
    82: '8',
    83: '9'
}

print("ENTER 'exit' TO QUIT")

progression = ""

while (progression != "exit"):

    print("\n")
    print("Usage: Enter Chord progression, each chord separated by comma")
    print("Use flat notation only i.e. its Gb not F#")
    print("use 'm' for minor, 'M' for major and '7' for dom ")

    progression = input("Enter progression: ")
    if progression == "exit":
        break

    name = input("Enter midi name: ")
    name = name + ".mid"

    print("**************************************************************************************************************")

    chords = progression.split(",")

    def print_keyboard(chord):

        file = open("keybed.txt", "r")
        data = file.read()
        keybednotes = data.split("\n")
        file.close()

        for note in chord:
            keypos = keyref[note]

            for i in range(len(keybednotes)):
                keybednotes[i] = keybednotes[i].replace(keypos, "X")

        for i in range(len(keybednotes)):
            for j in range(len(keybednotes[i])):
                v = keybednotes[i][j]
                if (v == "X") or (v == ' ') or (v == "|") or (v == '_') or (v == '#'):
                    pass
                else:
                    keybednotes[i] = keybednotes[i].replace(v, " ")

        for line in keybednotes:
            print(line)

    def voicing_maker(last_chord_values, new_root_value, chord_type_options):
        options = [[0 for i in range(4)] for j in range(len(chord_type_options))]
        i = 0
        for optionset in chord_type_options:
            j = 0
            for value in optionset:
                options[i][j] = (value+new_root_value)
                j += 1
            i += 1

        difference = list()
        j = 0

        for option in options:
            diff = []
            for i in range(len(option)):
                diff.append(abs(option[i] - last_chord_values[i]))
            difference.append(sum(diff))
            j += 1

        min_value = min(difference)
        option_choice = difference.index(min(difference))
        new_chord_values = options[option_choice]

        return new_chord_values

    first_type = chords[0][-1]
    if first_type == 'm':
        choice = minor
    elif first_type == 'M':
        choice = maj
    elif first_type == '7':
        choice = dom

    root = chords[0][:-1]
    root_value = midlib[root]

    voicing = random.randint(0, len(choice)-1)

    first_chord = []
    for item in choice[voicing]:
        first_chord.append(item+root_value)

    chord_sequence = []

    last_chord = first_chord

    for chord in chords:
        ctype = chord[-1]
        if ctype == 'm':
            choice = minor
        elif ctype == 'M':
            choice = maj
        elif ctype == '7':
            choice = dom

        root = chord[:-1]

        root_value = midlib[root]
        new_chord = voicing_maker(last_chord, root_value, choice)

        last_chord = new_chord

        chord_sequence.append(new_chord)

    def print_notes(notes_list):
        ch = ""
        for value in notes_list:
            ch = ch + " " + backref[value % 12]

        return ch

    i = 0
    for chord in chord_sequence:
        print("===========================================================================================================")
        print("Chord: ", chords[i])
        print("Notes: ", print_notes(chord))
        print("Keyboard: ")
        print_keyboard(chord)

        i += 1
        print("\n")

    track = 0
    channel = 0
    time = 0    # In beats
    duration = 2    # In beats
    tempo = 60   # In BPM
    volume = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)    # One track, defaults to format 1 (tempo track is created # automatically)
    MyMIDI.addTempo(track, time, tempo)

    i = 0
    for chord in chord_sequence:
        MyMIDI.addNote(track, channel, chord[0], time + i, duration, volume)
        MyMIDI.addNote(track, channel, chord[1], time + i, duration, volume)
        MyMIDI.addNote(track, channel, chord[2], time + i, duration, volume)
        MyMIDI.addNote(track, channel, chord[3], time + i, duration, volume)
        i += 1

    with open(name, "wb") as output_file:
        MyMIDI.writeFile(output_file)
