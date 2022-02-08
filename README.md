# Mare Rock Abundance code and data

This repository is for the Vanga et al. study, Rock abundance on the lunar mare on surfaces of different age: Implications for regolith evolution and thickness, in Geophysical Research Letters

plot.py is used to make Fig 2

plot_monte carlo.py is used to make Fig 3

The raw extractor for the data was RasterStatisticsFullExtractor.py.

A raw csv file from this extraction is available on Zenodo at the associated <a href="https://dx.doi.org/10.5281/zenodo.6011671">data archive</a>. Also available there is the neighborhood crater frequency raster from Fassett and Thomson (2014). 

The Monte Carlo model was run with a parameter search.  An example with a single set of parameters is shown in the rockgen subfolder.  The only non-standard python package required to make this work is <A href="https://pypi.org/project/pynverse/">pynverse</a>.

The Mann-Kendall test requires <a href="https://pypi.org/project/pymannkendall/">pymannkendall</a>.  
