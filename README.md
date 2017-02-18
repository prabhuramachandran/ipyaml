# IPython notebooks to YAML

This simple project allows one to convert IPython notebooks to easily editable
YAML files. This is very similar to the
[ipymd][http://github.com/rossant/ipymd] package but supports all IPython
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


    $ ipyaml notebook.ipynb notebook.ipyaml  # or notebook.yaml

    $ ipyaml notebook.ipyaml notebook.ipynb
