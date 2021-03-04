"""
Grab stuff from an ipython/jupyter notebook.
"""
import os
import json
from operator import itemgetter

from lined import Line, iterize
from py2store import LocalBinaryStore
from grub import SearchStore


def get_byte_contents(src):
    if isinstance(src, str):
        if os.path.isfile(src):
            with open(src, 'rb') as fp:
                return fp.read()
    elif hasattr(src, 'read'):
        return src.read()
    return src


get_ipynb_cells = Line(get_byte_contents, json.loads, itemgetter('cells'))
get_ipynb_cells_source = Line(get_ipynb_cells,
                              iterize(itemgetter('source')), iterize(''.join), list)


def text_for_cell(cell):
    if cell['cell_type'] == 'markdown':
        return ''.join((f"# {line}") for line in cell['source'])  # comment out lines
    else:
        return ''.join(cell['source'])


cell_seperator = '\n\n#%% ############################\n\n'
get_ipynb_cells_full_text = Line(get_ipynb_cells,
                                 iterize(text_for_cell),
                                 cell_seperator.join)


class SearchNotebooks(SearchStore):
    def __init__(self, src, n_neighbors: int = 10, max_levels=None):
        assert os.path.isdir(src), f"Right now, only a directory can be used as a source"
        store = LocalBinaryStore(src + '{}.ipynb', max_levels=None)
        super().__init__(store, n_neighbors=n_neighbors)

    def search_notebook(self, k):
        return SearchStore({(f"{k}", i): x for i, x in enumerate(get_ipynb_cells_source(self.store[k]))})
