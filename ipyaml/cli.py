from __future__ import print_function
import argparse

import nbformat
import yaml

from ipyaml.convert import nb_to_yaml, yaml_to_nb


def read_nb(fname):
    return nbformat.read(fname, 4)


def read_yaml(fname):
    data = yaml.load(open(fname))
    return yaml_to_nb(data)


def main(args=None):
    parser = argparse.ArgumentParser(
        "Convert Jupyter notebooks to YAML and vice-versa."
    )
    parser.add_argument("input", nargs=1, help="Input file (ipynb or yaml)")
    parser.add_argument("output", nargs=1, help="Output file")
    args = parser.parse_args(args)
    input = args.input[0]
    output = args.output[0]
    YAML_EXT = ('.yaml', '.yml', '.ipyml', '.ipyaml')
    if input.endswith(YAML_EXT):
        nb = read_yaml(input)
    elif input.endswith('.ipynb'):
        nb = read_nb(input)
    else:
        raise RuntimeError('Unknown input file format, %s' % input)

    if output.endswith(YAML_EXT):
        yml = nb_to_yaml(nb)
        print(yml, file=open(output, 'w'))
    elif output.endswith('.ipynb'):
        nbformat.write(nb, open(output, 'w'))


if __name__ == '__main__':
    main()
