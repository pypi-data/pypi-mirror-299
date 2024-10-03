from setuptools import setup, find_packages

setup(
    name='pandaPlus',
    version='0.3',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    license = 'MIT',
    author = 'Tiara Mathur',
    author_email = 'mathurtiara@gmail.com',
    url = 'https://github.com/tiaramathur/',
    keywords = ['pandas', 'formatting', 'dataframes'],
    install_requires=[
        'pandas',
	'xlsxwriter'
    ],
)
