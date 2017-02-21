try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import yaml

from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
from nbformat.v4.nbbase import NotebookNode


def indent(text, prefix):
    return ''.join(prefix + line for line in text.splitlines(True))


def to_dict(o):
    """Recursively convert NotebookNode instances to dicts.
    """
    if isinstance(o, NotebookNode):
        return dict({k: to_dict(v) for k, v in o.items()})
    elif isinstance(o, (tuple, list)):
        return [to_dict(i) for i in o]
    else:
        return o


def nb_to_yaml(nb, dump_output=True):
    """Given a notebook instance, generate the YAML.
    """
    nb_data = to_dict(nb)
    cells = nb_data.pop('cells')
    out = StringIO()
    out.write('cells:\n\n')
    data = []
    for cell in cells:
        prefix = 2*' '
        cell_type = cell['cell_type']
        out.write(indent('- %s: |\n' % cell_type, prefix))
        code = ''.join(cell['source'])
        prefix = 6*' '
        out.write(indent(code, prefix))
        out.write('\n\n')
        prefix = 4*' '
        if cell_type == 'code' and dump_output:
            index = len(data)
            cell_data = dict(
                outputs=cell['outputs'],
                execution_count=cell['execution_count']
            )
            data.append(cell_data)
            out.write(indent('id: %d\n' % index, prefix))
        md = cell.get('metadata')
        if md:
            out.write(indent('metadata:\n', prefix))
            yml_data = yaml.safe_dump(dict(md), default_flow_style=False)
            out.write(indent(yml_data, prefix + '  '))
        out.write('\n')

    out.write('# ' + '-'*75 + '\n')
    out.write(yaml.safe_dump(nb_data, default_flow_style=False))
    if dump_output:
        out.write('\n# ' + '-'*75 + '\n')
        out.write('data:\n')
        prefix = 2*' '
        data = yaml.safe_dump(data, default_flow_style=True)
        out.write(indent(data, prefix))
    out.seek(0)
    return out.read()


def yaml_to_nb(data):
    """Given the YAML data, construct a notebook.
    """
    yaml_data = dict(data)
    cell_info = yaml_data.pop('cells')
    cell_data = yaml_data.pop('data', [])
    n_cell_data = len(cell_data)
    cells = []
    for ci in cell_info:
        if 'markdown' in ci:
            source = ci.pop('markdown')
            cell = new_markdown_cell()
        elif 'code' in ci:
            source = ci.pop('code')
            cell = new_code_cell()
        else:
            raise RuntimeError('Unknown cell type for cell:\n%s' % ci)
        if cell.cell_type == 'code' and source.endswith('\n'):
            # Skip trailing newlines in code cells.
            source = source[:-1]
        cell['source'] = source
        cell_id = ci.pop('id', None)
        if cell_id is not None and cell_id < n_cell_data:
            ci.update(cell_data[cell_id])

        cell.update(ci)
        cells.append(cell)

    nb = new_notebook(cells=cells)
    nb.update(yaml_data)
    return nb
