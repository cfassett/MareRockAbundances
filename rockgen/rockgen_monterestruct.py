# Various imports.  Most of these are standard and will be available on any system
import numpy as np
import pandas as pd
import copy, random
from modelparams import *

from math import *


class Crater:
    def __init__(self, x=0.0, y=0.0, diam=0.0):
        # crater properties for each crater
        self.x = x
        self.y = y
        self.diam=diam        

    def locate(self):
        """ Finds a random x y in m"""
        newx=random.uniform(0,domainsize_m)
        newy=random.uniform(0,domainsize_m)
        
        return newx, newy    

def npfcalc(size):
    '''this finds the NPF ==> N(>=size) for crater with -crater size-.  From Neukum and Ivanov/2001.
    sizes in km''' 
    
    
    #lunar surface area
    domainsize_km=domainsize_m/1000.0
    surfacearea=(domainsize_km**2.0)
    correctionfrom1millionyrsto1yr=1.0e-6
       
    log10freq=0.0
   
    npfcoeffs=[-6.076755981,-3.557528,0.781027,1.021521,-0.156012,-0.444058,0.019977,0.08685,-0.005874,-0.006809,0.000825,0.0000554]
    for a in range(12):
        log10freq=log10freq+npfcoeffs[a]*((log10(size))**a)
    
    cumfreq=correctionfrom1millionyrsto1yr*surfacearea*(10.0**log10freq)
        
    return cumfreq



def gruncalc(size_km):
    '''this finds the Grun ==> N(>=size) for crater with -crater size- size
    number for whole Moon (hard wired in, easy to change, see surfacearea)
    input sizes must be in m (important to track carefully, I know)
    
    >=10m just calls the NPF    
    ''' 
    
    #theseareparticleradii in cm
    #grunsizelist=[4.57078E-07, 9.84745E-07, 2.12157E-06, 4.57078E-06, 9.84745E-06, 2.12157E-05, 4.57078E-05, 9.84745E-05, 0.000212157,\
    #0.000457078, 0.000984745, 0.002121569, 0.004570781, 0.00984745, 0.021215688, 0.045707815, 0.098474502, 0.212156884, 0.45707815, 0.984745022,\
    #2.121568836, 4.570781497, 9.847450218, 21.21568836]      
    #for i in grunsizelist:
    #    print hohocratersize(i/100.0)   #/100 is because of meters
    
    
    #these are in m, assuming hohoscaling -- calculated above.  Can switch back to radii in cm with newcrat.hohoimpactorsize()/0.020   if desired.
    grundiameters=[6.91E-07,1.49E-06,3.21E-06,6.91E-06,1.49E-05,3.21E-05,6.91E-05,0.000148787,0.000320552,0.000690607,0.001487869,0.003205516,0.006906074,0.014878687,0.03205516,\
    0.069060751,0.148786877,0.32055161,0.690607508,1.487868771,3.205516094,6.906075072,14.87868771,32.05516094]

    #these are in /km2 /yr
    grunfluxes=[8.20E+12,1.20E+12,1.86E+11,3.47E+10,7.89E+09,2.62E+09,1.07E+09,4.73E+08,2.02E+08,9.47E+07,3.79E+07,9.47E+06,1.48E+06,1.45E+05,1.04E+04,6.00E+02,3.06E+01,1.48E+00,6.94E-02,3.16E-03, 1.48e-4,\
    1.46e-5, 1.15e-6,1.07e-7]   #these final three are all from Neukum.  The last value isn't actually used for anything.  Neukum matches up nicely with Grun
  
    grundiameterslog=[-6.160768847, -5.827435381, -5.4941018, -5.160768847, -4.827435381, -4.4941018, -4.160768847, -3.827435381, -3.4941018, -3.160768847, -2.827435381, -2.494102005, -2.160768752, -1.827435381, -1.494102046, -1.160768705, -0.827435372, -0.494102037, -0.160768705, 0.172564628, 0.505897962, 0.839231295, 1.172564628, 1.505897962]
    
    grundfluxeslog=[12.91407732, 12.07888756, 11.26995598, 10.54049665, 9.897043976, 9.418182059, 9.030582884, 8.675195226,8.305283941, 7.976225222, 7.578285213, 6.976225222, 6.171201825, 5.161861799, 4.017617907, 2.777857568, 1.485875701, 0.171201825, -1.158473352 ,-2.500896033, -3.828798175, -4.835279357, -5.940706041, -6.969624639]

    domainsize_m=236.9011752
    domainsize_km=domainsize_m/1000.0
    surfacearea=(domainsize_km**2.0)
    

    size=size_km*1000.0

    if size<10.0:
        slog=log10(size)
        fluxintlog=np.interp(slog, grundiameterslog, grundfluxeslog)
        fluxint=10.0**fluxintlog
        globalfreq=surfacearea*fluxint
    else:
        globalfreq=npfcalc(size/1000.0)   
    return globalfreq

    
def getdiams(timestep=0.0, lowersizethreshold=(10**-2.3), uppersizethreshold=10.0**-0.1):
    '''This takes the NPF for the Moon and generates a list of crater diams'''
    '''units of timestep are years'''
    '''craters returned are in m, calculations in km and log10 km'''     
    '''uppersizethreshold=10.0**-0.1 --> ~0.8km'''

    upperbinsize=log10(uppersizethreshold) #start at largest craters
    loglower=log10(lowersizethreshold)
      
    diams=[]  #start with an empty diameter list
    logsizestep=0.1 #start with this for large craters, since the odds that they form is smaller
    
    while (upperbinsize>loglower):   
        lowerbinsize=upperbinsize-logsizestep
                
        expectednumberinthisbin=timestep*(gruncalc(10**lowerbinsize)-gruncalc(10**upperbinsize))
        foundnumber=np.random.poisson(expectednumberinthisbin)   
        
        if foundnumber>0.0:
            choiceset=((10**lowerbinsize)+(10**upperbinsize-(10**lowerbinsize))*np.random.random_sample(1000))  
            wtssum=np.sum((choiceset)**-3.1)   #inbin distribution
            wts=((choiceset)**-3.1)/wtssum
            diams.extend((1000.0*np.random.choice(choiceset,foundnumber,p=wts)).tolist())            
               
        if lowerbinsize<-1.1: logsizestep=0.025 
        upperbinsize=copy.copy(lowerbinsize)              
    return diams



def drawreg(diamlist, lunarreg, lunarrockfa, domainpx, pxres):
    '''This takes a list of diameters (in m) and gives how the surface regolith array is modified'''
    '''it also calls the funciton that generates rocks'''
 
    for acrat in diamlist:
        newcrat=Crater(diam=acrat)
        newcrat.x,newcrat.y=newcrat.locate()    #these are in physical units {m}
        
        r=acrat/2.0
        #pixel_space
        px_x = newcrat.x/pxres
        px_y = newcrat.y/pxres
        px_r = (r/(pxres))
        
        x,y=np.ogrid[:domainpx,:domainpx]
        
        #distance in pixelspace
        distfromcen=((x-px_x)**2.0 + (y-px_y)**2.0)**0.5
        
        incrat=(distfromcen<px_r)
        outcrat=(distfromcen>=px_r)                    
        
        h_in=np.zeros((domainpx,domainpx))
        h_exterior=np.zeros((domainpx,domainpx))
                
        if acrat>100:   #From Hirabayashi, delta parameter 
            delta=0.3
        else:
            delta=0.34                       
            
        #From Hirabayashi et al.
        h_in[incrat] = delta*r*(1-((distfromcen[incrat]/px_r)**2.0))       
        h_exterior[outcrat] = sigma*r*(distfromcen[outcrat]/px_r)**-kappa               
               
        #excavate new rocks, but only if the regolith depth is thin enough that the excavation depth in the center exceeds the current regolith. 
        countabove=(lunarreg[incrat]<(excfac*acrat)).sum() #number of cells inside crater above excavation depth      
        numcells=np.count_nonzero(h_in)                    #number of cells inside crater 
        if numcells>0:
            fractaboveexcdepth=float(countabove)/float(numcells)        
            lunarrockfa=drawrocks(newcrat, lunarrockfa, domainpx, pxres,fractaboveexcdepth)        
        
        # update regolith depth
        lunarreg[h_in>lunarreg] = h_in[h_in>lunarreg]  #create new regolith inside the crater if the regolith that would be created is larger than what exists
        lunarreg=lunarreg+h_exterior                   #transport regolith to the outside of the crater        
        
        #    could imagine subtracting regolith in crater centers where underlying bedrock is not being touched
        #    also could bury -rocks- when excavating only regolith w/o rocks... "makecoldspots(newcrat, lunarrockfa, domainpx, pxres)".  But I don't think this is physically that important.
    return lunarreg, lunarrockfa

def drawrocks(newcrat, lunarrockfa, domainpx, pxres, f):
    '''This takes a craters and modifies the lunar rock fa array'''
    
    r=newcrat.diam/2.0
    px_x = newcrat.x/pxres
    px_y = newcrat.y/pxres
    px_r = (r/(pxres))        
    x,y=np.ogrid[:domainpx,:domainpx]
    distfromcen=((x-px_x)**2.0 + (y-px_y)**2.0)**0.5        
    incrat=(distfromcen<px_r)
    outcrat=(distfromcen>=px_r)        
    nearfield=(distfromcen<3*px_r)
    rn=np.zeros((domainpx,domainpx))
                    
    rn[incrat] = f*rparam 
    rn[outcrat] = f*rparam*(distfromcen[outcrat]/px_r)**-kappa
    rn[nearfield] = rn[nearfield]+constantexc
        
    lunarrockfa=np.maximum(lunarrockfa,rn)   
       
    return lunarrockfa
    
def destroyrocks(lunarrockfa):
    '''This has a half-life-like modification of the lunar rock fa array'''
    
    lunarrockfa=lunarrockfa*exp(-rocklambda*modeltimestep)

    return lunarrockfa
   
    
       
#endtimeMoon is in the params
endtime=neqtime(endtimeMoon)        
steps=int(floor(endtime/modeltimestep))
ct=0
resultsarray=np.zeros((nruns,steps))
regarray=np.zeros((nruns,steps))

while (ct<nruns):
    lunarreg=np.zeros((domainpx,domainpx))+regthicknaught
    lunarrockfa=np.zeros((domainpx,domainpx))   	
    t=0.0
    step=0 
    while (step<steps):	    
        t=t+modeltimestep
        newdiams=getdiams(timestep=modeltimestep)
        lunarreg, lunarrockfa=drawreg(newdiams, lunarreg, lunarrockfa, domainpx, pxres)
        lunarrockfa=destroyrocks(lunarrockfa)  	
        regarray[ct,step]=np.percentile(lunarreg,50) 
        resultsarray[ct,step]=np.sum(lunarrockfa)/(domainpx**2.0)		
        step=step+1
    ct=ct+1

model='tuneout.csv'
f=open(model,'w+')
f.write("age,rparam,cexec,halflife,5thPercentileRA,MedianRA,95thPercentileRA,MeanRA,regthick\n")
step=0
t=0.0
while (step<steps):	    
    t=t+modeltimestep
    curractualtime=eqtimeton(t)
    wrstr=str(curractualtime/1.0e6)+","+str(rparam)+","+str(constantexc)+","+str(halflife)+","+str(np.percentile(resultsarray[:,step],5, axis=0))+","+str(np.percentile(resultsarray[:,step],50,axis=0))+","+str(np.percentile(resultsarray[:,step],95, axis=0))+","+str(np.mean(resultsarray[:,step],axis=0))+','+str(np.percentile(regarray[:,step],50,axis=0))+'\n'
    step=step+1
    print(wrstr)
    f.write(wrstr)
f.close()



#sashankdatapath='/users/cfassett/sashank_rockgen_tune/sashankdata.csv'
sashankdatapath='/users/cfassett/sashank_rockgen_tune/vv'
sashdf=pd.read_csv(sashankdatapath)
modeldf=pd.read_csv(model)

mergeDF=pd.merge_asof(sashdf,modeldf, on='age')
mergeDF['5thsym']=(mergeDF['5thPercentileRA_x']/mergeDF['5thPercentileRA_y']).apply(log).apply(abs)
mergeDF['95thsym']=(mergeDF['95thPercentileRA_x']/mergeDF['95thPercentileRA_y']).apply(log).apply(abs)
mergeDF['Medsym']=(mergeDF['MedianRA_x']/mergeDF['MedianRA_y']).apply(log).apply(abs)
mergeDF['Meansym']=(mergeDF['MeanRA_x']/mergeDF['MeanRA_y']).apply(log).apply(abs)

accuracyagg=mergeDF[['5thsym', '95thsym','Medsym', 'Meansym']]
acc=exp(np.median(accuracyagg.values.flatten()))-1

g=open("/users/cfassett/scratch/tuneout_thickerI.csv",'a+') 
wrstr=str(rparam)+","+str(constantexc)+","+str(halflife)+","+str(acc)+"\n"
g.write(wrstr)
g.close()

