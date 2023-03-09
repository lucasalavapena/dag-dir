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

    # TODO: Combine the below two functions
    def create_relative_vertex(dir_path, file_name):
        dest_abs = Path(dir_path) / file_name

        # In the case that you have a symbolic link pointing further down
        # in the directory tree, the vertex would already be created
        if str(dest_abs) in nodes:
            return nodes[str(dest_abs)]

        dest_rel = dest_abs.relative_to(curr_dir)

        nodes[str(dest_abs)] = Vertex(abs_path=dest_abs, rel_path=dest_rel)

        return nodes[str(dest_abs)]

    def create_symbolic_vertex(resolved_path):
        dest_abs = Path(resolved_path)

        if str(dest_abs) in nodes:
            return nodes[str(dest_abs)]

        # in case it points further down
        try:
            dest_rel = dest_abs.relative_to(curr_dir)
            nodes[str(dest_abs)] = Vertex(abs_path=dest_abs, rel_path=dest_rel, is_sym=True)
        except ValueError:
            # In case symlink is outside of the directory dag show would be called on
            #  Path.relative_to raises a ValueError if dest_abs is not a sub directory of curr_dir
            nodes[str(dest_abs)] = Vertex(abs_path=dest_abs, is_sym=True)

        return nodes[str(dest_abs)]

    for (dir_path, dir_names, file_names) in os.walk(path, followlinks=True):
        parent_vertex = nodes[dir_path]

        for file_name in file_names + dir_names:
            
            dest_vertex = create_relative_vertex(dir_path, file_name)
            edges.append((parent_vertex, dest_vertex))

            if os.path.islink(dest_vertex.abs_path):
                # In the case of a cycle os.path.realpath appears to resolve to the input path
                # So it likely we are getting a DAG,
                # TODO but this need to be tested thorougly
                resolved_path = os.path.realpath(dest_vertex.abs_path)

                symbolic_dest_vertex = create_symbolic_vertex(resolved_path)
                edges.append((dest_vertex, symbolic_dest_vertex))

    return edges, nodes