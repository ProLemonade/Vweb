# 某时刻，水平平均，垂直剖面：uvwT

f = "D:/Example/"

# 读取
import numpy as np
from netCDF4 import Dataset
fn = f + "field.nc"
ncid = Dataset(fn)
z = ncid.variables['zC'][::-1]
Nz = z.shape[0]
ncid.close()

fn = f + "Average.nc"
ncid = Dataset(fn)
ncid.variables
U = ncid.variables['U'][:,::-1][:,:Nz]
V = ncid.variables['V'][:,::-1][:,:Nz]
W = ncid.variables['W'][:,::-1][:,:Nz]
P = ncid.variables['P'][:,::-1][:,:Nz]
Tₐ = ncid.variables['Tₐ'][:,::-1][:,:Nz]

# 某时刻
t = -1
U = U[t, :]
V = V[t, :]
W = W[t, :]
T = Tₐ[t, :]

# 画图
import matplotlib as mpl
import matplotlib.pyplot as plt

figsize = (6, 12)
fig = plt.figure(figsize=figsize)
gs = fig.add_gridspec(2, 2,left=0.02, right=0.98, bottom=0.05, top=0.95, hspace=0.1, wspace=0.1)

ax_u = fig.add_subplot(gs[0, 0])
ax_v = fig.add_subplot(gs[0, 1])
ax_w = fig.add_subplot(gs[1, 0])
ax_T = fig.add_subplot(gs[1, 1])

ax_u.plot(U, z, color='C0', linestyle='--')
ax_u.set_xlabel("u(m/s)")
ax_u.set_ylabel("z(m)")

ax_v.plot(V, z, color='C0', linestyle='--')
ax_v.set_xlabel("v(m/s)")
ax_v.legend(loc="upper right")
ax_v.set_yticklabels([])

ax_w.plot(W, z, color='C0', linestyle='--')
ax_w.set_xlabel("w(m/s)")
ax_w.set_ylabel("z(m)")

ax_T.plot(T, z, color='C0', linestyle='--')
ax_T.set_xlabel("T(K)")
ax_T.set_yticklabels([])

plt.suptitle('Vertical distribution of u v w T')
#plt.show

