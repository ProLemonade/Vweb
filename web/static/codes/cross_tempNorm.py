# 某时刻，某竖直面：T_norm 最小/大温度值映射为0/1

f = "../static/data/Example/"

# 读取
import numpy as np
from netCDF4 import Dataset

fn_era5 = f + "field.nc"
ncid = Dataset(fn_era5)
z = ncid.variables['zC'][::-1]
Nz = z.shape[0]
x = ncid.variables['xC'][::-1]
Nx = x.shape[0]
y = ncid.variables['yC'][::-1]
Ny = y.shape[0]

t=-1
Txz = ncid.variables['T'][t, ::-1, :, Ny//2]
Txz_norm = (Txz - np.min(Txz)) / (np.max(Txz) - np.min(Txz))

# 画图
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
fig, ax = plt.subplots(figsize=(10, 7))

colors = ['black', 'darkblue', 'blue', 'lightblue', 'yellow']
custom_cmap = LinearSegmentedColormap.from_list('custom', colors, N=100)
im = ax.imshow(Txz_norm,
            cmap=custom_cmap,
            aspect='auto',
            interpolation='gaussian',extent=[x[0], x[-1], z[0], z[-1]])

ax.set_title('Temperature Field', color='white')
plt.colorbar(im, ax=ax)

# plt.show()