from pathlib import Path
from typing import NamedTuple, Optional
import os

class Vertex(NamedTuple):
    abs_path: Path
    rel_path: Optional[Path] = None
    is_sym: bool = False

    def __str__(self):
        if self.rel_path is not None:
            return str(self.rel_path)
        else:
            return self.abs_path
            
    def __len__(self):
        return len(str(self))

    def __iter__(self):
        if self.rel_path is not None:
            return iter(str(self.rel_path))
        else:
            return iter(str(self.abs_path))
             

def get_edges_vertices(path):
    edges = []
    curr_dir = Path(path)

    nodes = {path: Vertex(abs_path=path)}

    def create_vertex(vertex_path: Path):
        # In the case that you have a symbolic link pointing further down
        # in the directory tree, the vertex would already be created
        key = str(vertex_path)
        if key in nodes:
            return nodes[key]

        dest_rel = vertex_path.relative_to(curr_dir)
        is_sym = os.path.islink(vertex_path)
        try:
            nodes[key] = Vertex(abs_path=vertex_path, rel_path=dest_rel, is_sym=is_sym)
        except ValueError:
            # In case symlink is outside of the directory dag show would be called on
            #  Path.relative_to raises a ValueError if dest_abs is not a sub directory of curr_dir
            nodes[key] = Vertex(abs_path=vertex_path, is_sym=is_sym)

        return nodes[key]

    for (dir_path, dir_names, file_names) in os.walk(path, followlinks=True):
        parent_vertex = nodes[dir_path]

        for file_name in file_names + dir_names:
            dest_vertex = create_vertex(Path(dir_path) / file_name)
            edges.append((parent_vertex, dest_vertex))

            # Symbolic link case
            if dest_vertex.is_sym:
                # In the case of a cycle os.path.realpath appears to resolve to the input path
                # So it likely we are getting a DAG,
                # TODO but this need to be tested thorougly
                resolved_path = Path(os.path.realpath(dest_vertex.abs_path))
                resolved_vertex = create_vertex(resolved_path)
                edges.append((dest_vertex, resolved_vertex))

    return edges, nodes