import numpy as np

a = np.random.randn(9, 6)
print(a)
print('\n')
print(np.linalg.pinv(a))
