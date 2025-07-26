# 深度-时间图：UV

f = "D:/Example/"

# 读取
import numpy as np
from netCDF4 import Dataset
fn = f + "field.nc"
ncid = Dataset(fn)
z = ncid.variables['zC'][::-1]
time = ncid.variables['time'][:]
Nz = z.shape[0]
ncid.close()

fn = f + "Average.nc"
ncid = Dataset(fn)
ncid.variables
U = ncid.variables['U'][:,::-1][:,:Nz]
V = ncid.variables['V'][:,::-1][:,:Nz]
#W = ncid.variables['W'][:,::-1][:,:Nz]
#P = ncid.variables['P'][:,::-1][:,:Nz]
#Tₐ = ncid.variables['Tₐ'][:,::-1][:,:Nz]
ncid.close()

# 画图
import matplotlib.pyplot as plt
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

pc1 = ax1.pcolormesh(time / 3600, z, U.T, cmap='RdBu_r', shading='auto')
plt.colorbar(pc1, ax=ax1, label='U (m/s)')
ax1.set(ylabel='Depth (m)')

pc2 = ax2.pcolormesh(time / 3600, z, V.T, cmap='RdBu_r', shading='auto')
plt.colorbar(pc2, ax=ax2, label='V (m/s)')
ax2.set(xlabel='Time (hours)', ylabel='Depth (m)')

plt.tight_layout()
#plt.show()