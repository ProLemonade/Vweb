# 时间平均,垂直剖面;某深处,时间序列:TKE

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

TKE_mean_time = np.mean(TKE[:,:], axis=0)

# 最值位置
zi_1 = np.argmax(TKE_mean_time)
zi_2 = np.argmax(TKE_mean_time[int(Nz/2):])+int(Nz/2)
zi_3 = np.argmin(TKE_mean_time[zi_1:zi_2])

TKE1 = TKE[:, zi_1]
TKE2 = TKE[:, zi_2]
TKE3 = TKE[:, zi_3]

# 画图
import matplotlib.pyplot as plt
fig = plt.figure(figsize=(14, 6))

ax1 = plt.subplot2grid((1, 4), (0, 0), colspan=1)
ax1.plot(TKE_mean_time, z)
ax1.axhline(y=z[zi_1], color='blue', linestyle='--')
ax1.axhline(y=z[zi_2], color='orange', linestyle='--')
ax1.axhline(y=z[zi_3], color='black', linestyle='--')
ax1.set_xlabel("TKE")
ax1.set_ylabel("Depth(m)")
ax1.set_title("Vertical Profile")
ax1.grid()
ax1.legend()

ax2 = plt.subplot2grid((1, 4), (0, 1), colspan=3)
ax2.plot(time/3600, TKE1, label=f"Depth = {z[zi_1]:.2f}m", color="blue")
ax2.plot(time/3600, TKE2, label=f"Depth = {z[zi_2]:.2f}m", color="orange")
ax2.plot(time/3600, TKE3, label=f"Depth = {z[zi_3]:.2f}m", color="black")
ax2.set_xlabel("Time")
ax2.set_ylabel("TKE")
ax2.set_title("Time Series")
ax2.grid()
ax2.legend(loc='upper right')

#plt.show()

