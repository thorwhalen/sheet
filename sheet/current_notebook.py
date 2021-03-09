"""
Old code that was used to do things like get notebook lists, urls/rootdir thereof, kernel ids
"""
import os
import subprocess
from urllib.request import urlopen
from urllib.parse import urljoin
import json

from ipykernel.connect import get_connection_file
from notebook import notebookapp

from lined import Line, iterize, mk_filter


def _jupyter_notebook_list():
    """Runs the jupyter notebook list command and returns the output string"""
    process = subprocess.run(
        "jupyter notebook list".split(), stdout=subprocess.PIPE, text=True
    )
    if process.returncode == 0:
        return process.stdout
    else:
        raise SystemError(
            f"Running 'jupyter notebook list' didn't lead to a healthy return code: process is: {process}"
        )


jupyter_notebook_list_lines = Line(
    _jupyter_notebook_list,
    lambda x: x.split("\n"),
    mk_filter(lambda line: line.startswith("http")),
)
jupyter_notebook_list_lines.__doc__ = "Runs the jupyter notebook list command and returns a list extracted from the parsed string"

jupyter_notebooks_url_and_rootdir = Line(
    jupyter_notebook_list_lines,
    iterize(lambda line: tuple(line.split(" :: "))),
)
jupyter_notebooks_url_and_rootdir.__doc__ = (
    "Get (url, rootdir) pairs of currently running notebooks."
)

get_current_kernel_id = Line(
    get_connection_file,
    os.path.basename,
    lambda filename: filename.split("-", 1)[1].split(".")[0],
)
get_current_kernel_id.__doc__ = "Get current kernel id"

NotebookPathNotFound = object()


def _get_path_of_notebook(url, token=None, kernel_id=None):
    """Get the local filepath of the notebook pointed to by kernel_id (for the server defined by url and token)"""
    if "/api/sessions" not in url:
        url = urljoin(url, "/api/sessions")
    if token:  # None or ''
        url = url + f"?token={token}"

    with urlopen(url) as con:
        sessions = json.load(con)
        for sess in sessions:
            if sess["kernel"]["id"] == kernel_id:
                if "path" in sess:
                    return sess["path"]
                elif "notebook" in sess and "path" in sess["notebook"]:
                    return sess["notebook"]["path"]
                else:
                    raise ValueError(
                        f"Couldn't find a path in session info {sess}"
                    )
    return NotebookPathNotFound  # if no found


def first_server_found(server_filt=None):
    """Get the server specs (a dict) of the first server found (that matches the filter, if given)."""
    server = next(filter(server_filt, notebookapp.list_running_servers()), None)
    if server:
        return server
    else:
        raise ValueError("No notebook servers found.")


def url_token_and_notebook_dir_of_first_server_found(server_filt=None):
    """Get the (url, token, notebook_dir) of the first server found (that matches the filter, if given)"""
    server = first_server_found(server_filt=server_filt)
    url, token, notebook_dir = (
        server["url"],
        server.get("token", None),
        server["notebook_dir"],
    )
    return url, token, notebook_dir


def notebook_dir_of_first_server_found(server_filt=None):
    """Notebook rootdir of the firtt server found (that matches the filter, if given)"""
    _, _, notebook_dir = url_token_and_notebook_dir_of_first_server_found(server_filt=server_filt)
    return notebook_dir


def get_path_of_current_notebook(kernel_id=None, server_filt=None):
    """Get the local filepath of the current notebook, from within notebook."""
    url, token, notebook_dir = url_token_and_notebook_dir_of_first_server_found(server_filt=server_filt)
    if kernel_id is None:
        kernel_id = get_current_kernel_id()
    notebook_path = _get_path_of_notebook(url, token, kernel_id)
    if notebook_path is not NotebookPathNotFound:
        return os.path.join(notebook_dir, notebook_path)
    else:
        raise RuntimeError(
            f"No notebook path could be found for: {url}, {notebook_dir}, {token}"
        )
