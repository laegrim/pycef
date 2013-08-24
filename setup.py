import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name = "PyCef",
    version = "0.0.6",
    packages = find_packages(),
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires = ['BeautifulSoup','configobj', 'multiprocessing',
                        'pymongo', 'requests'],
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.conf', '*.csv'],
    },

    # metadata for upload to PyPI
    author = "Samuel Teich",
    author_email = "steich@gmail.com",
)
