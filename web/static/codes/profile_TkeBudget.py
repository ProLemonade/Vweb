# 某时刻，垂直剖面：TKE

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
TKE = ncid.variables['TKE'][:,::-1,0,0]
ncid.close()

fn = f + "Average.nc"
ncid = Dataset(fn)
ncid.variables
U = ncid.variables['U'][:,::-1][:,:Nz]
V = ncid.variables['V'][:,::-1][:,:Nz]
W = ncid.variables['W'][:,::-1][:,:Nz]
P = ncid.variables['P'][:,::-1][:,:Nz]
Tₐ = ncid.variables['Tₐ'][:,::-1][:,:Nz]
ncid.close()

fn = f + "twoOrder_A.nc"
ncid = Dataset(fn)
ncid.variables
uuA = ncid.variables['u²A'][:,::-1][:,:Nz]
vvA = ncid.variables['v²A'][:,::-1][:,:Nz]
wwA = ncid.variables['w²A'][:,::-1][:,:Nz]
uwA = ncid.variables['uwA'][:,::-1][:,:Nz]
vwA = ncid.variables['vwA'][:,::-1][:,:Nz]
uvA = ncid.variables['uvA'][:,::-1][:,:Nz]
pwA = ncid.variables['pwA'][:,::-1][:,:Nz]
TwA = ncid.variables['TwA'][:,::-1][:,:Nz]
uτ13A = ncid.variables['uτ13A'][:,::-1][:,:Nz]
vτ23A = ncid.variables['vτ23A'][:,::-1][:,:Nz]
wτ33A = ncid.variables['wτ33A'][:,::-1][:,:Nz]
ncid.close()

fn = f + "threeOrder_A.nc"
ncid = Dataset(fn)
uuwA = ncid.variables['uuwA'][:,::-1][:,:Nz]
vvwA = ncid.variables['vvwA'][:,::-1][:,:Nz]
wwwA = ncid.variables['wwwA'][:,::-1][:,:Nz]
ncid.close()

fn = f + "threeOrder_A.nc"
ncid = Dataset(fn)
uuwA = ncid.variables['uuwA'][:,::-1][:,:Nz]
vvwA = ncid.variables['vvwA'][:,::-1][:,:Nz]
wwwA = ncid.variables['wwwA'][:,::-1][:,:Nz]
ncid.close()

fn = f + "oneOrder_tau_A.nc"
ncid = Dataset(fn)
#τ11A = ncid.variables['τ₁₁A'][:,::-1][:,:Nz]
τ12A = ncid.variables['τ₁₂A'][:,::-1][:,:Nz]
τ13A = ncid.variables['τ₁₃A'][:,::-1][:,:Nz]
#τ22A = ncid.variables['τ₂₂A'][:,::-1][:,:Nz]
τ23A = ncid.variables['τ₂₃A'][:,::-1][:,:Nz]
τ33A = ncid.variables['τ₃₃A'][:,::-1][:,:Nz]
ncid.close()

fn = f + "oneOrder_strainRate_A.nc"
ncid = Dataset(fn)
#S11_opA = ncid.variables['S₁₁_opA'][:,::-1][:,:Nz]
S12_opA = ncid.variables['S₁₂_opA'][:,::-1][:,:Nz]
S13_opA = ncid.variables['S₁₃_opA'][:,::-1][:,:Nz]
#S22_opA = ncid.variables['S₂₂_opA'][:,::-1][:,:Nz]
S23_opA = ncid.variables['S₂₃_opA'][:,::-1][:,:Nz]
S33_opA = ncid.variables['S₃₃_opA'][:,::-1][:,:Nz]
ncid.close()

# 计算
H=80
u10=8
cᴰʷ=(0.75+0.067*u10)*1e-3 
α=1.67e-4
ρₐ=1.225
ρₒ=1026.0
Qᵘ=-ρₐ/ρₒ*cᴰʷ*u10*abs(u10)
ustar=np.sqrt(np.abs(Qᵘ))
g=9.80 
amplitude = 0.88
wavelength = 50
wavenumber = 2*np.pi / wavelength
frequency = np.sqrt(g * wavenumber)
dtime = 120

# TKE Ri
dTKEdt=np.gradient(TKE[:,:],dtime,axis=0)/(ustar ** 3/H)
Uz=np.gradient(U,z,axis=1)
Vz=np.gradient(V,z,axis=1)
Wz=np.gradient(W,z,axis=1)
Tz=np.gradient(Tₐ,z,axis=1)
Ri=g*α*Tz/(Uz*Uz+Vz*Vz)

# 𝑆k : Stokes 漂移生产项。
Us=amplitude**2*frequency*wavenumber
us = Us*np.cosh(2*wavenumber*(z+H))/(2*(np.sinh(wavenumber*H))**2)
dusdz = Uˢ * wavenumber * np.sinh(2 * wavenumber * (z+H))/(np.sinh(wavenumber*H))**2
Sk = -(uwA - U*W) * dusdz / (ustar**3 / H)

# Pk : 剪切生产项
Pk1=((uwA-(U-us)*W)+τ13A)*Uz
Pk2=((vwA-V*W)+τ23A)*Vz
Pk3=((wwA-W*W)+τ33A)*Wz
Pk=-(Pk1+Pk2)/(ustar**3/H)-Sk

# B: 浮力生产项。
B=α*g*(TwA-W*Tₐ )/(ustar**3/H)

# 𝑇 :湍流输运项 
T1=uuwA-2*U*uwA+2*U*U*W-W*uuA  #u'u'w'=uuw−2Uuw+UUw−uuW+2UuW−UUW
T2=vvwA-2*V*vwA+2*V*V*W-W*vvA
T3=wwwA-2*W*wwA+2*W*W*W-W*wwA
dTdz=np.gradient(T1+T2+T3,z,axis=1)
T=-0.5*dTdz/(ustar**3/H)

# Π: 压力输运项
dPWdz=np.gradient((pwA-P*W)*1000,z,axis=1)
Π=-dPWdz/ρₒ/(ustar**3/H)

# 𝐷𝑘: 黏性耗散项
uτ=uτ13A-U*τ13A
vτ=vτ23A-V*τ23A
wτ=wτ33A-W*τ33A
dDdz=np.gradient((uτ+vτ+wτ),z,axis=1)
Dk=dDdz/(ustar**3/H)

# ϵ: 湍流耗散项
ϵ = -dTKEdt+Pk+Sk+B+T+Π+Dk


import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib import cm
from matplotlib.colors import LogNorm
from matplotlib import font_manager


def ave_t(value,point):
    total=np.zeros(80)
    for i in range(point-7,point+8):
        total+=value[i,:]
    ave_t=total/15.0
    return ave_t

def ave_z(value,point):
    total=np.zeros(80)
    for i in range(point-7,point+8):
        total+=value[:,i]
    ave_z=total/15.0
    return ave_z

# 画图
fig=plt.figure(figsize=(5,6))
gs=fig.add_gridspec(1,1,left=0.05,right=0.90,bottom=0.12,top=0.96,hspace=0.2,wspace=0.1)

tp=-1

ax=fig.add_subplot(gs[0])
ax_TKE_Pk=ax.plot(ave_t(Pk,tp),z,label='Pk')
ax_TKE_Sk=ax.plot(ave_t(Sk,tp),z,label='Sk')
ax_TKE_B=ax.plot(ave_t(B,tp),z,label='B')
ax_TKE_T=ax.plot(ave_t(T,tp),z,label='T')
ax_TKE_Π=ax.plot(ave_t(Π,tp),z,label='Π')
ax_TKE_Dk=ax.plot(ave_t(Dk,tp),z,label='Dk')
ax_TKE_ϵ=ax.plot(ave_t(-ϵ,tp),z,label='ϵ')

ax.set_title('TKE BUDGET')
ax.set_xlabel(r'$\partial k /\partial t /[u_*^3/H]$')
ax.set_ylabel('Z(m)')
plt.xscale('symlog')
ax.set_ylim((-H,0))
ax.legend(loc="upper left")
