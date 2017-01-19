from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='cross',
    version='1.0.0',
    description='Tool to cross CSV/TSV datasets',
    long_description='If you deal every with data in text fomat (TSV/CSV), cross will help you NOT to write THAT script you have rewritten thousands of times to cross two files that share the same key column.',

    url='https://github.com/coelias/cross',
    author='Carlos del Ojo Elias',
    author_email='deepbit@gmail.com',

    license='GPLv3',

    classifiers=[
        'Development Status :: 5 - Production/Stable',

        "Topic :: Scientific/Engineering :: Information Analysis",
        'Topic :: Scientific/Engineering :: Bio-Informatics',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',

        'Intended Audience :: Science/Research',

        'Environment :: Console',
    ],

    keywords='csv tsv cross dataset',

    packages=find_packages(),

    entry_points={
        'console_scripts': [
            'cross=cross.cross:main',
        ],
    },
)
