# 某时刻，三截面：垂直速度w

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
Lx, Ly, Lz = np.max(np.abs(x)),np.max(np.abs(y)),np.max(np.abs(z))

# 某时刻表面
t = -1
u = ncid.variables['u'][t, ::-1, :, :]
v = ncid.variables['v'][t, ::-1, :, :]
ncid.close()

surface = 0
u_xy = u[surface, :, :]
v_xy = v[surface, :, :]

stride = 5
X, Y = np.meshgrid(x[::stride], y[::stride])
U = u_xy[::stride, ::stride]
V = v_xy[::stride, ::stride]

# 画图
import matplotlib.pyplot as plt
fig, ax = plt.subplots()
q = ax.quiver(X, Y, U.T, V.T, scale=3, color='blue')
ax.set(xlabel='x (m)', ylabel='y (m)',title=f'Surface Current Vectors')
ax.axis('equal')

#plt.show()