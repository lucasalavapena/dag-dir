
def canvas_to_scale(canvas_size, max_node_size):
    # Note the subtractiom by max_node_size because netgraph.get_sugiyama_layout 
    # does not account the size of the text of the node.
    y_value = canvas_size[1] - 1 - max_node_size
    return (canvas_size[0] - 1, y_value)
