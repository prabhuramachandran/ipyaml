import os
from setuptools import setup, find_packages

data = {}
fname = os.path.join('ipyaml', '__init__.py')
exec(compile(open(fname).read(), fname, 'exec'), data)

install_requires = ['pyyaml', 'nbformat']
tests_require = ['pytest']

setup(
    name='ipyaml',
    version=data.get('__version__'),
    author='Prabhu Ramachandran',
    author_email='prabhu@aero.iitb.ac.in',
    description='Convert IPython notebooks to YAML and vice-versa',
    url='https://github.com/prabhuramachandran/ipyaml',
    packages=find_packages(),
    install_requires=install_requires,
    tests_require=tests_require,
    package_dir={'ipyaml': 'ipyaml'},
    entry_points="""
        [console_scripts]
        ipyaml = ipyaml.cli:main
    """
)
