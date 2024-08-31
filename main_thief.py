########################################################################################################################
# Goals: Make a program that takes a video (mp4) of a midi player playing a piano piece, and convert it to an actual
# midi file that can be used later on
# This will require the following:
# 1. Computer Vision (most likely using CV2) Check
# 3. Code to midi
# 5. automation
# The plan is to get an mp4 file of the video in question:
# Go over the video actively and take notes (literally) on each note as the pass by and pasting it to a midi file.
# is this legal? I don't see a reason why transcribing a video wouldn't be,
# just because I'm automating it doesn't make it less legal.
########################################################################################################################

# credits:
# 0. Johnathan BIG save with the midi conversion advice
# 1. Yahav also helped <3


# final thing to add: have loop a key up press to prevent video from darkening
#  add TRUE keyboard reajustablity by reading the baseline to determine key coords based on the black keys as landmarks

from note_spy import *
from cv2 import waitKey
from concurrent.futures import ThreadPoolExecutor
import time
from keyboard import is_pressed


class Rouge:
    threshold1 = 10
    threshold2 = 35
    threshold = threshold2
    # List of all black notes on the piano and their starting locations
    black_notes = ["A#0", "C#1", "D#1", "F#1", "G#1",
                   "A#1", "C#2", "D#2", "F#2", "G#2",
                   "A#2", "C#3", "D#3", "F#3", "G#3",
                   "A#3", "C#4", "D#4", "F#4", "G#4",
                   "A#4", "C#5", "D#5", "F#5", "G#5",
                   "A#5", "C#6", "D#6", "F#6", "G#6",
                   "A#6", "C#7", "D#7", "F#7", "G#7",
                   "A#7"]

    # List of all white notes on the piano
    white_notes = ["A0", "B0", "C1", "D1", "E1", "F1", "G1",
                   "A1", "B1", "C2", "D2", "E2", "F2", "G2",
                   "A2", "B2", "C3", "D3", "E3", "F3", "G3",
                   "A3", "B3", "C4", "D4", "E4", "F4", "G4",
                   "A4", "B4", "C5", "D5", "E5", "F5", "G5",
                   "A5", "B5", "C6", "D6", "E6", "F6", "G6",
                   "A6", "B6", "C7", "D7", "E7", "F7", "G7",
                   "A7", "B7", "C8"]
    # (7+3/88) rotations
    live_keyboard = [
        ["A0", None], ["A#0", None], ["B0", None], ["C1", None], ["C#1", None], ["D1", None], ["D#1", None],
        ["E1", None],
        ["F1", None], ["F#1", None], ["G1", None], ["G#1", None],
        ["A1", None], ["A#1", None], ["B1", None], ["C2", None], ["C#2", None], ["D2", None], ["D#2", None],
        ["E2", None],
        ["F2", None], ["F#2", None], ["G2", None], ["G#2", None],
        ["A2", None], ["A#2", None], ["B2", None], ["C3", None], ["C#3", None], ["D3", None], ["D#3", None],
        ["E3", None],
        ["F3", None], ["F#3", None], ["G3", None], ["G#3", None],
        ["A3", None], ["A#3", None], ["B3", None], ["C4", None], ["C#4", None], ["D4", None], ["D#4", None],
        ["E4", None],
        ["F4", None], ["F#4", None], ["G4", None], ["G#4", None],
        ["A4", None], ["A#4", None], ["B4", None], ["C5", None], ["C#5", None], ["D5", None], ["D#5", None],
        ["E5", None],
        ["F5", None], ["F#5", None], ["G5", None], ["G#5", None],
        ["A5", None], ["A#5", None], ["B5", None], ["C6", None], ["C#6", None], ["D6", None], ["D#6", None],
        ["E6", None],
        ["F6", None], ["F#6", None], ["G6", None], ["G#6", None],
        ["A6", None], ["A#6", None], ["B6", None], ["C7", None], ["C#7", None], ["D7", None], ["D#7", None],
        ["E7", None],
        ["F7", None], ["F#7", None], ["G7", None], ["G#7", None],
        ["A7", None], ["A#7", None], ["B7", None], ["C8", None]
    ]
    og_map = [
        "A0", None, "A#0", None, "B0", None, "C1", None, "C#1", None, "D1", None, "D#1", None,
        "E1", None, "F1", None, "F#1", None, "G1", None, "G#1", None,
        "A1", None, "A#1", None, "B1", None, "C2", None, "C#2", None, "D2", None, "D#2", None,
        "E2", None, "F2", None, "F#2", None, "G2", None, "G#2", None,
        "A2", None, "A#2", None, "B2", None, "C3", None, "C#3", None, "D3", None, "D#3", None,
        "E3", None, "F3", None, "F#3", None, "G3", None, "G#3", None,
        "A3", None, "A#3", None, "B3", None, "C4", None, "C#4", None, "D4", None, "D#4", None,
        "E4", None, "F4", None, "F#4", None, "G4", None, "G#4", None,
        "A4", None, "A#4", None, "B4", None, "C5", None, "C#5", None, "D5", None, "D#5", None,
        "E5", None, "F5", None, "F#5", None, "G5", None, "G#5", None,
        "A5", None, "A#5", None, "B5", None, "C6", None, "C#6", None, "D6", None, "D#6", None,
        "E6", None, "F6", None, "F#6", None, "G6", None, "G#6", None,
        "A6", None, "A#6", None, "B6", None, "C7", None, "C#7", None, "D7", None, "D#7", None,
        "E7", None, "F7", None, "F#7", None, "G7", None, "G#7", None,
        "A7", None, "A#7", None, "B7", None, "C8", None
    ]
    key_starting_timer = og_map.copy()
    key_ending_timer = key_starting_timer.copy()
    timer_buffer = og_map.copy()
    key_buffer = og_map.copy()

    monitor_width, monitor_height = get_monitor(0)
    transformative = Converter()
    screen_grabber = Paparatsy(0, 0, monitor_width, monitor_height, 1)

    def __init__(self):
        self.tests = None
        self.test = None
        self.scrible = None

        self.keyboard_height, self.keyboard_width, self.keyboard_coordinates = self.screen_grabber.keyboard_getter()

        self.screen_grabber.screengrab()
        _, self.scan_line_y = self.screen_grabber.get_mouse_coordinates()

        self.starting_x_val = self.keyboard_coordinates[0]
        # self.starting_x_val = 0

        #   self.sub_base_line = []
        self.safety_margine = 10

        white_layer, black_layer = self.key_layering()
        self.white_layer = white_layer
        self.black_layer = black_layer

        print(f"keyboard height {self.keyboard_height}")
        print(f"keyboard width {self.keyboard_width}")
        print("-" * 100)

        keyboard_collection = white_layer.copy()
        keyboard_collection.update(black_layer)

        pixel_collection = sorted(keyboard_collection.values())
        print(pixel_collection)
        self.pixel_collection = pixel_collection

        self.base_line = [((i, self.scan_line_y), self.screen_grabber.grab_pixel(i, self.scan_line_y)) for i in
                          pixel_collection]
        # self.sub_base_line = [bound for item in self.base_line for bound in
        #                      [item[0][0] - self.safety_margine, item[0][0] + self.safety_margine]]

        self.segment_grabber = Paparatsy(0, self.scan_line_y, self.monitor_width, 1)

        self.timer_initiated = time.time()

    def main(self):
        self.vst()
        while True:

            self.timer_buffer = self.og_map.copy()
            self.key_buffer = self.og_map.copy()

            self.segment_grabber.screengrab()
            active_notes = self.detection_line()

            print(f"{active_notes}\n")

            if is_pressed('alt'):
                self.transformative.finish_song()
                break

    def detection_line(self):
        # checks for a gsv change in the detection line
        with ThreadPoolExecutor() as tpe:
            detected_changes = list(tpe.map(self.detect_gsv_change, self.base_line))
            [tpe.submit(self.false_positive_protection, i, detected_changes) for i in range(len(detected_changes))]

        active_notes = [i for i in self.live_keyboard if i[1] == 1]
        return active_notes

    def false_positive_protection(self, i, detected_changes):
        # # key color => key
        # key = ""
        #
        # left_gsv = self.detect_gsv_change((((self.pixel_collection[i] - self.safety_margine), self.scan_line_y),
        #                                    self.sub_base_line[2 * i]))
        # right_gsv = self.detect_gsv_change((((self.pixel_collection[i] + self.safety_margine), self.scan_line_y),
        #                                    self.sub_base_line[2 * i + 1]))
        # if '#' in self.live_keyboard[i][0]:
        #     key = "black"
        # else:
        #     key = "white"
        if detected_changes[i] == 1:
            if self.live_keyboard[i][1] == 0:
                self.key_starting_timer[i * 2 + 1] = time.time()
            self.live_keyboard[i][1] = 1
            return
            # if key == "black":
            #     if right_gsv == 1 and left_gsv == 1:
            #         if self.live_keyboard[i][1] == 0:
            #             self.key_starting_timer[i * 2 + 1] = time.time()
            #         self.live_keyboard[i][1] = 1
            #         return
            # if key == "white":
            #     if self.live_keyboard[i][1] == 0:
            #         self.key_starting_timer[i * 2 + 1] = time.time()
            #     self.live_keyboard[i][1] = 1
            #     return

        if self.live_keyboard[i][1] == 1:
            self.key_ending_timer[i * 2 + 1] = time.time()

            self.timer_buffer[i * 2 + 1] = self.key_ending_timer[i * 2 + 1] - self.key_starting_timer[i * 2 + 1]

            temp_dict = {"key": self.live_keyboard[i][0],
                         "time": self.key_starting_timer[i * 2 + 1] - self.timer_initiated,
                         "duration": self.timer_buffer[i * 2 + 1]}
            self.transformative.apply_notes(temp_dict)

        self.live_keyboard[i][1] = 0

    def key_layering(self):

        scan_line = self.scan_line_y
        thresh = 100

        black_line = []

        white_notes = self.white_notes
        black_notes = self.black_notes

        dupe_prot = 0

        stv = self.starting_x_val
        # stv = 0
        print("starting key layering process...")
        key_journal = [int(self.screen_grabber.grab_pixel(i, scan_line)) for i in
                       range(self.keyboard_coordinates[0], self.keyboard_coordinates[2], 1)]

        for i in range(len(key_journal)):
            t_i = i + stv
            gsv_diff_b = key_journal[i - 2]

            if gsv_diff_b > thresh:
                if i - 10 > dupe_prot or dupe_prot > i + 10:
                    black_line.append(t_i)
                dupe_prot = i

        black_line = [i-12 for i in black_line]
        white_line = self.screen_grabber.thresholder(self.keyboard_coordinates, scan_line)
        white_line = [self.starting_x_val + i for i in white_line]

        print(len(black_line), len(white_line))
        print(f"black line: {black_line}")
        print(f"white line: {white_line}")

        white_starting_coords = dict(map(lambda i, j: (i, j), white_notes, white_line))
        black_starting_coords = dict(map(lambda i, j: (i, j), black_notes, black_line))

        print(f"{white_starting_coords}\n {black_starting_coords}")
        self.test = black_line
        self.tests = white_line
        return white_starting_coords, black_starting_coords

    def detect_gsv_change(self, base_line_item):
        threshold = self.threshold
        x, y = base_line_item[0]
        base_item_pixel = base_line_item[1]
        pixel_color_value = self.segment_grabber.grab_pixel(x, 0)
        grayscale_diff = abs(int(base_item_pixel) - int(pixel_color_value))
        if grayscale_diff > threshold:
            return 1
        else:
            return 0

    # for testing purposes

    # def rbr(self, key_location):  # ratio based resizer
    #     kb_width = self.keyboard_width
    #     scale_ratio = kb_width / 2560
    #     return int(key_location * scale_ratio)

    def vst(self):
        # visual segmentaiton test

        segment_top_left_x, segment_top_left_y = self.keyboard_coordinates[0], self.keyboard_coordinates[1]
        segment_bot_right_x, segment_bot_right_y = self.keyboard_coordinates[2], self.keyboard_coordinates[3]
        segment = self.screen_grabber.screenshot_segment(segment_top_left_x, segment_top_left_y,
                                                         segment_bot_right_x, segment_bot_right_y)
        self.screen_grabber.display_setup(2, 200, 200)
        self.draw_lines_from_top_to_bottom(segment, self.white_layer, (200, 60, 255))
        self.draw_lines_from_top_to_bottom(segment, self.black_layer, (50, 100, 255))
        for x in self.test:
            cv2.circle(segment, (int(x), 100), 1, (200, 60, 255), -1)
        for x in self.tests:
            cv2.circle(segment, (int(x), 100), 1, (50, 100, 255), -1)
        self.screen_grabber.display_screen_grab(segment, self.keyboard_width, self.keyboard_height)
        waitKey(0)

    # @staticmethod
    def draw_lines_from_top_to_bottom(self, image, pixel_locations, color):
        height, width = image.shape
        # for x in pixel_locations:
        #     start_point = (int(x), 0)
        #     end_point = (int(x), height)
        #     cv2.line(image, start_point, end_point, color, 1)

        for x in self.test:
            start_point = (int(x), 0)
            end_point = (int(x), height)
            cv2.line(image, start_point, end_point, (200, 200, 200), 1)
        for x in self.tests:
            start_point = (int(x), 0)
            end_point = (int(x), height)
            cv2.line(image, start_point, end_point, (50, 100, 255), 1)


test = Rouge()
test.main()
