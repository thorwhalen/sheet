# sheet.contents

Read the cells of ipynb notebooks and search them (one notebook, or a directory of them).

### Functions

| `default_src`()            |    |
|----------------------------|----|
| `get_byte_contents`([src]) |    |
| `text_for_cell`(cell)      |    |

### Classes

| [`SearchNotebooks`](#sheet.contents.SearchNotebooks)([src, n_hit_files, ...])      | Search notebooks under a directory.   |
|------------------------------------------------------------------------------------------------|---------------------------------------|
| [`SingleNotebookSearch`](#sheet.contents.SingleNotebookSearch)([src, n_hit_cells, ...]) | Search the cells of a notebook.       |

### *class* sheet.contents.SearchNotebooks(src=None, n_hit_files=10, n_hit_cells=10, \*, max_levels=None, tokenizer=<function camelcase_and_underscore_tokenizer>)

Bases: `SearchStore`

Search notebooks under a directory.

### *class* sheet.contents.SingleNotebookSearch(src=None, n_hit_cells=10, tokenizer=<function camelcase_and_underscore_tokenizer>)

Bases: `SearchStore`

Search the cells of a notebook. Defaults to current notebook (where-ever the instance is created)
