# 时间平均，水平平均，垂直剖面：νₑ

f = "D:/Example/"

# 读取
import numpy as np
from netCDF4 import Dataset
fn = f + "field.nc"
ncid = Dataset(fn)
x = ncid.variables['xC'][:]
y = ncid.variables['yC'][:]
z = ncid.variables['zC'][::-1]
time = ncid.variables['time'][:]
Nx, Ny, Nz = x.shape[0], y.shape[0], z.shape[0]
Y=int(Nx/2)
Z=int(Ny/2)
νₑ = ncid.variables['νₑ'][:, ::-1, Y , Z ]
ncid.close()


# 画图
import matplotlib.pyplot as plt
νₑ_a = νₑ.mean(axis=0)
plt.figure(figsize=(10, 6))
plt.semilogx(νₑ_a, z)

plt.xlim(1e-8, 1e-6)

plt.xlabel('νₑ (m²/s)')
plt.ylabel('Depth (m)')
plt.title('νₑ Profile (log)')
plt.grid(True, which='both', linestyle='--', alpha=0.5)
#plt.show()