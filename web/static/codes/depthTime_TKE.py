# 深度-时间图：TKE

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

fn = f + "TKE.nc"
ncid = Dataset(fn)
TKE = ncid.variables['TKE'][:,:,0,0]
ncid.close()

# 画图
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(10,4))
plt.contourf(time/3600, z, TKE.T, levels=10, cmap='rainbow')

plt.colorbar(label='TKE')
plt.xlabel('Time(hours)')
plt.ylabel('Depth(m)')
plt.title('Turbulent Kinetic Energy Distribution')
#plt.show()
