import argparse
from collections import defaultdict
from pathlib import Path
from typing import Optional, NamedTuple, Tuple
import os

import netgraph

from ascii_canvas import ASCIICanvas, Coord2D
from utils import canvas_to_scale
from layout_transforms import transform_layout
from graph import get_edges_vertices


def dag_dir(path: Path, *, canvas_size: Tuple[int, int] = (30, 80), max_depth = None):
    if max_depth is not None:
        assert max_depth > 0, "maximum depth argument has to be positive"

    path = os.path.abspath(path)

    if not os.path.exists(path):
        msg = f"Ensure that the enter path exists, it was resolved as {path=}"
        raise FileNotFoundError(msg)

    canvas = ASCIICanvas(*canvas_size)
    edges, vertices_dict = get_edges_vertices(path, max_depth)

    max_node_size = max(len(v) for v in vertices_dict.values())

    # calculate padding based on longest case
    layout_dict = netgraph.get_sugiyama_layout(edges, origin=(0, 0), scale=canvas_to_scale(canvas_size, max_node_size), pad_by=0.05, total_iterations=5)
    layout_dict, canvas = transform_layout(layout_dict, canvas)

    for node_id, coord in layout_dict.items():
        canvas.modify_coordinate(coord, node_id, is_sym=node_id.is_sym)
    
    for src, dest in edges:
        canvas.add_line_between(layout_dict[src], layout_dict[dest], len(src),len(dest), is_sym=src.is_sym)
    
    canvas.draw()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Show DAG of file path, includes symlinks."
    )
    parser.add_argument('path', type=str)
    parser.add_argument('-cs', '--canvas-size', type=int, nargs=2)
    parser.add_argument('-md', '--max-depth', type=int, default=None)

    opt = parser.parse_args()

    if opt.canvas_size:
        dag_dir(opt.path, canvas_size=tuple(opt.canvas_size), max_depth=opt.max_depth)
    else:
        dag_dir(opt.path, max_depth=opt.max_depth)
