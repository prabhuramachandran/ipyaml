from textwrap import dedent
import pytest
from nbformat.v4 import (new_notebook, new_code_cell, new_markdown_cell,
                         new_output)

from ipyaml.convert import nb_to_yaml, yaml_to_nb, StringIO
import yaml


def make_notebook():
    src = "print(1)"
    output = new_output('stream', text='1\n')
    code1 = new_code_cell(
        source=src,
        outputs=[output],
        metadata=dict(collapsed=False),
        execution_count=1
    )
    src = "list(range(3))"
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


def test_nb_to_yaml_without_outputs():
    # Given
    nb = make_notebook()

    # When
    yml = nb_to_yaml(nb, dump_output=False)
    data = yaml.load(StringIO(yml))
    nb1 = yaml_to_nb(data)

    # Then
    for key in nb:
        if key != 'cells':
            assert nb[key] == nb1[key]
    assert len(nb1.cells) == len(nb.cells)
    for i in range(3):
        assert nb1.cells[i].cell_type == nb.cells[i].cell_type
        assert nb1.cells[i].source == nb.cells[i].source


def test_yaml_with_bad_cell_type_raises_error():
    # Given
    data = dedent("""\
    cells:
      - source: |
          print(1)
          print(2)
    """)
    s = StringIO(data)
    yml = yaml.load(s)

    # When/Then
    with pytest.raises(RuntimeError) as excinfo:
        yaml_to_nb(yml)

    assert 'Unknown cell type for cell' in str(excinfo.value)
