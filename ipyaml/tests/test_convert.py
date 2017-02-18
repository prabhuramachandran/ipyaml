from nbformat.v4 import (new_notebook, new_code_cell, new_markdown_cell,
                         new_output)

from ipyaml.convert import nb_to_yaml, yaml_to_nb, StringIO
import yaml


def make_notebook():
    src = "print(1)\n"
    output = new_output('stream', text='1\n')
    code1 = new_code_cell(
        source=src,
        outputs=[output],
        metadata=dict(collapsed=False),
        execution_count=1
    )
    src = "list(range(3))\n"
    output = new_output(
        'execute_result',
        {'text/plain': "[0, 1, 2]"},
        execution_count=2
    )
    code2 = new_code_cell(
        source=src,
        outputs=[output],
        metadata=dict(collapsed=False),
        execution_count=2
    )

    md = new_markdown_cell(source='Hello world\n')
    cells = [md, code1, code2]
    nb = new_notebook(metadata=dict(language='python'), cells=cells)
    return nb


def test_nb_to_yaml():
    # Given
    nb = make_notebook()

    # When
    yml = nb_to_yaml(nb)
    data = yaml.load(StringIO(yml))
    nb1 = yaml_to_nb(data)

    # Then
    print(nb)
    print(nb1)
    assert nb1 == nb
