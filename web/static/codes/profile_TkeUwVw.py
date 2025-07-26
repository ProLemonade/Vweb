# 某时刻，水平平均，垂直剖面：TKE uw/vw

f = "D:/Example/"

# 读取
import numpy as np
from netCDF4 import Dataset
fn = f + "field.nc"
ncid = Dataset(fn)
z = ncid.variables['zC'][::-1]
Nz = z.shape[0]
ncid.close()

fn = f + "TKE.nc"
ncid = Dataset(fn)
TKE = ncid.variables['TKE'][:,:,0,0]
ncid.close()

fn = f + "twoOrder_A.nc"
ncid = Dataset(fn)
uw = ncid.variables['uwA'][:,::-1]
vw = ncid.variables['vwA'][:,::-1]
ncid.close()

t=-1
TKE_t=TKE[t, :]
uw_t = uw[t, :][:Nz]
vw_t = vw[t, :][:Nz]

# 画图
import matplotlib as mpl
import matplotlib.pyplot as plt
figsize = (6, 6)
fig = plt.figure(figsize=figsize)
gs = fig.add_gridspec(1, 2,left=0.02, right=0.98, bottom=0.05, top=0.95, hspace=0.1, wspace=0.1)

ax_tke = fig.add_subplot(gs[0, 0])
ax_flux = fig.add_subplot(gs[0, 1])

ax_tke.plot(TKE_t, z)
ax_tke.set(xlabel='TKE (m²/s²)', ylabel='Depth (m)')

ax_flux.plot(uw_t, z)
ax_flux.plot(vw_t, z)
ax_flux.set(xlabel='uw/vw (m²/s²)')
ax_flux.yaxis.set_ticks_position('none')
ax_flux.set_yticklabels([])
ax_flux.legend()

plt.suptitle('Vertical distribution of TKE uw/vw')
plt.legend()
#plt.show