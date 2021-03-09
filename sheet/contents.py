import json
import os
from operator import itemgetter

from grub import SearchStore, camelcase_and_underscore_tokenizer
from lined import Line, iterize
from py2store import LocalBinaryStore


def default_src():
    from sheet.current_notebook import get_path_of_current_notebook
    return get_path_of_current_notebook()


def get_byte_contents(src=None):
    if src is None:
        src = default_src()
    if isinstance(src, str):
        if os.path.isfile(src):
            with open(src, "rb") as fp:
                return fp.read()
    elif hasattr(src, "read"):
        return src.read()
    return src


get_ipynb_cells = Line(get_byte_contents, json.loads, itemgetter("cells"))
get_ipynb_cells_source = Line(
    get_ipynb_cells, iterize(itemgetter("source")), iterize("".join), list
)


def text_for_cell(cell):
    if cell["cell_type"] == "markdown":
        return "".join(
            (f"# {line}") for line in cell["source"]
        )  # comment out lines
    else:
        return "".join(cell["source"])


cell_seperator = "\n\n#%% ############################\n\n"
get_ipynb_cells_full_text = Line(
    get_ipynb_cells, iterize(text_for_cell), cell_seperator.join
)


class SingleNotebookSearch(SearchStore):
    """Search the cells of a notebook. Defaults to current notebook (where-ever the instance is created)"""
    def __init__(self, src=None,
                 n_hit_cells: int = 10,
                 tokenizer=camelcase_and_underscore_tokenizer):
        if src is None:
            src = default_src()
        store_to_search = {
            i: x
            for i, x in enumerate(get_ipynb_cells_source(src))
        }
        super().__init__(store=store_to_search, n_neighbors=n_hit_cells, tokenizer=tokenizer)
        self.n_hit_cells = n_hit_cells


class SearchNotebooks(SearchStore):
    """Search notebooks under a directory."""
    def __init__(self,
                 src=None,
                 n_hit_files: int = 10,
                 n_hit_cells: int = 10,
                 *,
                 max_levels=None,
                 tokenizer=camelcase_and_underscore_tokenizer):
        if src is None:
            from sheet.current_notebook import notebook_dir_of_first_server_found
            src = notebook_dir_of_first_server_found()
            print(f"No src was specified, so I'll use: {src}")

        assert os.path.isdir(
            src
        ), f"Right now, only a directory can be used as a source"
        store = LocalBinaryStore(src + "{}.ipynb", max_levels=max_levels)
        super().__init__(store, n_neighbors=n_hit_files, tokenizer=tokenizer)
        self.n_hit_files = n_hit_files
        self.n_hit_cells = n_hit_cells

    def search_notebook(self, k):
        return SearchStore(
            {
                (f"{k}", i): x
                for i, x in enumerate(get_ipynb_cells_source(self.store[k]))
            },
            n_neighbors=self.n_hit_cells
        )
