# 某时刻，三截面：垂直速度w

f = "D:/Example/"

# 读取
import numpy as np
from netCDF4 import Dataset
fn = f + "field.nc"
ncid = Dataset(fn)
time = ncid.variables['time'][:]
x = ncid.variables['xC'][:]
y = ncid.variables['yC'][:]
z = ncid.variables['zC'][::-1]
Nx, Ny, Nz = x.shape[0], y.shape[0], z.shape[0]
Lx, Ly, Lz = np.max(np.abs(x)),np.max(np.abs(y)),np.max(np.abs(z))

# 某时刻三维数据
t = -1
u = ncid.variables['u'][t, ::-1, :, :]
v = ncid.variables['v'][t, ::-1, :, :]
w = ncid.variables['w'][t, ::-1, :, :][:Nz,:,:]
ncid.close()

# 格点数据&切片
x3d = np.tile(x[np.newaxis, np.newaxis, :], (Nz, Nx, 1))
y3d = np.tile(y[np.newaxis, :, np.newaxis], (Nz, 1, Ny))
z3d = np.tile(z[:, np.newaxis, np.newaxis], (1, Nx, Ny))
ix_crs = 50
iy_crs = 50
iz_crs = 20

# 画图
import matplotlib as mpl
import matplotlib.pyplot as plt
figsize = (5, 5)
fig = plt.figure(figsize=figsize)

gs = fig.add_gridspec(2, 2,width_ratios=(2, 1),height_ratios=(2, 1),
    left=0.1, right=0.98, bottom=0.1, top=0.98,hspace=0.1, wspace=0.05)

ax_ul = fig.add_subplot(gs[0, 0])
ax_ur = fig.add_subplot(gs[0, 1])
ax_ll = fig.add_subplot(gs[1, 0])
ax_lr = plt.axes([0.82, 0.1, 0.05, 0.2])

# 坐标
xlims = (0, Lx)
ylims = (0, Ly)
zlims = (-Lz, 0)

# 刻度
from matplotlib.ticker import MultipleLocator
xspacing = 25
yspacing = 25
zspacing = 20
xmaxLocator = MultipleLocator(xspacing)
ymaxLocator = MultipleLocator(yspacing)
zmaxLocator = MultipleLocator(zspacing)

# 等值线
from matplotlib import cm
cmap_w = cm.get_cmap('RdYlBu_r')
w_min = np.min(w)
w_max = np.max(w)
levels_w = np.linspace(-0.05, 0.05, 10)

# xy截面
ax_ul.set_aspect('equal')
cax=ax_ul.contourf(x3d[iz_crs, :, :], y3d[iz_crs, :, :], w[iz_crs, :, :],
        levels=levels_w, cmap=cmap_w, extend='both')
ax_ul.set_ylabel('y (m)')
ax_ul.xaxis.set_major_locator(xmaxLocator)
ax_ul.yaxis.set_major_locator(ymaxLocator)
ax_ul.set_xlim(xlims)
ax_ul.set_ylim(ylims)
ax_ul.set_xticklabels([])

# xz截面
ax_ll.contourf(x3d[:, iy_crs, :], z3d[:, iy_crs, :], w[:, iy_crs, :],
    levels=levels_w, cmap=cmap_w, extend='both')
ax_ll.set_xlabel('x (m)')
ax_ll.set_ylabel('z (m)')
ax_ll.xaxis.set_major_locator(xmaxLocator)
ax_ll.yaxis.set_major_locator(zmaxLocator)
ax_ll.set_xlim(xlims)
ax_ll.set_ylim(zlims)

# yz截面
ax_ur.contourf(z3d[:, :, ix_crs], y3d[:, :, ix_crs], w[:, :, ix_crs],
    levels=levels_w, cmap=cmap_w, extend='both')
ax_ur.set_xlabel('z (m)')
ax_ur.xaxis.set_major_locator(zmaxLocator)
ax_ur.yaxis.set_major_locator(ymaxLocator)
ax_ur.set_xlim(zlims)
ax_ur.set_ylim(ylims)
ax_ur.set_yticklabels([])
ax_ur.invert_xaxis() 

# 色阶图
cbar = fig.colorbar(cax, cax=ax_lr, ticks=levels_w[::5])
cbar.ax.set_title("w (m/s)", ha='center', va='bottom')

