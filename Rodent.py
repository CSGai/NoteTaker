from note_spy import Paparatsy, get_monitor

monitor_width, monitor_height = get_monitor(2)
screen_grabber = Paparatsy(0, 0, monitor_width, monitor_height, 3)


def main():
    keyboard_height, keyboard_width = keyboard_getter()
    print(f"keyboard height {keyboard_height}")
    print(f"keyboard width {keyboard_width}")


def keyboard_getter():
    coordinates = []
    for i in range(2):
        x, y = screen_grabber.get_mouse_coordinates()
        coordinates.append(x)
        coordinates.append(y)
        print(f"mouse position: {x}, {y}")
    keyboard_width = abs(coordinates[0] - coordinates[2])
    keyboard_height = abs(coordinates[1] - coordinates[3])
    return keyboard_height, keyboard_width


main()
