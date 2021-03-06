#!/bin/python3

#########################
######### ROUTINE TO PLOT THE SEASONAL MEAN OF ANY VARIABLE OVER AN ALREADY 
######### SELECTED REGION.
#########################


import cartopy
import cartopy.feature as cfeat
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import xarray as xr
import numpy as np

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.colors import BoundaryNorm
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable


#########################
######### OPENING FILES AND DIRECTORIES
#########################

directory = '/media/lgarcia2/CHIBIMOON/Raw_data/Monthly/Region/Mean/'
file1 = 'Clim_JJAS.nc'

file2 = 'JJ_06.nc'
file3 = 'JJ_07.nc'
file4 = 'JJ_08.nc'
file5 = 'JJ_09.nc'

#Regional data, 2D graph
mean_JJAS =  xr.open_dataset(directory+file1)
Jun_data = xr.open_dataset(directory+file2)
Jul_data = xr.open_dataset(directory+file3)
Aug_data = xr.open_dataset(directory+file4)
Sep_data = xr.open_dataset(directory+file5)


#Monthly Climatology
JJAS = mean_JJAS.sp[0]
jun = Jun_data.sp[0] 
jul = Jul_data.sp[0] 
aug = Aug_data.sp[0] 
sep = Sep_data.sp[0] 


#########################
######### SETTING THE RANGE OF VALUES TO PLOT
#########################

### Parameter 'vmin/vmax' will be scaled dependig on the magnitude. Parameter a
### makes visible the values in the region of interest if they are too different
### from the extremes. (Just uncomment!) HERE WE HAVE TWO VALUE a

### For precipitation:       
#scale = 1000.
#amax = 85.29
#amin = 0.

### For SST:                 
#scale = 1.
#amax = 0.87
#amin = -0.65

### For pressure:            
scale = 1e-2
amax = 0.
amin = 408.        


#Array of all the values to determine the max and min
var = np.array(JJAS)
var = np.vstack((var, jun))
var = np.vstack((var, jul))
var = np.vstack((var, aug))
var = np.vstack((var, sep))

v =[]

for i in range(len(var)):
    for j in range(len(var[i])):
        if ( np.isnan(var[i,j]) != True):
            v =np.append(v, var[i,j])

vmin = np.amin(v)
vmax = np.amax(v)


vmin = vmin*scale+amin
vmax = vmax*scale-amax


##Just checking
print(np.amax(v*scale))
print(np.amin(v*scale))
print(vmin, vmax)     #This works for the precipitation




#########################
######### STARTING THE PLOT
#########################

##Stating the number of plots to do in this plot. Is better to make just one!!!
Nrows = 1
Ncols = 1


##Seting the coordinates
x = mean_JJAS.longitude
y = mean_JJAS.latitude
x_n, y_n = np.meshgrid(x, y)


##Variable to plot 

#var = JJAS*scale
#var = jun*scale
#var = jul*scale
#var = aug*scale
var = sep*scale

title_fig = 'Mean pressure and wind fields, September'
print(title_fig)


##If wind is needed uncomment this lines
u = Sep_data.u10[0]
v = Sep_data.v10[0]
#jun = Jun_data.sst[0] 
#jul = Jul_data.sst[0] 
#aug = Aug_data.sst[0] 
#sep = Sep_data.sst[0] 

##For wind field in pressure plot include this 4 lines
#windspeed = (u**2 + v**2)**0.5
u_norm = u / np.sqrt(u ** 2.0 + v ** 2.0)
v_norm = v / np.sqrt(u ** 2.0 + v ** 2.0)


#########################
### PARAMETERS OF COLORBAR:
###    (just uncomment)
#########################
### PRECIPITATION 
#ticks = ['<-8.3', '-6.7', '-5.1', '-3.5', '-1.9', '0.0', 
#         '1.9', '3.5', '5.1', '6.7', '>8.3']
#title_cbr = 'pp [mm day-1]'
#cmap = 'YlGnBu'

### SEA SURFACE TEMPERATURE
#ticks = ['<-8.3', '-6.7', '-5.1', '-3.5', '-1.9', '0.0', 
#         '1.9', '3.5', '5.1', '6.7', '>8.3']
#title_cbr = 'SST [K]'
#cmap = 'RdYlBu_r'
#
### PRESSURE
#ticks = ['<-8.3', '-6.7', '-5.1', '-3.5', '-1.9', '0.0', 
#         '1.9', '3.5', '5.1', '6.7', '>8.3']
title_cbr = 'pressure [hPa]'
cmap = 'Spectral'

orientation = 'vertical'


##Projection and region to plot
proj = ccrs.PlateCarree(360)
reg = [-180, -30, -10, 45]


fig, ax = plt.subplots(nrows=Nrows, ncols=Ncols, subplot_kw=dict(projection=proj), figsize=(15,5))

ax.set_global()
ax.coastlines('50m')
ax.add_feature(cartopy.feature.BORDERS, linestyle=':')
ax.set_extent(reg, crs=ccrs.PlateCarree())     #lat, lon

ax.contourf(x_n, y_n, var, levels=np.linspace(vmin,vmax,30), cmap=cmap)
contr = ax.contourf(x_n, y_n, var, levels=np.linspace(vmin,vmax,30), cmap=cmap)
cb0 = fig.colorbar(contr, ax=ax, orientation=orientation)
cb0.set_label(title_cbr)

#For pressure/wind include this line
ax.quiver(x_n[::10, ::10]+360, y_n[::10,::10], u_norm[::10, ::10], v_norm[::10, ::10], pivot='tip', width=0.001)

ax.set_title(title_fig)

plt.subplots_adjust(top=0.912, bottom=0.046, left=0.015, right=0.985, hspace=0.43, wspace=0.2)
fig.savefig('/media/lgarcia2/CHIBIMOON/Tesis_ICTP/September_wind.pdf')
plt.show()

