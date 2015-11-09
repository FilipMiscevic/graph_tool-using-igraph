graph_tool using igraph
=======================

Python module to provide `graph_tool` functionality using only `igraph`.

Specifically, it extends the `igraph` Graph class, allowing it to be interfaced in the same way as the `graph_tool` Graph class. The intended purpose of this tool is to permit code written using `graph_tool` to be executed where `graph_tool` itself may not be possible or is too involved to install, i.e. on Windows machines or servers lacking the necessary libraries to support `graph_tool`. Like `graph_tool`, `igraph` is also implemented in `C`, so performance will approach but is almost certainly worse than `graph_tool` (https://graph-tool.skewed.de/performance).

`graph_tool` functions already shared by `igraph` Graph class:
- `copy`

`graph_tool` functions currently implemented and tested:
- `new_vertex_property`
- `new_vp`
- `new_edge_property`
- `new_ep`
- `new_graph_property`
- `new_gp`
- `set_directed`
- `reindex_edges`
- `add_edge` *vertices may be Vertex objects or their indices
- `add_vertex`
- `num_edges`
- `num_vertices`
- `vertices`
- `edges`
- `vertex` *add_missing=True adds the number of vertices up to i
- `edge` *add_missing=True adds the edge if it does not exist
- `remove_vertex`
- `remove_edge`

`graph_tool` functions currently implemented but not extensively tested:
- `set_filters`
- `set_vertex_filter`
- `set_edge_filter`
- `purge_vertices`
- `purge_edges`
- `clear_filters`

Known issues:
- Plotting in `igraph` depends on the `pycairo` library, which means that users are forced to use it for any graphing functionality.
- `clear_filters` implementation returns the original Graph object

Instructions for installation:
Download the script to the working directory for your python code.
Replace the import code for `graph_tool` with `from graph_tool_igraph import *` or `import graph_tool_igraph as graph_tool` as applicable. Alternatively, you can use a `try/except` block to try and import `graph_tool` first and only import this tool on an `ImportError`.