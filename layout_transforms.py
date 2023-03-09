from collections import defaultdict
from operator import itemgetter

from ascii_canvas import Coord2D

def layout_account_for_text(layout_dict, inplace=False):
    res = layout_dict if inplace else {k: v for k, v in layout_dict.items()}  
    group_by_x = defaultdict(list)

    for k, (x, y) in res.items():
        group_by_x[x].append((y, k))

    for x in group_by_x:
        group_by_x[x].sort(key=itemgetter(0))
        # figure out if there is a better in built group by x
        offset = 0
        for (y_coord, name) in group_by_x[x]:
            # to deal with large numbers, etc
            res[name] = Coord2D(x, y_coord + offset)
            offset_space = len(str(name))
            offset += offset_space

    return None if inplace else res


# if memory is important
def discretise_layout_generator(layout_dict):
    for node_id, (x, y) in layout_dict.items():
        yield node_id, Coord2D(x=round(x), y=round(y))


def discretise_layout_to_coord(layout_dict, inplace: bool = False):
    res = layout_dict if inplace else {k: v for k, v in layout_dict.items()}   
    for k, (x, y) in res.items():
        res[k] = Coord2D(x=int(x), y=int(y))

    # None convention for inplace
    return None if inplace else res


def layout_shift_origin(layout, inplace: bool = False):
    min_x = min(x for x, y in layout.values())
    min_y = min(y for x, y in layout.values())
    min_coord = (min_x, min_y)

    # No shift required
    if min_x >= 0 and min_y >= 0:
        if inplace:
            return layout, min_coord
        return {k: v for k, v in layout.items()}, min_coord

    offset = Coord2D(max(-min_x, 0), max(-min_y, 0))

    new_min_x = max(min_x, 0)
    new_min_y = max(min_y, 0)

    offset_min_coord = (new_min_x, new_min_y)

    # Make spacing on the other side okay?
    if not inplace:
        return {k: v + offset for k, v in layout.items()}, offset_min_coord

    for k, v in layout.items():
        layout[k] += offset

    return layout, offset_min_coord

def resize_canvas_horizontally(layout, canvas, min_y: int):
    max_y_vertex, (_, max_y) = max(layout.items(), key=lambda x: x[1].y)

    # canvas.no_cols + (max_y - canvas.no_cols) + min_y + 1 + len(max_y_vertex) simplies to what is below
    # min_y is needed for equal spacing on both sides
    desired_no_cols = max_y + min_y + len(max_y_vertex) + 2

    # resize canvas in y direction
    if canvas.no_cols < desired_no_cols:
        canvas.resize(no_cols=desired_no_cols)

    return layout, canvas


def transform_layout(layout_dict, canvas):
    res = discretise_layout_to_coord(layout_dict)
    res = layout_account_for_text(res)
    res, (_, min_y) = layout_shift_origin(res)
    res, canvas = resize_canvas_horizontally(res, canvas, min_y)

    return res, canvas