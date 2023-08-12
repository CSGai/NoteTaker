import cv2
import numpy
import screeninfo
from pynput import keyboard, mouse
from mss import mss
from mido.midifiles import MidiFile, MidiTrack
from mido.messages import Message


def get_monitor(mon_num, primary=True):
    monitors = screeninfo.get_monitors()
    target_monitor = monitors[mon_num]
    return target_monitor.width, target_monitor.height


class Paparatsy:
    def __init__(self, top_left_x, top_left_y_from_top, width, height, monitor_number=1):
        self.mouse_coords = None
        self.listener = None
        self.k_listener = None
        self.screenshot = None
        with mss() as sct:
            monitor = sct.monitors[monitor_number]
            self.monitor = {
                "top": monitor["top"] + top_left_y_from_top,
                "left": monitor["left"] + top_left_x,
                "width": width,
                "height": height,
                "monitor": monitor
            }

    def screengrab(self, grayscale=True):
        mon = self.monitor
        with mss() as sct:
            img_grab = sct.grab(mon)
            # noinspection PyTypeChecker
            self.screenshot = numpy.array(img_grab)
            if grayscale:
                self.screenshot = cv2.cvtColor(self.screenshot, cv2.COLOR_BGRA2GRAY)

    def screen_save(self):
        cv2.imwrite('screenshots/image.jpg', self.screenshot)

    @staticmethod
    def display_setup(output_mon_num, out_win_pos_offset_x, out_win_pos_offset_y):
        monitor_list = screeninfo.get_monitors()
        target_monitor = monitor_list[output_mon_num]

        cv2.namedWindow("Display", cv2.WINDOW_NORMAL)
        cv2.moveWindow("Display", target_monitor.x + out_win_pos_offset_x, target_monitor.y + out_win_pos_offset_y)

    @staticmethod
    def display_screen_grab(img, width, height, scale=80):
        cv2.resizeWindow("Display", (int(width * scale / 100), int(height * scale / 100)))
        cv2.imshow("Display", img)
        cv2.waitKey(1)

    def grab_pixel(self, y_val, x_val):
        return self.screenshot[x_val][y_val]

    def screenshot_segment(self, top_left_x, top_left_y, bot_right_x, bot_right_y):
        segment = self.screenshot[top_left_y:bot_right_y, top_left_x:bot_right_x]
        return segment

    # Keyboard cords shenanigans
    def get_mouse_coordinates(self):
        self.listener = mouse.Listener(on_move=self.on_move)
        self.k_listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.k_listener.start()
        self.k_listener.join()
        return self.mouse_coords

    def on_press(self, key):
        if key == keyboard.Key.ctrl_r:
            # print("Ctrl+R pressed. Retrieving mouse coordinates...")
            self.listener.stop()
            self.k_listener.stop()

    def on_move(self, x, y):
        self.mouse_coords = (abs(x), abs(y))


class Converter:

    def __init__(self, output_file='song_titile.mid', tempo=500000):

        self.output_file = output_file
        self.midi_file = MidiFile(type=0)
        self.track = MidiTrack()

        self.midi_file.tracks.append(self.track)
        self.track.append(Message('set_tempo', tempo=tempo))

        self.midi_file.save(output_file)

    def apply_notes(self, note_dict):

        for note in note_dict:
            note_number = note['note_number']
            velocity = note['velocity']
            duration = note['duration']

            self.track.append(Message('note_on', note=note_number, velocity=velocity))
            self.track.append(Message('note_off', note=note_number, velocity=0, time=duration))

        self.midi_file.save(self.output_file)
