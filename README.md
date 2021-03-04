
# sheet
Tools to manipulate ipython (jupyter) notebooks


To install:	```pip install sheet```


# Examples

```python
from sheet import get_ipynb_cells, get_ipynb_cells_source
filepath = '/Users/Thor.Whalen/Downloads/stream2py_pyaudio_and_dpp_struct_ideas.ipynb'

cells = get_ipynb_cells(filepath)
assert type(cells), type(cells[0]) == (list, dict)

cells = get_ipynb_cells_source(filepath)
assert type(cells), type(cells[0]) == (list, str)
```


```python
from sheet import get_ipynb_cells_full_text
notebook_text = get_ipynb_cells_full_text(filepath)
print(notebook_text)
```

```python
from sheet import SearchNotebooks

search = SearchNotebooks('~/my_notebooks_folder', max_levels=0)  # enter max_levels=None for full recursive
search('bayesian')
```

    array(['Spyn 01 - Potentials.ipynb',
           'Bayes 01 - Potentials-Only explanation.ipynb', 'taped.ipynb',
           'separation of concerns - how py2store does it.ipynb',
           'equate.ipynb', 'peruse.ipynb',
           'hum, taped, lined -- feeding audio to a pipeline.ipynb',
           'owner.ipynb', 'best of 2020.ipynb',
           'Bayes 02 - Potentials - And drug data example.ipynb'],
          dtype=object)

Okay, we have a list of notebooks that match our query 
(i.e. the highest average alignment to our query -- not just keyword matching!), 
but what cells in particular have the highest relevance?

Well, we can now peruse our notebook at that level, with a notebook cells searcher.
(Note: You can combine both to make a cell-level searcher from the folder level.)

```python
ss = search.search_notebook('Spyn 01 - Potentials.ipynb')
ss('bayesian')
```

    array([['Spyn 01 - Potentials.ipynb', 6],
           ['Spyn 01 - Potentials.ipynb', 2],
           ['Spyn 01 - Potentials.ipynb', 71],
           ['Spyn 01 - Potentials.ipynb', 88],
           ['Spyn 01 - Potentials.ipynb', 91],
           ['Spyn 01 - Potentials.ipynb', 84],
           ['Spyn 01 - Potentials.ipynb', 85],
           ['Spyn 01 - Potentials.ipynb', 86],
           ['Spyn 01 - Potentials.ipynb', 87],
           ['Spyn 01 - Potentials.ipynb', 82]], dtype=object)
           
```python
ss['Spyn 01 - Potentials.ipynb', 6]
```

    '# Potentials - A key data structure to Discrete Bayesian Inference'


```python
ss['Spyn 01 - Potentials.ipynb', 87]
```

    '### Making a few potentials from pts data'

