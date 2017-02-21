import pytest
import nbformat

from ipyaml.cli import main, read_nb, read_yaml, file_type

from .test_convert import make_notebook


def test_file_type():
    for fname in ('test.ipyaml', 'test.ipyml', 'test.yml', 'test.yaml'):
        assert file_type(fname) == 'yaml'

    assert file_type('test.ipynb') == 'notebook'

    assert file_type('test.c') is None


def test_main_simple(tmpdir):
    # Given
    p = tmpdir.join('test.ipynb')
    src = str(p)
    p1 = tmpdir.join('test.ipyml')
    dest = str(p1)

    nb = make_notebook()
    nbformat.write(nb, src, 4)

    # When
    main(args=[src, dest])

    # Then
    nb1 = read_yaml(dest)

    assert nb1 == nb

    # When
    # Convert from yaml to nb
    main(args=[dest, src])

    # Then
    nb2 = read_nb(src)
    assert nb2 == nb


def test_main_without_output(tmpdir):
    # Given
    p = tmpdir.join('test.ipynb')
    src = str(p)
    p1 = tmpdir.join('test.ipyml')
    dest = str(p1)

    nb = make_notebook()
    nbformat.write(nb, src, 4)

    # When
    main(args=[src, dest, '--no-output'])

    # Then
    nb1 = read_yaml(dest)

    for key in nb:
        if key != 'cells':
            assert nb[key] == nb1[key]
    assert len(nb1.cells) == len(nb.cells)
    for i in range(3):
        assert nb1.cells[i].cell_type == nb.cells[i].cell_type
        assert nb1.cells[i].source == nb.cells[i].source

    assert len(nb1.cells[1].outputs) == 0
    assert len(nb1.cells[2].outputs) == 0


def test_main_with_bad_files_should_warn(capsys, tmpdir):
    # Given/When
    with pytest.raises(SystemExit):
        main(args=['foo.c', 'foo.ipyml'])

    # Then
    out, err = capsys.readouterr()
    assert 'ERROR: Unknown input' in err

    # Given
    p = tmpdir.join('test.ipynb')
    src = str(p)
    nb = make_notebook()
    nbformat.write(nb, src, 4)

    # When
    with pytest.raises(SystemExit):
        main(args=[src, 'foo.py'])

    # Then
    out, err = capsys.readouterr()
    assert 'ERROR: Unknown output' in err
