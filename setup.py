from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

# any data files that match this pattern will be include in the build
data_files_to_include = ["*.png", "*.tngl", "*.jpg"]

setup(
    name='tangle-node-editor',
    version='1.0.6-alpha',
    packages=find_packages(),
    package_data={
        "": data_files_to_include,
    },
    url='https://www.github.com/nielsvaes/tangle',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["ez-qt", "ez-settings", "ez-utils", "PySide2", "numpy", "pillow", "pyqtgraph"],
    license='MIT',
    author='Niels Vaes',
    author_email='nielsvaes@gmail.com',
    description='A Python based node editor',

    entry_points = {
        'console_scripts': ['tangle=tangle.app:main'],
    },
)
