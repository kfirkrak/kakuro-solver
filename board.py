import copy

BIGGEST_NUM = 9
TILE_START_VALUE = "#"

INDEX_SUM = 0
INDEX_NUM_TILES = 1
INDEX_ORIENTATION = 2
INDEX_START_X = 3
INDEX_START_Y = 4

ALL_NUMBERS = [i for i in range(1, BIGGEST_NUM + 1)]
BASE_SET = set(ALL_NUMBERS)
HORIZONTAL = 0
VERTICAL = 1
EMPTY_S = "X"
CONST_S = "@"
SQUARE_S = 0
FLAG = (-1, -1)
BASE_SER_NUM = "000"
SEPARATE = '>'
X_INDEX = 0
Y_INDEX = 1

possible_dict = {}


class Tile:
    """
    A class representing a single place on the board
    this place does not know the logic of the game,
    just to place a single number
    """

    def __init__(self, row, col):
        """
        Constructor of a new tile
        :param row: the x coordinate
        :param col: the y coordinate
        """

        self.row = row
        self.col = col
        self.visited = False
        self.value = TILE_START_VALUE

        # set of the numbers 1 to the biggest possible number
        self.poss_values = ALL_NUMBERS
        self.constraints = set()

    def get_row(self):
        """
        :return: the x-coordinate of this tile
        """
        return self.row

    def get_col(self):
        """
        :return: the y-coordinate of this tile
        """
        return self.col

    def get_value(self):
        """
        :return: this tile's value
        """
        return self.value

    def is_visited(self):
        """
        :return: true if this tile has been visited
        """
        return self.visited

    def possible_values(self):
        """
        :return: the possible values for this tile
        """
        return self.poss_values

    def set_value(self, value):
        """
        Putting the number in this tile
        :param value: the number we wish to put in this tile
        """
        self.value = value
        self.poss_values = [value]
        self.visited = True

    def add_constraint(self, index):
        """
        Add a constraint to this tile's constraints
        :param index: the index of the constraint
        """
        self.constraints.add(index)

    def get_constraints(self):
        """
        :return: The set of constraints for this tile
        """
        return self.constraints

    def intersect_possible_values(self, known_values):
        """
        Updating the possible values set
        :param known_values: a list of values to put in our possibles
        """
        old_values = self.poss_values
        self.poss_values = []
        for val in known_values:
            if val in old_values:
                self.poss_values.append(val)

    def remove_value_from_possible(self, value):
        """
        Removing a giving number from the possible values for this tile
        :param value: the number to remove
        :return: True if this number was a possibility and got removed
        """
        if value not in self.poss_values:
            return False
        self.poss_values.remove(value)
        return True

    def num_possible(self):
        """
        :return: the number of possible constraint for this tile
        """
        return len(self.poss_values)


class Constraint:
    """
    A class representing a constraint for a giving board
    """

    def __init__(self, total_sum, num_tiles, orientation,
                 start_tile_row, start_tile_col, index):
        """
        Constructor for a constraint
        :param total_sum: the number to sum up to
        :param num_tiles: number of tiles in this constraint
        :param start_tile_row: the row for this constraint
        :param start_tile_col: the column for this constraint
        :param orientation: vertical or horizontal constraint
        :param index: the serial number of this constraint
        """
        self.total_sum = total_sum
        self.num_tiles = num_tiles
        self.start_tile_row = start_tile_row
        self.start_tile_col = start_tile_col
        self.orientation = orientation
        self.index = index
        self.locations = []
        self.find_locations()

        # possible values list for this constraint tiles
        self.possible_sets = []
        self.possible_numbers = set()
        options = self.calculate_possible_subsets(total_sum, num_tiles)
        for option in options:
            self.possible_sets.append(option)
            for number in option:
                self.possible_numbers.add(number)

    def find_locations(self):
        """
        Finding the places of this constraint's tile on the board
        """
        if self.orientation == VERTICAL:
            for i in range(self.start_tile_row + 1, self.start_tile_row + self.num_tiles + 1):
                self.locations.append((i, self.start_tile_col))
        else:
            for i in range(self.start_tile_col + 1, self.start_tile_col + self.num_tiles + 1):
                self.locations.append((self.start_tile_row, i))

    def get_total_sum(self):
        """
        :return: number of tiles in this constraint
        """
        return self.total_sum

    def get_locations(self):
        """
        :return: the locations of this constraint
        """
        return self.locations

    def get_num_tiles(self):
        """
        :return: the number of tile in this constraint
        """
        return self.num_tiles

    def is_in(self, loc):
        """
        Check is loc is under this constraint
        :param loc: the place on the board
        :return: True if it is in this constraint
        """
        return loc in self.locations

    def get_index(self):
        """
        :return: this constraint's index
        """
        return self.index

    def get_possible_placements(self):
        """
        :return: the list of possible values for the tiles
        """
        return self.possible_sets

    def get_possible_numbers(self):
        """
        :return: the possible numbers that can be places in this constraint
        """
        return self.possible_numbers

    def calculate_possible_subsets(self, total_sum, num_tiles):
        if total_sum < num_tiles or total_sum <= 0 or num_tiles <= 0:
            return []
        if (total_sum, num_tiles) in possible_dict:
            return possible_dict[(total_sum, num_tiles)]
        possible_dict[(total_sum, num_tiles)] = []
        if num_tiles == 1:
            if total_sum > BIGGEST_NUM:
                return []
            possible_dict[(total_sum, num_tiles)].append([total_sum])
            return possible_dict[(total_sum, num_tiles)]
        cur_possible = set()
        for i in range(1, BIGGEST_NUM + 1):
            sub_options = self.calculate_possible_subsets(total_sum - i, num_tiles - 1)
            for option in sub_options:
                if i in option:
                    continue
                new_option = (tuple(sorted([i] + option)))
                cur_possible.add(new_option)
            i += 1
        for option in cur_possible:
            possible_dict[(total_sum, num_tiles)].append(list(option))
        return possible_dict[(total_sum, num_tiles)]

    def remove_placement(self, placement):
        if placement in self.possible_sets:
            self.possible_sets.remove(placement)
            self.possible_numbers = set()
            for option in self.possible_sets:
                for number in option:
                    self.possible_numbers.add(number)

    def remove_placements_without_numbers(self, numbers):
        """
        Remove all the possibilities without some numbers,
        and updates the possible numbers
        :param numbers: the numbers we know are in this constraint
        """
        for possibility in self.possible_sets:
            for number in numbers:
                if number not in possibility:
                    self.possible_sets.remove(possibility)
                    break

        self.possible_numbers = set()
        for possibility in self.possible_sets:
            for number in possibility:
                self.possible_numbers.add(number)

    def __str__(self):
        """
        Print function for a constraint
        """
        final_string = ""
        for location in self.locations:
            final_string += "(" + str(location[X_INDEX]) + "," + str(location[Y_INDEX]) + ")" + " "
        return "In places: " + final_string + "we sum to: " + str(self.total_sum)


class Board:
    """
    This class represent a single game board
    """

    def __init__(self, constraints):
        """
        Constructs a new board
        :param constraints: list of constraints to place on this boars
        """
        self.dimensions = self.choose_board_dimensions(constraints)
        self.serial_num = BASE_SER_NUM

        self.tiles = {}
        self.constraints = {}

        # adding each constraint onto the board
        for constraint in constraints:
            self.add_const(constraint)

    @staticmethod
    def choose_board_dimensions(constraints):
        """
        Choosing the size of this board, based on the constraints list
        :param constraints: the list of constraint for this board
        :return: the size for the board, based on the given constraints
        """
        max_x = 0
        max_y = 0
        for i in range(len(constraints)):
            num_tiles = constraints[i][INDEX_NUM_TILES]
            if constraints[i][INDEX_ORIENTATION] == HORIZONTAL:
                new_max = constraints[i][INDEX_START_X] + num_tiles - 1
                max_y = max(max_y, new_max)
            else:
                new_max = constraints[i][INDEX_START_Y] + num_tiles - 1
                max_x = max(max_x, new_max)
        return max_x, max_y

    def one_move_board_copy(self, value, row, col):
        """
        Create new board from this board, with one extra move
        :param value: the number we want to place on the board
        :param row: the row
        :param col: the column
        :return: the newly created board
        """
        if value not in BASE_SET:
            return None
        new_board = copy.deepcopy(self)
        new_board.place_tile(value, row, col)
        new_board.serial_num += ">" + str(value) + "(" + str(row) + str(col) + ")"
        return new_board

    def set_serial_num(self, num):
        """
        Sets the board serial number
        :param num: the new serial number
        """
        self.serial_num = num

    def get_serial_num(self):
        """
        Gets this board serial number
        :return: the serial number of this board
        """
        return self.serial_num

    def __str__(self):
        s = ""
        for row in range(self.dimensions[0]):
            for col in range(self.dimensions[1]):
                if (row, col) in self.tiles:
                    tile = self.get_tile(row, col)
                    s += str(tile.get_value())
                else:
                    s += TILE_START_VALUE
            s += "\n"
        return s

    def add_const(self, constraint):
        """
        Adding a constraint to the board's constraint list
        :param constraint: the information for this constraint
        """
        const_index = len(self.constraints)

        # creating the new constraint
        new_constraint = Constraint(constraint[INDEX_SUM],
                                    constraint[INDEX_NUM_TILES],
                                    constraint[INDEX_ORIENTATION],
                                    constraint[INDEX_START_X],
                                    constraint[INDEX_START_Y],
                                    const_index)
        self.constraints[const_index] = new_constraint

        # linking it to tiles on the board
        possible_values = new_constraint.get_possible_numbers()
        for location in new_constraint.get_locations():
            row = location[X_INDEX]
            col = location[Y_INDEX]

            # if this tile not on board yet, we'll add it
            if (row, col) not in self.tiles:
                self.tiles[(row, col)] = Tile(row, col)

            # remembering that this tile is under this constraint
            cur_tile = self.tiles[(row, col)]
            cur_tile.add_constraint(const_index)

            # updating the possible values for this tile
            cur_tile.intersect_possible_values(possible_values)
        return

    def get_tile(self, row, col):
        """
        Gets the tile in location [row][col]
        :param row:
        :param col:
        :return: the tile is found, None if there's no tile on this location
        """
        if (row, col) not in self.tiles:
            return None
        return self.tiles[(row, col)]

    def get_tiles(self):
        """
        Gets all the tiles of this board
        :return:
        """
        return self.tiles

    def get_constraint(self, index):
        """
        Gets the constraint with index [index]
        :param index:
        :return: the constraint if found, else none
        """
        if index not in self.constraints:
            return None
        return self.constraints[index]

    def get_related_tiles(self, row, col):
        """
        Gets the tiles in constraint with the tile in location [row][col]
        :param row:
        :param col:
        :return: set of all the tiles in constraints with this tile
        """
        related_tiles = set()
        cur_tile = self.get_tile(row, col)
        for const_index in cur_tile.get_constraints:
            cur_const = self.get_constraint(const_index)
            for location in cur_const.get_locations:
                related_tiles.add(location)
        return related_tiles

    def num_related_tiles(self, row, col):
        """
        Gets the number of tiles in constraints with the tile in location [row][col]
        """
        return len(self.get_related_tiles(row, col)) - 2

    def place_tile(self, value, row, col):
        """
        Placing the number value in location [row][col] on the board
        :param value: the number we want to place
        :param row: the row to place
        :param col: the col to place
        """
        tile = self.get_tile(row, col)
        for const_index in tile.get_constraints():
            constraint = self.get_constraint(const_index)
            constraint.remove_placements_without_numbers([value])
            new_possible_values = constraint.get_possible_numbers()
            if value in new_possible_values:
                new_possible_values.remove(value)
            for location in constraint.get_locations():
                if location[X_INDEX] == row and location[Y_INDEX] == col:
                    continue
                cur_tile = self.get_tile(location[X_INDEX], location[Y_INDEX])
                if cur_tile.is_visited():
                    continue
                cur_tile.intersect_possible_values(new_possible_values)

        # placing the number in the location
        tile.set_value(value)

    def tile_poss_values(self, row, col):
        """
        Get the possible numbers to put in location loc
        :param row:
        :param col:
        :return: the list of possible values
        """
        tile = self.get_tile(row, col)
        return tile.possible_values()

    def is_legal(self):
        """
        :return: True if this board is legal
        """
        # do we have a tile with 0 possible values
        for tile in self.tiles.values():
            if tile.num_possible() == 0:
                return False

        # checks that all the constraints are okay:
        # 1. they don't sum to more than the sum of the const
        # 2. we don't have number repetitions
        for constraint in self.constraints.values():
            cur_values = []
            for tile_index in constraint.get_locations():
                cur_tile = self.get_tile(tile_index[X_INDEX], tile_index[Y_INDEX])
                if cur_tile.is_visited():
                    cur_values.append(int(cur_tile.get_value()))
            cur_sum = sum(cur_values)
            if cur_sum > constraint.total_sum:
                return False
            if len(cur_values) < len(set(cur_values)):
                return False
        return True

    def is_complete(self):
        """
        :return: True if this board is complete, False otherwise
        """
        # did we visit all the tiles?
        for tile in self.tiles.values():
            if not tile.is_visited():
                return False

        # did we fill all the constraints?
        for constraint in self.constraints.values():
            cur_sum = 0
            for tile_index in constraint.get_locations():
                tile = self.get_tile(tile_index[X_INDEX], tile_index[Y_INDEX])
                cur_sum += tile.get_value()
            if cur_sum != constraint.get_total_sum():
                return False
        return True

    def update_constraints_with_two(self):
        for constraint in self.constraints.values():
            const_sum = constraint.get_total_sum()
            if constraint.get_num_tiles() == 2:
                first_index = constraint.get_locations()[0]
                first = self.get_tile(first_index[X_INDEX], first_index[Y_INDEX])
                second_index = constraint.get_locations()[1]
                second = self.get_tile(second_index[X_INDEX], second_index[Y_INDEX])

                if first.is_visited() or second.is_visited():
                    continue

                first_poss = first.possible_values()
                second_poss = second.possible_values()
                for number in first_poss:
                    if const_sum - number not in second_poss:
                        first.remove_value_from_possible(number)
                for number in second_poss:
                    if const_sum - number not in first_poss:
                        second.remove_value_from_possible(number)

    def update_constraints(self):
        self.update_constraints_with_two()
        for constraint in self.constraints.values():
            possible_values = set()
            for tile_index in constraint.get_locations():
                tile = self.get_tile(tile_index[X_INDEX], tile_index[Y_INDEX])
                for number in tile.possible_values():
                    possible_values.add(number)
            for option in constraint.get_possible_placements():
                for number in option:
                    if number not in possible_values:
                        constraint.remove_placement(option)
