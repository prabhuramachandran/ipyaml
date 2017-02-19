import os

import nbformat

from tornado import web

try:
    from notebook.services.contents.filemanager import FileContentsManager
except ImportError:
    from IPython.html.services.contents.filemanager import FileContentsManager

from .cli import file_type, read_nb, read_yaml, nb_to_yaml


class YAMLContentsManager(FileContentsManager):
    """Subclass the IPython file manager to use YAML as the storage format for
    notebooks.

    Intercepts the notebook before read and write to determine the storage
    format from the file extension (_read_notebook and _save_notebook).

    We have to override the get method to treat .ipyml as a notebook file
    extension. This is the only change to that method.

    To use, add the following line to jupyter_notebook_config.py:

      c.NotebookApp.contents_manager_class = 'ipyaml.api.YAMLContentsManager'

    With this, yaml files can be opened by Jupyter.
    """

    def _read_notebook(self, os_path, as_version=4):
        """Read a notebook from an os path."""
        try:
            if file_type(os_path) == 'notebook':
                return read_nb(os_path)
            elif file_type(os_path) == 'yaml':
                return read_yaml(os_path)
        except Exception as e:
            raise web.HTTPError(
                400,
                u"Unreadable Notebook: %s %r" % (os_path, e),
            )

    def _save_notebook(self, os_path, nb):
        """Save a notebook to an os_path."""
        with self.atomic_writing(os_path, encoding='utf-8') as f:
            if file_type(os_path) == 'notebook':
                nbformat.write(nb, f, version=nbformat.NO_CONVERT)
            elif file_type(os_path) == 'yaml':
                yml = nb_to_yaml(nb)
                f.write(yml)

    def get(self, path, content=True, type=None, format=None):
        """ Takes a path for an entity and returns its model

        Parameters
        ----------
        path : str
            the API path that describes the relative path for the target
        content : bool
            Whether to include the contents in the reply
        type : str, optional
            The requested type - 'file', 'notebook', or 'directory'.
            Will raise HTTPError 400 if the content doesn't match.
        format : str, optional
            The requested format for file contents. 'text' or 'base64'.
            Ignored if this returns a notebook or directory model.

        Returns
        -------
        model : dict
            the contents model. If content=True, returns the contents
            of the file or directory as well.
        """
        path = path.strip('/')

        if not self.exists(path):
            raise web.HTTPError(404, u'No such file or directory: %s' % path)

        os_path = self._get_os_path(path)
        extension = ('.ipynb', '.ipyml')

        if os.path.isdir(os_path):
            if type not in (None, 'directory'):
                raise web.HTTPError(400,
                                    u'%s is a directory, not a %s' % (path,
                                                                      type),
                                    reason='bad type')
            model = self._dir_model(path, content=content)

        elif type == 'notebook' or (type is None and path.endswith(extension)):
            model = self._notebook_model(path, content=content)
        else:
            if type == 'directory':
                raise web.HTTPError(400,
                                    u'%s is not a directory' % path,
                                    reason='bad type')
            model = self._file_model(path, content=content, format=format)
        return model
