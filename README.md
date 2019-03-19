deltascope
===========

This package is designed to quantify biological structures in 3D image data.

Features
------

- Compare sets of 3D biological images to identify differences
- Automatically align the structure in the image to correct for variation introduced during mounting and imaging
- Generate descriptive graphs that quantify both the average and variation of the data
- Use machine learning techniques to classify samples and identify regions of statistically significant difference

Installation
------

Package hosted on [PyPI](https://pypi.python.org/pypi/deltascope)

	$ pip install deltascope: try running `pip install -e` from the root of the deltascope directory.

Setting up
------

- Download Anaconda and launch JupyterLab, then interface with the `experiments` folder.
- Set the kernel to be `deltascope`.
- Parameters: Wild-Type sample has radius 20; You-Too sample has radius 10.

Setting directories
------

- For windows users, please use backslashes (e.g., `os.path.abspath(.\SampleNum)`).
- For mac users, please use normal slashes (e.g., `os.path.abspath(./SampleNum)`).
- `gfap` corresponds to You-Too data whereas `at` corresponds to Wild-Type data.

Reading in the data
------

- For personal laptops, please try limiting the maximum amount of data being read in under 10 paired samples (so 20 samples in total).
- It will take approximately 30 seconds per sample, and the code prints out how long each iteration takes.

Alignment
------

- Four alignment correction options: dotted line is where we want the commissure to be, and solid line is where the commissure in the actual sample is.

![Types of alignment](/experiments/alignments.png)

Support
------

- Complete documentation is available on [Read the Docs](http://deltascope.readthedocs.io/en/latest/).
- Check out the [Frequently Asked Question <faq>]() page.
- Submit an issue describing a problem or question on the project's Github [Issue Tracker](http://github.com/msschwartz21/deltascope/issues).

Contribute
------

- Issue Tracker: https://github.com/msschwartz21/deltascope/issues
- Source Code: https://github.com/msschwartz21/deltascope

License
------

This project is licensed under the GNU General Public License.
