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

1. Download deltascope folder from Git.
2. Open terminal for installation
	- Download all the packages mentioned in `requirements.txt` using pip package installer. 
		- For example in order to install `numpy`, use `pip install numpy`.
	- Go to the working directory of your deltascope folder, install a local project in "editable" mode.
		- For example, if you stored your deltascope folder on you desktop, and assume the name of your deltascope name is "deltascope", ```cd desktop```  ```cd deltascope``` ```$ pip install -e .```
  - Download Anaconda and launch JupyterLab. You should only be required to interface with the `experiments` folder.
  - We work with Jupyter Notebook files within JupyterLab.

Setting up
------

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
- If the circle on the top right corner of your Jupyter Notebook file is filled, the computer is working to read in the data. It just takes time.

Functions
----------

- k: The dictionary key that identifies this sample. It should be the sample number extracted from the filename.
- df: The dataframe containing datapoints associated with the primary alignment channel, in this case, AT.
- Ldf: A list of additional dataframes corresponding to other channels in the collection. In this template, we are assuming only one additional channel, ZRF.
- ax: The format used to present outputs. In our case there are two rows and three columns, 2x3.

Example Alignment
------

- *Note that all the code should be run in order--because all the objects for different alignments all have the same names, running the code not in the order it's written will mess up the data.*
- Four alignment correction options: dotted line is where we want the commissure to be, and solid line is where the commissure in the actual sample is.

![Types of alignment](/experiments/alignments.png)

- Use the corresponding functions within each category to correctly align the samples.
- The `ut.make_graph(df1,Ldf1)` functions under category C and D are currently not working.
- In the actual graphs deltascope outputs, the yellow line represents x-axis, red line y-axis and teal line z-axis.
  - First column
    - this is a view in the xy plane: we are viewing the parabolic commissure structure from the front. Therefore, we want the commissure to lie flat on x-axis in the final alignment.
    - The first alignment picture below is how an ideal xy plane view of the commissure should look like: the commissure lies flat on the x-axis. The second alignment picture suggests that there still needs to be some adjustments done: the slightly curved shape formed by the data points suggests that the two tails of the parabolic commissure is probably tilted above the x-axis, so we would want the two tails drop until they align with the x-axis.
    
    
![commissure lying flat on x-axis](experiments/testvideo/1_flat.png)
![commissure tails tilted above x-axis](experiments/testvideo/1_tilted.png)
  - Second column
    - this is a view in the xz plane: we are viewing the commisure from above, and we are able to see the very obvious commissure structure.
  - Third column
    - this is a view in the yz plane: we are viewing the parabolic commissure from its side. Since this is a side view of the structure, we would expect it to be lying flat on the teal-colored z-axis, but empirical results have shown that it is the best when the commisure is tilted 50 degrees below the z-axis. Here is an example:
    
![tilted 50 360$^\circ$ below z-axis](experiments/testvideo/3_tilted.png)

Finishing up
-------------

- Click on `File` in the upper left corner of JupyterLab and go down to `Export Notebook As...` and save your output as html. This way the next time you need to check your alignments there is no need to take a long time to read in the data again and run through the entire file.

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
