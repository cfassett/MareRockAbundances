# MareRockAbundances
Vanga et al. study of Rock abundance evolution with time

Figs 1-3 of paper

plot.py makes Fig 2
plot_monte carlo.py makes Fig 3

The raw extractor for the data was RasterStatisticsFullExtractor.py.
The raw csv file  from this extraction is available on <a href="https://drive.google.com/file/d/16CDSCZU0k1DVQBBm7_jmSfooDD9PmSJJ/view?usp=sharing">Google Drive</a>


The Monte Carlo model was run with a parameter search (see rockgen_tune) and can be more simply run with a single set of parameters (see rockgen).  
The only non-standard python package required to make this work is <A href="https://pypi.org/project/pynverse/">pynverse</a>.
