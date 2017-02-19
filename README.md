# IPython notebooks to YAML


[![Build Status](https://travis-ci.org/prabhuramachandran/ipyaml.svg?branch=master)](https://travis-ci.org/prabhuramachandran/ipyaml)
[![codecov](https://codecov.io/gh/prabhuramachandran/ipyaml/branch/master/graph/badge.svg)](https://codecov.io/gh/prabhuramachandran/ipyaml)



This simple project allows one to convert IPython notebooks to easily editable
YAML files. This is very similar to the
[notedown](http://github.com/aaren/notedown) and
[ipymd](http://github.com/rossant/ipymd) packages but supports all IPython
outputs as well.

The advantage of using this package is that you get complete compatibility
with IPython notebooks and the ability to edit the files in any text editor.

The format is YAML so it is not as pretty as Markdown but is a reasonable
compromise.

## Installation

Install the package as follows:

    $ pip install ipyaml


## Usage

Run the command `ipyaml` to convert between the two formats:


    $ ipyaml notebook.ipynb notebook.ipyml  # or notebook.ipyaml

    $ ipyaml notebook.ipyml notebook.ipynb


If you want jupyter to automatically load and save the `.ipyml` files. Add the
following to your `jupyter_notebook_config.py`:

    c.NotebookApp.contents_manager_class = 'ipyaml.api.YAMLContentsManager'


The `jupyter_notebook_config.py` can be found by running:

    $ jupyter --config-dir

If you don't see a `jupyter_notebook_config.py` you can do this:

    $ jupyter notebook --generate-config
