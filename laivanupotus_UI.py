"""
One player (per computer) Battleship game where ship placements are loaded from
<FILENAME>. Game is played by clicking coordinates on the map until every ship
is destroyed.

The goal is to destroy someone else's ships (playing on other computer) before
they destroy your ships.
"""
import _tkinter
from tkinter import *
import winsound

# Scale the UI with this number. Images are scaled at integer intervals.
SCALER = 1

FILENAME = "Battleships.txt"

HEADER_FONT = ("Arial", int(20 * SCALER))
COORDINATE_FONT = ("Arial", int(15 * SCALER))
BUTTON_WIDTH = int(3 * SCALER)

# Global variables
ship_coordinates = []
list_of_ships = []
end_state = False
images_found = False


class Userinterface:
    """
    User interface with explanation labels and a game board. The game board
    contains coordinate labels and coordinate buttons.
    """
    def __init__(self):
        """
        Initialize user interface.
        """
        self.__main_window = Tk()

        # Load images. If load was unsuccessful use symbols instead.
        global images_found
        try:
            # Set images:
            self.__not_shot_image = (PhotoImage(file="not_shot.png")
                                     .zoom(int(SCALER)))
            self.__hit_image = PhotoImage(file="hit.png").zoom(int(SCALER))
            self.__miss_image = PhotoImage(file="miss.png").zoom(int(SCALER))
            images_found = True

        except _tkinter.TclError:
            images_found = False

        self.__hits = []

        # Creating header labels.
        self.__prompt = Label(self.__main_window,
                              text="CLICK TO SHOOT",
                              font=HEADER_FONT)
        self.__prompt.grid(row=0, column=0, columnspan=11)

        self.__shot_outcome = Label(self.__main_window,
                                    text="Start by shooting",
                                    font=HEADER_FONT)
        self.__shot_outcome.grid(row=1, column=0, columnspan=11)

        # Create column to letter dictionary.
        column_letter = {}
        letters = ["", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]
        for num in range(11):
            column_letter[num] = letters[num]

        self.__buttons_list = []  # Empty list to append buttons to.

        # Create the game board containing coordinate labels and corresponding
        # buttons.
        for row in range(11):
            for column in range(11):
                if row == 0:
                    (Label(self.__main_window,
                           text=column_letter[column],
                           font=COORDINATE_FONT)
                     .grid(row=row + 2, column=column))

                elif column == 0:
                    for number in range(10):
                        Label(self.__main_window,
                              text=row - 1,
                              font=COORDINATE_FONT).grid(row=row + 2,
                                                         column=column)

                else:
                    # When button is pressed button's row, column and column
                    # letter is passed into after_shot function.

                    if images_found:
                        button = \
                            (Button(self.__main_window,
                                    image=self.__not_shot_image,
                                    command=lambda row=row, column=column:
                                    self.after_shot(row - 1, column,
                                                    column_letter[column])))

                    else:
                        button = \
                            (Button(self.__main_window,
                                    text="",
                                    width=BUTTON_WIDTH * 2,
                                    height=BUTTON_WIDTH,
                                    command=lambda row=row, column=column:
                                    self.after_shot(row - 1, column,
                                                    column_letter[column])))

                    button.grid(row=row+2, column=column)

                    self.__buttons_list.append(button)

        # Start UI.
        self.__main_window.mainloop()

    def after_shot(self, row, column, column_letter):
        """
        After a shot the shot is evaluated as a hit or a miss using previously
        generated <ship_coordinates> global variable. A shot disables the
        button so the same coordinate can't be shot twice. If every ship has
        been shot the program notices the user and disables clicking
        functionality.

        :param row: int, shot coordinate row index.
        :param column: int, shot coordinate column index.
        :param column_letter: str, corresponding letter for <column> column.
        """
        pressed_button = self.__buttons_list[row * 10 + column - 1]

        shot_coordinate = column_letter + str(row)  # Format: <letter><number>.

        global ship_coordinates, end_state
        if shot_coordinate in ship_coordinates or end_state:
            # A HIT!
            self.__shot_outcome.configure(text="HIT!")

            if not end_state:
                # Play hit sound effect.
                winsound.PlaySound("hit.wav", winsound.SND_ASYNC)

                if images_found:
                    pressed_button.configure(image=self.__hit_image,
                                             state=DISABLED)

                else:
                    pressed_button.configure(text="X", state=DISABLED)

            self.__hits.append(shot_coordinate)

            end_state = check_for_destruction(list_of_ships, self.__hits)

            if end_state:
                # End the game.
                self.__prompt.configure(text="ALL ENEMY SHIPS SUNK!")
                self.__shot_outcome.configure(text="WELL DONE!")

        else:
            # A MISS!
            # Play miss sound effect.
            winsound.PlaySound("miss.wav", winsound.SND_ASYNC)

            self.__shot_outcome.configure(text="MISS!")

            if images_found:
                pressed_button.configure(image=self.__miss_image,
                                         state=DISABLED)

            else:
                pressed_button.configure(text="*", state=DISABLED)


class Battleship:
    """
    Battleship class with ship names, ship coordinates and sunk state.
    """
    def __init__(self, name, coordinates):
        """
        Initialize ship with name, its coordinates and sunk state.

        :param name: str, name of the ship.
        :param coordinates: list, list containing ship coordinates on the game
            board.
        """
        self.set_name(name)
        self.set_coordinates(coordinates)
        self.set_has_sunk(False)

    def set_name(self, name):
        """
        Initialize name of the ship.

        :param name: str, name of the ship.
        """
        self.__name = name

    def get_name(self):
        """
        Return name of the ship.

        :return: str, name of the ship.
        """
        return self.__name

    def set_coordinates(self, coordinates):
        """
        Initialize ship coordinates.

        :param coordinates: list, ship coordinates on the game board.
        """
        self.__coordinates = coordinates

    def get_coordinates(self):
        """
        Return ship coordinate list.

        :return: list, ship coordinates.
        """
        return self.__coordinates

    def set_has_sunk(self, has_sunk):
        """
        Initializes ship's sunk state.

        :param has_sunk: bool, ship's sunk state.
        """
        self.__has_sunk = has_sunk

    def get_has_sunk(self):
        """
        Return ship's sunk state.

        :return: bool, ship's sunk state.
        """
        return self.__has_sunk


def process_file(filename):
    """
    Open <filename>. Create and return list of which odd indices are names and
    even indices are coordinate lists.

    :param filename: str, name of the opened file.
    :return: list, list of a list with ship names in odd indices and their
        coordinates as a list in even indices.
    :raises: OSError, if <filename> was not found.
    :raises: SyntaxError, if <filename>'s syntax is incorrect.
    :raises: ValueError, if ship coordinates are overlapping.
    """
    read_file = open(filename, mode="r")

    # Empty list's to append to.
    ships_list = []

    for line in read_file:
        line = line.replace("\n", "")
        name = line.split(";")[0]
        coordinates = line.split(";")[1:]

        # Check for syntax errors in the line.
        if len(coordinates) == 0:
            raise SyntaxError

        for coordinate in coordinates:
            if len(coordinate) != 2:
                raise SyntaxError

            elif coordinate[0] not in ["A", "B", "C", "D", "E", "F", "G", "H",
                                       "I", "J"]:
                raise SyntaxError

            elif not coordinate[1].isnumeric():
                raise SyntaxError

            elif int(coordinate[1]) not in list(range(10)):
                raise SyntaxError

            # Append coordinate list that contains every coordinate for
            # overlapping check.
            global ship_coordinates
            ship_coordinates.append(coordinate)

        ships_list.append(name)
        ships_list.append(coordinates)

        # Check for overlapping.
        for coordinate in ship_coordinates:
            if ship_coordinates.count(coordinate) != 1:
                raise ValueError

    read_file.close()

    return ships_list


def create_battleship_objects(battleship_list):
    """
    Create Battleship type objects from <battleship_list>'s names and
    coordinates.

    :param battleship_list: list, list of a list with ship names in odd indices
        and their coordinates as a list in even indices.
    :return: list, list of battleship objects.
    """
    global list_of_ships

    for ind in range(int(len(battleship_list) / 2)):
        name = battleship_list[ind * 2]
        coordinates = battleship_list[ind * 2 + 1]
        global list_of_ships
        list_of_ships.append(Battleship(name, coordinates))

    return list_of_ships


def create_hits_dictionary():
    """
    Initialize hits dictionary with zero hits (symbols " "). Dictionary of
    dictionary contains x-coordinates (letters) and y-coordinates (numbers).
    With two coordinate keys dictionary returns the symbol as the value.

    :return: dict, dictionary containing dictionary with hit symbols.
    """
    hits_dict = {}

    for letter in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
        inner_dict = {}
        for number in range(10):
            inner_dict[number] = " "

        hits_dict[letter] = inner_dict

    return hits_dict


def check_for_destruction(list_of_ships, hits_list):
    """
    Update ships destruction state and return True if every ship has been
    destroyed.

    :param list_of_ships: list, list containing every Battleship object.
    :param hits_list: list, contains hit coordinates.
    :return: bool, True if every ship is destroyed.
    """
    # Ship has sunk if every ship coordinate has been hit.
    for ship in list_of_ships:
        if set(hits_list) & set(ship.get_coordinates())\
                == set(ship.get_coordinates()):
            ship.set_has_sunk(True)

    # Return True if every ship has sunk. Firstly, assume that every ship has
    # sunk. If even one ship has not sunk change this assumption.
    every_ship_has_sunk = True
    for ship in list_of_ships:
        if not ship.get_has_sunk():
            every_ship_has_sunk = False

    if every_ship_has_sunk:
        return True

    else:
        return False


def main():
    # Store information from the .txt file containing ship names and
    # coordinates.
    try:
        battleship_list = process_file(FILENAME)

    except OSError:
        print("File can not be read!")
        return

    except SyntaxError:
        print("Error in ship coordinates!")
        return

    except ValueError:
        print("There are overlapping ships in the input file!")
        return

    list_of_ship_objects = create_battleship_objects(battleship_list)

    hits_dict = create_hits_dictionary()

    Userinterface()


if __name__ == "__main__":
    main()
