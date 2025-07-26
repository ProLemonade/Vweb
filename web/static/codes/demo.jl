# 测试

using Plots

x = 0:0.1:10
y = [sin.(x), cos.(x)]
plot(x, y, linewidth=1, size=(600,300))

