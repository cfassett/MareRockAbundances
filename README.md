# MareRockAbundances
Vanga et al. study of Rock abundance evolution with time

plot.py makes Fig 2

plot_monte carlo.py makes Fig 3


The raw extractor for the data was RasterStatisticsFullExtractor.py.
The raw csv file  from this extraction is available on <a href="https://drive.google.com/file/d/16CDSCZU0k1DVQBBm7_jmSfooDD9PmSJJ/view?usp=sharing">Google Drive</a>. Also available is the <a href="https://github.com/cfassett/MareRockAbundances/blob/main/FT2014-Dense50kmN-n800mto5km.tif.zip">neighborhood crater frequency raster</a> from Fassett and Thomson (2014).  Both  will be put on a Zenodo archive after completion of peer-review.

The Monte Carlo model was run with a parameter search.  An example with a single set of parameters is shown in the rockgen subfolder.  The only non-standard python package required to make this work is <A href="https://pypi.org/project/pynverse/">pynverse</a>.

The Mann-Kendall test requires <a href="https://pypi.org/project/pymannkendall/">pymannkendall</a>.  
