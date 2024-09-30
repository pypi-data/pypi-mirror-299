from numpy_typing import np, ax



a:np.float32_2d[ax.x, ax.y] = np.array([[[1,2,3],[4,5,6]],[[7,8,9],[10,11,12]]], dtype = np.float32)
b = a[[0, 1], :]

c = np.add(a, b)
print(c)