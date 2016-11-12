''' 
The following demonstrates using *rbf.filter.filter* to remove noise 
from the classic Lena image. The image has been resampled into 100,000 
data points which are normally distributed about [0.5,0.5] and white 
noise has been added to each datum. *rbf.filter.filter* acts as a 
low-pass filter which damps out frequencies which are higher than the 
user specified cutoff frequency.  In this example the cutoff frequency 
is set to 40.
'''
import numpy as np
from scipy.misc import lena
from scipy.interpolate import NearestNDInterpolator
import matplotlib.pyplot as plt
from rbf.filter import filter
from rbf.halton import Halton
from matplotlib.ticker import AutoMinorLocator

y = np.linspace(1.0,0.0,512)
x = np.linspace(0.0,1.0,512)
x,y = np.meshgrid(x,y)
points = np.array([x.flatten(),y.flatten()]).T
#values = np.loadtxt('../data/fabric.csv').flatten()
#values = np.loadtxt('/cmld/data2/hinest/Desktop/snake.csv').flatten()
#values /= 255.0 # normalize so that the max is 1.0
def signal(points):
  freq1 = 20*points[:,0]
  freq2 = 20*points[:,1]
  func = np.sin(2*np.pi*points[:,0]*freq1)*np.sin(2*np.pi*points[:,1]*freq2) 
  out = (func + 1.0)/2.0
  #out = (func > 0.0).astype(float)
  return out

#signal = NearestNDInterpolator(points,values)

# interpolate Lena onto new observation points and add noise
H = Halton(2)
points_obs = H(50000)
u_obs = signal(points_obs) #+ np.random.normal(0.0,0.2,40000)
# find filtered solution
cutoff1 = 1.0/0.1
soln1,sigma = filter(points_obs,u_obs,cutoff=cutoff1,n=12)
cutoff2 = 1.0/0.05
soln2,sigma = filter(points_obs,u_obs,cutoff=cutoff2,n=12)
cutoff3 = 1.0/0.025
soln3,sigma = filter(points_obs,u_obs,cutoff=cutoff3,n=12)

# plot the observed and filtered results
minorLocator = AutoMinorLocator()
fig,ax = plt.subplots(2,2,figsize=(8,8))
ax = [ax[0][0],ax[0][1],ax[1][0],ax[1][1]]
for i in range(4): ax[i].set_aspect('equal')
for i in range(4): ax[i].set_axis_bgcolor('blue')
for i in range(4): ax[i].set_xlim((0,1.0))
for i in range(4): ax[i].set_ylim((0,1.0))
for i in range(4): ax[i].set_title('Noisy Data')
for i in range(4): ax[i].xaxis.set_minor_locator(minorLocator)
for i in range(4): ax[i].yaxis.set_minor_locator(minorLocator)
for i in range(4): ax[i].tick_params(which='both', width=1)
for i in range(4): ax[i].tick_params(which='major', length=6)
for i in range(4): ax[i].tick_params(which='minor', length=4)

ax[0].set_title(r'Observed')
p1 = ax[0].scatter(points_obs[:,0],points_obs[:,1],s=2,c=u_obs,
                   edgecolor='none',cmap='Greys_r',vmin=0.0,vmax=1.0,rasterized=True)
ax[1].set_title(r'Filtered Solution $\mathregular{(\omega_c = %s)}$' % cutoff1)
p2 = ax[1].scatter(points_obs[:,0],points_obs[:,1],s=2,c=soln1,
                   edgecolor='none',cmap='Greys_r',vmin=0.0,vmax=1.0,rasterized=True)
ax[2].set_title(r'Filtered Solution $\mathregular{(\omega_c = %s)}$' % cutoff2)
p2 = ax[2].scatter(points_obs[:,0],points_obs[:,1],s=2,c=soln2,
                   edgecolor='none',cmap='Greys_r',vmin=0.0,vmax=1.0,rasterized=True)
ax[3].set_title(r'Filtered Solution $\mathregular{(\omega_c = %s)}$' % cutoff3)
p2 = ax[3].scatter(points_obs[:,0],points_obs[:,1],s=2,c=soln3,
                   edgecolor='none',cmap='Greys_r',vmin=0.0,vmax=1.0,rasterized=True)
plt.tight_layout()

plt.savefig('../figures/filter.d.png')
plt.show()

