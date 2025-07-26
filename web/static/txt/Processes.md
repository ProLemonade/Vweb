# Depth
## Process Code
```
const H = 80
const Nz = H/0.5
grid = RectilinearGrid(GPU(),size=(100,100,80), extent=(100, 100, H))
```
## Process Application
筛选条件中，
Depth：
Deep → H = 80；
Middle → H = 40；
Shallow → H = 20。
Grid：
Coarse → (Lx/1,Ly/1,H/1)；
Middle → (Lx/1,Ly/1,H/0.5)；
Dense → (Lx/0.5,Ly/0.5,H/0.25)。
Bottom：
No → Flat；
Slope → slope_angle = 10*π/180。

# Coriolis
## Process Code
```
latitude=0
f=2*7.2921e-5*sin(latitude*π/180)
coriolis = FPlane(f)
```
## Process Application
筛选条件中：
HighLatitude → latitude=60；
MidLatitude → latitude=45；
LowLatitude → latitude=0。
## ProcessFormula
### f = 2\Omega \sin \phi
φ -- rad -- latitude -- 纬度
Ω -- rad/s -- Earth angular velocity -- 地球角速度~7.2921×10^(−5)rad/s  
f -- s⁻¹ -- Coriolis parameter -- 科里奥利参数

# Wind
## Process Code
```
const u₁₀=8  # m/s
const ρₐ=1.225  # kg/m³
const ρₒ=1026.0 # kg/m³
const cᴰʷ=(0.75+0.067*u₁₀)*1e-3
Qᵘ = -ρₐ/ρₒ*cᴰʷ*u₁₀*abs(u₁₀) # m²/s²
```
## Process Application
筛选条件中：
Waker → u₁₀=8;
Stronger → u₁₀=16。


## ProcessFormula
### \tau = \rho_a · c_d^w · u_{10}^2
ρₐ -- kg/m³ -- Average density of air at sea-level -- 海表附近空气密度  
cᴰʷ -- None -- Drag coefficient (dimensionless) -- 风阻系数  
u₁₀ -- m/s -- Average wind velocity 10 meters above the ocean -- 距海表10米高处平均风速  
τ -- N/m² -- Wind stress -- 风应力
### Q^u = -\frac{\rho_a}{\rho_o} · c_d^w · u_{10}^2 = -\frac{\tau}{\rho_o}
ρₒ -- kg/m³ -- Average density of the world ocean at the surface -- 海表平均密度  
Qᵘ -- N·m/kg=(m/s)² -- Friction velocity squared -- 水侧摩擦速度平方

# BottomDrag
## Process Code
```
κ = 0.4 
z₀ = 0.01 # m
z₁ = H/Nz/2 # m
@inline drag_u(x, y, t, u, v, p) = - p.cᴰᵇ * √(u^2 + v^2) * (u)
@inline drag_v(x, y, t, u, v, p) = - p.cᴰᵇ * √(u^2 + v^2) * (v)
drag_bc_u = FluxBoundaryCondition(drag_u, field_dependencies=(:u, :v), parameters=(; cᴰᵇ))
drag_bc_v = FluxBoundaryCondition(drag_v, field_dependencies=(:u, :v), parameters=(; cᴰᵇ))
```
## Process Application

## ProcessFormula
### c_d^b = \left( \frac{\kappa}{\ln(z_1/z_0)} \right)^2
κ -- None -- von Karman constant--冯卡曼常数 
z₀ -- m -- Bottom roughness length--底粗糙长度 
z₁ -- m --Height of nearest grid center above bottom-- 底网格中心高度
cᴰᵇ -- None -- Bottom Drag Coefficient -- 底剪切系数
### \tau_b^x = -\rho c_d^b |\mathbf{u}| u  /  \tau_b^y = -\rho c_d^b |\mathbf{u}| v
ρ -- kg/m³ -- Seawater density -- 海水密度 
|u| -- m/s -- Horizontal velocity magnitude -- 水平流速幅值 
u,v -- m/s -- Velocity components -- x/y方向流速 
τb--  kg/(m⋅s²)=N/m² -- Bottom Shear Stress --  底剪切应力
# Wave
## Process Code
```
amplitude = 0.88 # m
wavelength = 50  # m
const wavenumber = 2π / wavelength # m⁻¹
frequency = sqrt(g_Earth * wavenumber) # s⁻¹
const vertical_scale = wavelength / 4π 
const Uˢ = amplitude^2 * wavenumber * frequency # m s⁻¹
uˢ(z) = Uˢ * cosh(2*wavenumber*(z+H))/2*(sinh(wavenumber*H))^2
∂z_uˢ(z, t) = Uˢ * wavenumber * sinh(2 * wavenumber * (z+H))/(sinh(wavenumber*H))^2
```
## Process Application
筛选条件中：
Lower → amplitude = 0.88;
Higher → amplitude = 1.76。
利用函数定义Uˢ(z)：
表层（z ≈ 0），速度最大，cosh 函数主导，体现波浪对表层水体的直接驱动。
底层（z≈−H），速度趋近于零，满足无滑移边界条件（但在实际边界层中会因粘性产生剪切）。
深水（H→∞），公式此时呈  (z)∝e^2kz ，速度随深度指数衰减，能量局限于表层。
## ProcessFormula
### \sigma = \sqrt{g \cdot k} =\sqrt{g \cdot \frac{2\pi}{L}}
L -- m -- Wavelength -- 波长  
k -- m⁻¹ -- Wavenumber -- 波数  
g -- m/s² -- Gravitational acceleration -- 重力加速度  
σ -- s⁻¹ -- Wave angular frequency -- 波浪角频率  
### U^s = a^2 k \sigma
a -- m -- Wave amplitude -- 波幅  
Uˢ -- m/s -- Characteristic velocity -- 波浪特征速度  
### u^s(z) = U^s \frac{\cosh[2k(z+H)]}{2\sinh^2(kH)}
### \frac{\partial u^s}{\partial z} = U^s k \frac{\sinh[2k(z+H)]}{\sinh^2(kH)}

# Heat
## Process Code
```
const Qʰ = 50 # W m⁻²
const cᴾ = 4000.0 # J K⁻¹ kg⁻¹
const HA=800
const Tₛ=24hours
Qᵀ(x,y,t) =t < (2*((t ÷ Tₛ)+1)-1)*Tₛ/2 && t > (((t ÷ Tₛ)+1)-1)*Tₛ ? (-HA*sin(t*π/12hours)+Qʰ) / (ρₒ * cᴾ) : Qʰ/(ρₒ * cᴾ)
```
## Process Application
利用分段函数定义Qᵀ：以周期Tₛ=24hours为界，温度变化Qᵀ或Qᵀ+sin…
## ProcessFormula
### Q^T=\frac{Q^h}{\rho_0 c^P}
Qʰ  -- W/m²  (J/(s·m²))  -- Surface heat flux -- 海表热通量
ρₒ  -- kg/m³   -- Density -- 海水密度
cᴾ  -- J/(kg·K)   -- Specific heat capacity -- 海水比热容
Qᵀ -- m·K/s  -- Temperature change rate  -- 温度变化率(单位深度下)

### \begin{equation*} Q^T(x,y,t) = \begin{cases} \frac{-HA \sin\left(\frac{\pi t}{12\,\text{hours}}\right) + Q^h}{\rho_0 c^P}, & \text{if } \tau < \frac{T_s}{2}, \\[1em] \frac{Q^h}{\rho_0 c^P}, & \text{if } \tau \geq \frac{T_s}{2}. \end{cases} \end{equation*}


# Tide
## Process Code
```
const period = 24hours
const σ=2*π/period
const Uₘₐⱼ=0.25 #m/s
const Uₘᵢₙ=0.25  #m/s
const Γ=0 #direction angle of the major axis
const ψ=0 #initial angle
const ϕ=atan(Uₘₐⱼ*sin(ψ-Γ)/(Uₘᵢₙ*cos(ψ-Γ)))
Fx(x,y,z,t)=((f+σ)*(Uₘₐⱼ+Uₘᵢₙ)*(-sin(σ*t+ϕ+Γ))+(f-σ)*(Uₘₐⱼ-Uₘᵢₙ)*(-sin(-σ*t-ϕ+Γ)))/2
Fy(x,y,z,t)=((f+σ)*(Uₘₐⱼ+Uₘᵢₙ)*(cos(σ*t+ϕ+Γ))+(f-σ)*(Uₘₐⱼ-Uₘᵢₙ)*(cos(-σ*t-ϕ+Γ)))/2
```
## ProcessFormula
### \phi = \arctan\left( \frac{U_{\mathrm{maj}} \sin(\psi-\Gamma)}{U_{\mathrm{min}} \cos(\psi-\Gamma)} \right )
### F_x = \frac{(f+\sigma)(U_{\mathrm{maj}}+U_{\mathrm{min}})(-\sin(\sigma t+\phi+\Gamma)) + (f-\sigma)(U_{\mathrm{maj}}-U_{\mathrm{min}})(-\sin(-\sigma t-\phi+\Gamma))}{2}
### F_y = \frac{(f+\sigma)(U_{\mathrm{maj}}+U_{\mathrm{min}})\cos(\sigma t+\phi+\Gamma) + (f-\sigma)(U_{\mathrm{maj}}-U_{\mathrm{min}})\cos(-\sigma t-\phi+\Gamma)}{2}
## Process Application

# Initial
## Process Code
```
initial_mixed_layer_depth=0
stratification(z) = z < - initial_mixed_layer_depth ? dTdz * z : dTdz * (-initial_mixed_layer_depth)
Tᵢ(x,y,z)=stratification(z)+1e-8*Ξ(z)+290
Sᵢ=35 #PSU
Ξ(z) = randn()*exp(z/4)
uᵢ(x, y, z) = 1e-4*Ξ(z)
vᵢ(x, y, z) = 1e-4*Ξ(z)
wᵢ(x, y, z) = 1e-4*Ξ(z)
```
## Process Application
利用分段函数定义Tᵢ，再加上一些初始扰动。
## ProcessFormula
### \begin{equation*} T =  \begin{cases}  dT_{dz} \cdot z, & z < -D_{mix} \\ dT_{dz} \cdot D_{mix}, & \text{otherwise} \end{cases} \end{equation*}