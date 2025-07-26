# 时间序列图：KE TKE

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
W = ncid.variables['W'][:,::-1][:,:Nz]
ncid.close()

fn = f + "TKE.nc"
ncid = Dataset(fn)
TKE = ncid.variables['TKE'][:,::-1,0,0]
ncid.close()

KE = np.mean( 0.5 * (U**2 + V**2 + W**2), axis=1)
TKE = np.mean( TKE , axis=1)

# 画图
import numpy as np
import matplotlib.pyplot as plt

fig, ax1 = plt.subplots(figsize=(10, 6))

ax1.plot(time/3600, KE, color='blue', label='KE')
ax1.set_xlabel('Time (hours)')
ax1.set_ylabel('KE (m²/s²)', color='blue')
ax1.set_ylim(0, max(KE)*1.2)
ax1.tick_params(axis='y', labelcolor='blue')

ax2 = ax1.twinx()
ax2.plot(time/3600, TKE, color='red', label='TKE')
ax2.set_ylabel('TKE (m²/s²)', color='red')
ax2.tick_params(axis='y', labelcolor='red')

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

plt.title('Time Evolution of KE and TKE')
#plt.show()