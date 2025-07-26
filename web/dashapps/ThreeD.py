import os
from django.conf import settings

import dash
import numpy as np
import pandas as pd
# from skimage import io
from django_plotly_dash import DjangoDash

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

# 函数

# 提取text文件数据 return origin,name,x,y,z,u,v,w,T
def txt_data_get(file):
    import numpy as np
    i=1
    origin=[]
    with open("%s"%file, "r")  as fid:
        for ele in fid:    #读取文档
            if i<=6:       #前六行为元数据
                info=ele.strip('\n')
                info=info.split('=') # 按照分割符分割字符串
                origin=origin+[info[1]] #将元数据存入列表
            else: #第七行为要素量名称
                name=ele.split()
                break
            i=i+1
    # 读取格点数据
    x = np.loadtxt("%s"%file, skiprows=7, usecols=0)
    y = np.loadtxt("%s"%file, skiprows=7, usecols=1)
    z = np.loadtxt("%s"%file, skiprows=7, usecols=2)
    u = np.loadtxt("%s"%file, skiprows=7, usecols=3)
    v = np.loadtxt("%s"%file, skiprows=7, usecols=4)
    w = np.loadtxt("%s"%file, skiprows=7, usecols=5)
    T = np.loadtxt("%s"%file, skiprows=7, usecols=6)
    Nx=int(origin[3])
    Ny=int(origin[4])
    Nz=int(origin[5])
    #改变格点数据维度
    x=x.reshape(Nz,Ny,Nx)
    y=y.reshape(Nz,Ny,Nx)
    z=z.reshape(Nz,Ny,Nx)
    u=u.reshape(Nz,Ny,Nx)
    v=v.reshape(Nz,Ny,Nx)
    w=w.reshape(Nz,Ny,Nx)
    T=T.reshape(Nz,Ny,Nx)
    return origin,name,x,y,z,u,v,w,T
# 3D切片图（动态） return fig
def frame_args(duration):
    return {
            "frame": {"duration": duration},
            "mode": "immediate",
            "fromcurrent": True,
            "transition": {"duration": duration, "easing": "linear"},
    }
def slice(volume,Lz,cb_min,cb_max):
    import numpy as np
    import plotly.express as px
    import plotly.graph_objects as go
    # 获取数据维度
    Nx=volume[0].shape[0]
    Ny=volume[0].shape[1]
    Nz=volume.shape[0]
    # Define frames (通过数据维度Nz与输入水深Lz调节得到绘图纵轴z)
    fig=go.Figure(
        frames=[
            go.Frame( # 通过变化的k选取数据作为展示层
                data=go.Surface(
                    z=-k/Nz*Lz*np.ones((Nx, Ny)),
                    surfacecolor=np.flipud(volume[k]),
                    cmin=cb_min,
                    cmax=cb_max),
                name=str(k))
            for k in range(Nz)])   # 变化的k
    # Axis 分别标记4个标签值 为纵轴添加单位m
    fig.update_layout(
        scene=dict(
            xaxis=dict(nticks=5, range=[0,Nx]),
            yaxis=dict(nticks=5, range=[0,Ny]),
            zaxis=dict(nticks=5, range=[0,Lz]),),
        autosize=True,
        margin=dict(r=20, l=20, b=20, t=20))
    fig.update_layout(
        scene=dict(
            xaxis_title='x',
            yaxis_title='y',
            zaxis_title='z (m)'))
    # Add data to be displayed before animation starts (1/3水深处)
    fig.add_trace(
        go.Surface(
            z=-Lz/3*np.ones((Nx, Ny)),
            surfacecolor=np.flipud(volume[int(Lz/3)]),
            colorscale='YlGnBu',
            cmin=cb_min,
            cmax=cb_max,
            colorbar=dict(thickness=20, ticklen=5)))
    sliders=[{"pad": {"b": 10, "t": 60},
                "len": 0.9,
                "x": 0.1,
                "y": 0,
                "steps": [{
                    "args": [[f.name], frame_args(0)],
                    "label": str(int(-k/Nz*Lz)),
                    "method": "animate", }
                for k, f in enumerate(fig.frames)]}]
    fig.update_layout(
        autosize=True,
        scene=dict(   # 切片上下滑动
            zaxis=dict(range=[-Lz, 0], autorange=False),
            aspectratio=dict(x=1, y=1, z=1),),
        updatemenus=[{ # 播放和停止
            "buttons":[
               {"args": [None, frame_args(50)],
                "label": "&#9654;",
                "method":"animate"},
               {"args": [[None], frame_args(0)],
                "label": "&#9724;", # pause symbol
                "method": "animate"}],
            "direction": "left",
            "pad": {"r": 10, "t": 70},
            "type": "buttons",
            "x": 0.1,
            "y": 0,}],
        sliders=sliders)
    return fig
# 求层平均  Vertical distribution of..
def layer_average(volume):
    import numpy as np
    Nz=volume.shape[0]
    average = np.array([])
    for i in range(0,Nz):
        layer=volume[i]
        layer_average=np.mean(layer)
        average=np.append(average,layer_average)
    return average
# 求层方差 Vertical distribution : Variance values of..
def layer_var(volume):
    import numpy as np
    Nz=volume.shape[0]
    var = np.array([])
    for i in range(0,Nz):
        layer=volume[i]
        layer_var=np.var(layer)
        var=np.append(var,layer_var)
    return var
# 计算湍流动能 Vertical distribution : Turbulent kinetic energy
def layer_e(u_var,v_var,w_var):
    e=0.5*(u_var**2+v_var**2+w_var**2)
    return e
# 寻找切片数据
def cut(volumn,derection,locations,location,near):
    # 输入三维数据 切片方向 可切范围 切片位置 位置误差
    i=1
    for l in locations:
        if abs(l-location)<near:
            number=i
            break
        i=i+1
    if derection=='z':
        data=volumn[number, :, :]
    elif derection=='x':
        data=volumn[:, number, :]
    elif  derection=='y':
        data=volumn[:, :, number]
    return data


import os
from django.conf import settings

# 添加这些调试信息
wind_file = os.path.join(settings.BASE_DIR, 'web', 'static', 'data', 'threeD_wind.txt')
windWave_file = os.path.join(settings.BASE_DIR, 'web', 'static', 'data', 'threeD_windWave.txt')

print(f"Wind file exists: {os.path.exists(wind_file)}")
print(f"WindWave file exists: {os.path.exists(windWave_file)}")
print(f"Wind file path: {wind_file}")
print(f"WindWave file path: {windWave_file}")

try:
    wind = txt_data_get(wind_file)
    windWave = txt_data_get(windWave_file)
    print("Data files loaded successfully")
except Exception as e:
    print(f"Error loading data files: {e}")

OML_wind=dict(zip(wind[1],wind[2:]))    #将文档数据以要素量名称为key存入字典
OML_windWave=dict(zip(windWave[1],windWave[2:]))
Lx=int(wind[0][0])
Ly=int(wind[0][1])
Lz=int(wind[0][2])
Nx=int(wind[0][3])
Ny=int(wind[0][4])
Nz=int(wind[0][5])
alldata={'u Without Wind':OML_wind['u(m/s)'],'u With Wind':OML_windWave['u(m/s)'],
         'v Without Wind':OML_wind['v(m/s)'],'v With Wind':OML_windWave['v(m/s)'],
         'w Without Wind':OML_wind['w(m/s)'],'w With Wind':OML_windWave['w(m/s)'],
         'T Without Wind':OML_wind['T(K)'],'T With Wind':OML_windWave['T(K)'],
         'x':OML_wind['x(m)'],
         'y':OML_wind['y(m)'],
         'z':OML_wind['z(m)']}

# 导入绘图模块
import plotly.graph_objs as go  # 绘图
from dash.dependencies import Input, Output # 回调
import dash_core_components as dcc  # 交互式组件
import dash_html_components as html # 代码转html
import dash_bootstrap_components as dbc

fig_names=['w Without Wind','w With Wind']

# 动态切片图
app_1 = DjangoDash('threeD_Ani', external_stylesheets=external_stylesheets)
app_1.layout = html.Div(
    children=[
        dcc.Dropdown(
            id='dropdown1',
            options=[{'label': x, 'value': x} for x in fig_names],
            value='w Without Wind',
            multi=False,
            ),
        dcc.Graph(
            id="graph1",
            style={
                'height': '100%',
                'width': '100%',
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center'
            }
        ),
        html.Br()])


@app_1.callback(
    dash.dependencies.Output('graph1', 'figure'),
    [dash.dependencies.Input('dropdown1', 'value')])
def update_graph1(selected_column1):
    try:
        print(f"Callback triggered with: {selected_column1}")

        if selected_column1 not in alldata:
            print(f"Selected column not found in alldata. Available keys: {list(alldata.keys())}")
            return go.Figure()  # 返回空图

        data1 = alldata[selected_column1]
        print(f"Data shape: {data1.shape}")
        print(f"Data type: {type(data1)}")

        fig1 = slice(data1, Lz, -0.02, 0.02)
        print("Figure created successfully")
        return fig1

    except Exception as e:
        print(f"Error in callback: {e}")
        import traceback
        traceback.print_exc()
        return go.Figure()  # 返回空图

#静态图
app_2 = DjangoDash('threeD', external_stylesheets=external_stylesheets)
app_2.layout = html.Div(
    children=[
        dcc.Dropdown(
            id='dropdown2',
            options=[{'label': x, 'value': x} for x in fig_names],
            value='w With Wind',
            multi=False,),
        dcc.Graph(id="graph2",
            style={
                'height': '100%',
                'width': '100%',
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center'
            }),
        html.Br()])
@app_2.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('dropdown2', 'value')])
def update_graph2(selected_column2):
    data2 = alldata[selected_column2]
    Nx=data2[0].shape[0]
    Ny=data2[0].shape[1]
    Nz=data2.shape[0]
    z1 = np.array(data2[0, :, :])
    z2 = np.array(data2[int(Nz*1/3), :, :])
    z3 = np.array(data2[int(Nz*2/3), :, :])
    fig2 = go.Figure(data=[
        go.Surface(z=z1,showscale=False, opacity=1,colorscale='YlGnBu',cmin=-0.02, cmax=0.02),
        go.Surface(z=z2-Lz*1/3, showscale=False, opacity=1,colorscale='YlGnBu'),
        go.Surface(z=z3-Lz*2/3, showscale=False, opacity=1,colorscale='YlGnBu')])
    fig2.update_layout(
                  autosize=True,
                  margin=dict(l=10,r=10,b=10,t=10))  # 4个位置的距离
    fig2.update_layout(scene_aspectmode='cube')
    fig2.update_layout(
            scene=dict(
                xaxis=dict(nticks=4, range=[0,Nx]),
                yaxis=dict(nticks=4, range=[0,Ny]),
                zaxis=dict(nticks=4, range=[-Lz,1])))
    return fig2

