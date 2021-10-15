from math import *
from pynverse import inversefunc  #pip install pynverse  in relevant conda environment

domainsize_m=236.9011752  #linear dimension of Domain edge, in m. ~236 is a Diviner pixel
domainpx=118           #linear dimension of Domain in -pixels-
pxres=domainsize_m/domainpx   #resolution (m/px)
modeltimestep=5.0e7     # yrs
endtimeMoon=3.72e9       # yrs  ~ endtime for <3 Ga, for greater, use Neukum chronology.  Now set on commandline
###endtime_stepper=2.0e8   # tiemstep for endtimes   NOT USING IN NON-MC MODE


# Should be big in the real run
nruns=1000

###assert endtimeMoon<4.5e9


#excavation factor (excavation depth, as fraction of crater diameter)
excfac=0.1              # This is a canonical rule of thumb from Melosh 1989

#Hirabayashi parameters  (from Hirabayashi et al, 2018; https://agupubs.onlinelibrary.wiley.com/doi/full/10.1002/2017JE005377)
sigma=0.014
kappa=3.0

#initial regolith thickness (artificial)
regthicknaught=2.0

#RockAbundance initial parameters
rparam=0.08

#RockAbundance Decay Rate
halflife=80000000  #60 million years Basilevsky et al. 2013; https://linkinghub.elsevier.com/retrieve/pii/S0032063313001906
rocklambda=(0.69314718056)/halflife     #rock lambda is ln(2)/halflife

#RockAbundance constant exc coming out of the regolith
constantexc=0.004

# Helper functions to implement Neukum chronology  {needed to handle enhanced early flux}.  
def neqtime(time):
    timeMa=time/1.0e6
    timeCorMa=(0.0000000000000544*(exp(0.00693*timeMa)-1)+0.000000838*timeMa)/0.000000838  
    timeCor=timeCorMa*1.0e6 # convert back to Neukum-eq years (not physical years, for the early chronology!)
    
    return timeCor

eqtimeton=inversefunc(neqtime)

#uppersizethreshold=10.0**-0.1:  D~800m.  This is set explicitly in the code, could be modified, but seems sensible.
#lowesizethreshold=10.0**-2.3  :    5m


