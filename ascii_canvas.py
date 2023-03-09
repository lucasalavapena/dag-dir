from typing import NamedTuple, Iterable, SupportsFloat
import os

def sign(x: SupportsFloat):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    return -1

class Coord2D(NamedTuple):
    x: int
    y: int

    def __add__(self, other):
        if isinstance(other, Coord2D):
            return Coord2D(self.x + other.x, self.y + other.y)
        else:
            msg = f"__add__ only works with other Coord2D, not with {type(other)}"
            raise TypeError(msg)


class ASCIICanvas:

    EMPTY_CHAR = " "
    LINE_CHAR = "*"

    def __init__(self, no_rows: int, no_cols: int):
        # assertion that values are positive
        self._no_rows = no_rows 
        self._no_cols = no_cols 
        
        self.resize()

    def __repr__(self):
        return f"ASCIICanvas(no_rows={self.no_rows=}, no_cols={self.no_cols=})"

    def __str__(self):
        rows = map("".join, self._canvas)
        return os.linesep.join(rows)
    
    def __getitem__(self, key):
        # TODO raise custom error messages for Index Error
        if isinstance(key, tuple):
            assert len(key) == 2, "Key should be an instance of a tuple with of length 2"
            return self._canvas[key[0]][key[1]]
        else:
            raise TypeError("Key has to be an instance of a tuple")

    def __setitem__(self, key, value):
        # TODO raise custom error messages for Index Error
        if isinstance(key, tuple):
            assert len(key) == 2, "Key should be an instance of a tuple with of length 2"
            self._canvas[key[0]][key[1]] = value
        else:
            raise TypeError("Key has to be an instance of a tuple")

    def draw(self):
        print(self)

    @property
    def no_rows(self):
        return self._no_rows

    @property
    def no_cols(self):
        return self._no_cols

    @no_cols.setter
    def no_cols(self, value: int):
        self._no_cols = value

    def resize(self, *, no_rows: int = None, no_cols: int = None):
        # TODO is it okay to mix and max _norows stuff
        if no_rows:
            self.no_rows = no_rows
        if no_cols:
            self.no_cols = no_cols
        self._canvas = [[ASCIICanvas.EMPTY_CHAR] * self.no_cols for r in range(self.no_rows)]


    def should_overdraw(self, coord: tuple, desired_char: str) -> bool:
        curr_char = self[coord]
        is_empty = curr_char == ASCIICanvas.EMPTY_CHAR
        return is_empty or (curr_char == ASCIICanvas.LINE_CHAR and desired_char != ASCIICanvas.LINE_CHAR)

    def modify_coordinate(self, coord: Coord2D, value: str):
        # TODO raise custom error messages for Index Error
        if isinstance(value, Iterable):
            for i, v in enumerate(value):
                if self.should_overdraw((coord.x, coord.y + i), v):
                    self._canvas[coord.x][coord.y + i] = v
        else:
            value = str(value)
            if self.should_overdraw(coord, value):
                self._canvas[coord.x][coord.y] = value


    # inclusive??
    def add_line_between(self, src_coord: Coord2D, dest_coord: Coord2D, src_size: int, dest_size: int, *, x_padding: int = 0, y_padding: int = 1):
        # TODO make padding both sides equally

        # easier to deal with horizontal lines separately
        if src_coord.x == dest_coord.x:
            dy = sign(dest_coord.y-src_coord.y)

            # in case nodes are very close and for loop is skipped
            new_y = src_coord.y
            # note the -2 in the step argument of range is -1 twice, once for getting the correct index (dest_size)
            # and then second for padding
            for new_y in range(src_coord.y + dy * y_padding, dest_coord.y - dy * (y_padding + dest_size), dy):
                self.modify_coordinate(Coord2D(src_coord.x, new_y), ASCIICanvas.LINE_CHAR)
                        
            self.modify_coordinate(Coord2D(src_coord.x, new_y + dy), ">" if dy > 0 else "<")
        else:
            src_mid_coord = src_coord + Coord2D(0, src_size // 2)
            dest_mid_coord = dest_coord + Coord2D(0, dest_size // 2)

            gradient = (dest_mid_coord.y - src_mid_coord.y) / (dest_mid_coord.x - src_mid_coord.x)
            y_intercept = src_mid_coord.y - gradient * src_mid_coord.x
            dx = sign(dest_mid_coord.x - src_mid_coord.x)

            # TODO solve this more nicely, in case nodes are very close so for loop is skipped
            new_x = src_mid_coord.x
            new_y = src_mid_coord.y

            for new_x in range(src_mid_coord.x + dx * (x_padding + 1), dest_mid_coord.x - dx * (x_padding + 1), dx):
                new_y = round(y_intercept + gradient * new_x)
                self.modify_coordinate(Coord2D(new_x, new_y), ASCIICanvas.LINE_CHAR)

            arrow_x = (new_x + dest_mid_coord.x) // 2
            arrow_y = (new_y + dest_mid_coord.y) // 2

            self.modify_coordinate(Coord2D(arrow_x, arrow_y), "∨" if dx > 0 else "^")


if __name__ == "__main__":
    canvas_size = (10, 20)
    canvas = ASCIICanvas(*canvas_size)
