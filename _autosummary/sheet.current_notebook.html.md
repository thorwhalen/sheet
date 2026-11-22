# sheet.current_notebook

Old code that was used to do things like get notebook lists, urls/rootdir thereof, kernel ids

### Functions

| [`first_server_found`](#sheet.current_notebook.first_server_found)([server_filt])                       | Get the server specs (a dict) of the first server found (that matches the filter, if given).     |
|----------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| [`get_path_of_current_notebook`](#sheet.current_notebook.get_path_of_current_notebook)([kernel_id, ...])          | Get the local filepath of the current notebook, from within notebook.                            |
| [`notebook_dir_of_first_server_found`](#sheet.current_notebook.notebook_dir_of_first_server_found)([server_filt])       | Notebook rootdir of the firtt server found (that matches the filter, if given)                   |
| [`url_token_and_notebook_dir_of_first_server_found`](#sheet.current_notebook.url_token_and_notebook_dir_of_first_server_found)([...]) | Get the (url, token, notebook_dir) of the first server found (that matches the filter, if given) |

### sheet.current_notebook.first_server_found(server_filt=None)

Get the server specs (a dict) of the first server found (that matches the filter, if given).

### sheet.current_notebook.get_path_of_current_notebook(kernel_id=None, server_filt=None)

Get the local filepath of the current notebook, from within notebook.

### sheet.current_notebook.notebook_dir_of_first_server_found(server_filt=None)

Notebook rootdir of the firtt server found (that matches the filter, if given)

### sheet.current_notebook.url_token_and_notebook_dir_of_first_server_found(server_filt=None)

Get the (url, token, notebook_dir) of the first server found (that matches the filter, if given)
