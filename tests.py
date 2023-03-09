import unittest
import tempfile
from pathlib import Path
import os

from ascii_canvas import ASCIICanvas, Coord2D
from dag_dir import dag_dir


class TestASCIICanvas(unittest.TestCase):
    def test__setitem__(self):
        canvas = ASCIICanvas(19, 19)
        canvas[(7, 7)] = "A"
        self.assertEqual(canvas._canvas[7][7], "A")

        canvas[(0, 0)] = "B"
        self.assertEqual(canvas._canvas[0][0], "B")

        canvas[(18, 18)] = "C"
        self.assertEqual(canvas._canvas[18][18], "C")

        # TODO: try values outside bound to test exception


    def test__getitem__(self):
        canvas = ASCIICanvas(10, 10)
        self.assertEqual(canvas[(0, 0)], canvas._canvas[0][0])

        canvas = ASCIICanvas(19, 19)
        self.assertEqual(canvas[(7, 7)], canvas._canvas[7][7])

        canvas = ASCIICanvas(19, 19)
        canvas._canvas[7][7] = "K"
        self.assertEqual(canvas[(7, 7)], canvas._canvas[7][7])

        # TODO: try values outside bound to test exception

    def test_modify_coordinate_value(self):
        c = ASCIICanvas(15, 15)

        c.modify_coordinate(Coord2D(7, 6), 19)
        self.assertEqual(c._canvas[7][6], str(19))

        c.modify_coordinate(Coord2D(0, 0), 3)
        self.assertEqual(c._canvas[0][0], str(3))

        # test it does not overwrite important information
        before = c._canvas[7][6]
        c.modify_coordinate(Coord2D(7, 6), "*")
        self.assertEqual(c._canvas[7][6], before)
        self.assertNotEqual(c._canvas[7][6], "*")

    def test_modify_coordinate_str(self):
        c = ASCIICanvas(15, 15)

        text1 = "19"
        c.modify_coordinate(Coord2D(7, 6), text1)
        self.assertEqual(c._canvas[7][6:6 + len(text1)], list(text1))

        text2 = "Lorem ipsum"
        c.modify_coordinate(Coord2D(8, 1), text2)
        self.assertEqual(c._canvas[8][1:1 + len(text2)], list(text2))

    def test_modify_coordinate_assertions(self):
        pass


class TestDAGDIR(unittest.TestCase):
    def test_dag_dir(self):
        """
        Testing set up
        [X@X tmpdntrwq94]$ tree
        .
        ├── a.txt
        └── subdir
            ├── ptr.txt -> /tmp/tmpdntrwq94/a.txt
            └── b.text

        TODO surpress stdout?
        """
        # to start from a new clean line
        print()
        with tempfile.TemporaryDirectory() as td:
            file_to_sym_link = Path(td) / "a.txt"
            # create file
            open(file_to_sym_link, 'a').close()

            subdir = Path(td) / "subdir" 
            subdir.mkdir()

            # create normal file
            open(subdir / "b.txt", 'a').close()

            # create symlink
            os.symlink(file_to_sym_link, subdir / "ptr.txt")

            # create structure
            dag_dir(td, canvas_size=(20, 50))


if __name__ == '__main__':
    unittest.main()