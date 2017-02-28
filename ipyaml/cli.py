from __future__ import print_function
import argparse
import os

import nbformat
import yaml

from ipyaml.convert import nb_to_yaml, yaml_to_nb


def read_nb(fname):
    return nbformat.read(fname, 4)


def read_yaml(fname):
    data = yaml.safe_load(open(fname))
    return yaml_to_nb(data)


def file_type(fname):
    _, ext = os.path.splitext(fname)
    YAML_EXT = ('.yaml', '.yml', '.ipyml', '.ipyaml')
    if ext in YAML_EXT:
        return 'yaml'
    elif ext in ['.ipynb']:
        return 'notebook'
    else:
        return None


def main(args=None):
    parser = argparse.ArgumentParser(
        "Convert Jupyter notebooks to YAML and vice-versa."
    )
    parser.add_argument("input", nargs=1, help="Input file (ipynb or yaml)")
    parser.add_argument("output", nargs=1, help="Output file")
    parser.add_argument(
        '--no-output', dest='no_output',
        action='store_true', default=False,
        help='Do not store output in YAML file. (defaults to False)'
    )
    args = parser.parse_args(args)
    input = args.input[0]
    output = args.output[0]
    ift = file_type(input)
    if ift == 'yaml':
        nb = read_yaml(input)
    elif ift == 'notebook':
        nb = read_nb(input)
    else:
        parser.print_usage()
        message = 'ERROR: Unknown input file format, %s\n' % input
        parser.exit(1, message)

    oft = file_type(output)
    if oft == 'yaml':
        yml = nb_to_yaml(nb, not args.no_output)
        print(yml, file=open(output, 'w'))
    elif oft == 'notebook':
        nbformat.write(nb, open(output, 'w'))
    else:
        parser.print_usage()
        message = 'ERROR: Unknown output file format, %s\n' % output
        parser.exit(1, message)


if __name__ == '__main__':
    main()
