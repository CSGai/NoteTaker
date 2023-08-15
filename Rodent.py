from note_spy import Paparatsy, get_monitor
from mido.midifiles import MidiFile, MidiTrack, MetaMessage
from mido.messages import Message

# monitor_width, monitor_height = get_monitor(2)
# screen_grabber = Paparatsy(0, 0, monitor_width, monitor_height, 3)

piano_notes_midi_dict = {
    "A0": 21, "A#0": 22, "B0": 23,
    "C1": 24, "C#1": 25, "D1": 26, "D#1": 27, "E1": 28, "F1": 29, "F#1": 30, "G1": 31, "G#1": 32,
    "A1": 33, "A#1": 34, "B1": 35,
    "C2": 36, "C#2": 37, "D2": 38, "D#2": 39, "E2": 40, "F2": 41, "F#2": 42, "G2": 43, "G#2": 44,
    "A2": 45, "A#2": 46, "B2": 47,
    "C3": 48, "C#3": 49, "D3": 50, "D#3": 51, "E3": 52, "F3": 53, "F#3": 54, "G3": 55, "G#3": 56,
    "A3": 57, "A#3": 58, "B3": 59,
    "C4": 60, "C#4": 61, "D4": 62, "D#4": 63, "E4": 64, "F4": 65, "F#4": 66, "G4": 67, "G#4": 68,
    "A4": 69, "A#4": 70, "B4": 71,
    "C5": 72, "C#5": 73, "D5": 74, "D#5": 75, "E5": 76, "F5": 77, "F#5": 78, "G5": 79, "G#5": 80,
    "A5": 81, "A#5": 82, "B5": 83,
    "C6": 84, "C#6": 85, "D6": 86, "D#6": 87, "E6": 88, "F6": 89, "F#6": 90, "G6": 91, "G#6": 92,
    "A6": 93, "A#6": 94, "B6": 95,
    "C7": 96, "C#7": 97, "D7": 98, "D#7": 99, "E7": 100, "F7": 101, "F#7": 102, "G7": 103, "G#7": 104,
    "A7": 105, "A#7": 106, "B7": 107,
    "C8": 108
}
ticks_per_beat = 480

# def main():
#     keyboard_height, keyboard_width = keyboard_getter()
#     print(f"keyboard height {keyboard_height}")
#     print(f"keyboard width {keyboard_width}")
#
#
# def keyboard_getter():
#     coordinates = []
#     for i in range(2):
#         x, y = screen_grabber.get_mouse_coordinates()
#         coordinates.append(x)
#         coordinates.append(y)
#         print(f"mouse position: {x}, {y}")
#     keyboard_width = abs(coordinates[0] - coordinates[2])
#     keyboard_height = abs(coordinates[1] - coordinates[3])
#     return keyboard_height, keyboard_width


def main():
    output_file = input()
    output_file += ".mid"
    midi_file = MidiFile(type=0)
    track = MidiTrack()
    midi_file.tracks.append(track)
    track.append(MetaMessage('set_tempo', tempo=500000))

    note_dict = [{'key': 'A4',
                  'velocity': 64,
                  'duration': 2
                  },
                 {'key': 'A5',
                  'velocity': 64,
                  'duration': 2
                  }
                 ]
    for note in note_dict:
        key = note['key']
        velocity = note['velocity']
        seconds = note['duration']

        note_number = piano_notes_midi_dict[f'{key}']
        duration = int(seconds * ticks_per_beat)

        track.append(Message('note_on', note=note_number,  velocity=velocity))
        print(f"{note_number}, {duration} correctly")

    for note in note_dict:
        key = note['key']
        velocity = note['velocity']
        seconds = note['duration']
        print("test")
        note_number = piano_notes_midi_dict[f'{key}']
        duration = int(seconds * ticks_per_beat)
        track.append(Message('note_off', note=note_number, velocity=0, time=duration))

    print("finished song")
    midi_file.save(output_file)

# class Converter:
#     piano_notes_midi_dict = {
#         "A0": 21, "A#0": 22, "B0": 23,
#         "C1": 24, "C#1": 25, "D1": 26, "D#1": 27, "E1": 28, "F1": 29, "F#1": 30, "G1": 31, "G#1": 32,
#         "A1": 33, "A#1": 34, "B1": 35,
#         "C2": 36, "C#2": 37, "D2": 38, "D#2": 39, "E2": 40, "F2": 41, "F#2": 42, "G2": 43, "G#2": 44,
#         "A2": 45, "A#2": 46, "B2": 47,
#         "C3": 48, "C#3": 49, "D3": 50, "D#3": 51, "E3": 52, "F3": 53, "F#3": 54, "G3": 55, "G#3": 56,
#         "A3": 57, "A#3": 58, "B3": 59,
#         "C4": 60, "C#4": 61, "D4": 62, "D#4": 63, "E4": 64, "F4": 65, "F#4": 66, "G4": 67, "G#4": 68,
#         "A4": 69, "A#4": 70, "B4": 71,
#         "C5": 72, "C#5": 73, "D5": 74, "D#5": 75, "E5": 76, "F5": 77, "F#5": 78, "G5": 79, "G#5": 80,
#         "A5": 81, "A#5": 82, "B5": 83,
#         "C6": 84, "C#6": 85, "D6": 86, "D#6": 87, "E6": 88, "F6": 89, "F#6": 90, "G6": 91, "G#6": 92,
#         "A6": 93, "A#6": 94, "B6": 95,
#         "C7": 96, "C#7": 97, "D7": 98, "D#7": 99, "E7": 100, "F7": 101, "F#7": 102, "G7": 103, "G#7": 104,
#         "A7": 105, "A#7": 106, "B7": 107,
#         "C8": 108
#     }
#     ticks_per_beat = 480
#
#     def __init__(self, output_file='song_titile.mid'):
#
#         self.output_file = output_file
#         self.midi_file = MidiFile(type=0)
#         self.track = MidiTrack()
#         self.midi_file.tracks.append(self.track)
#
#     def apply_notes(self, note_dict):
#         for note in note_dict:
#             key = note['key']
#             velocity = note['velocity']
#             seconds = note['duration']
#
#             note_number = self.piano_notes_midi_dict[f'{key}']
#             duration = int(seconds * self.ticks_per_beat)
#
#             self.track.append(Message('note_on', note=note_number, velocity=velocity, time=duration))
#             self.track.append(Message('note_off', note=note_number, velocity=0))
#             print(f"{note_number}, {duration} correctly")
#
#     def finish_song(self):
#         print("finished song")
#         self.midi_file.save(self.output_file)


main()
