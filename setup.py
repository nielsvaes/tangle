from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='tangle-node-editor',
    version='0.0.1',
    packages=['tangle'],
    url='https://www.github.com/nielsvaes/tangle',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["ez-qt", "ez-settings", "ez-utils", "PySide2", "numpy"],
    license='MIT',
    author='Niels Vaes',
    author_email='nielsvaes@gmail.com',
    description='A Python based node editor, very early version',

    entry_points = {
                   'console_scripts': ['tangle=tangle.app:main'],
               },
)
