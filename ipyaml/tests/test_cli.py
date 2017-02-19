import nbformat

from ipyaml.cli import main, read_nb, read_yaml, file_type

from .test_convert import make_notebook


def test_file_type():
    for fname in ('test.ipyaml', 'test.ipyml', 'test.yml', 'test.yaml'):
        assert file_type(fname) == 'yaml'

    assert file_type('test.ipynb') == 'notebook'

    assert file_type('test.c') is None


def test_main(tmpdir):
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
