"""
import numpy as np

a = np.array([[1,2],[3,4]])
b = np.array([[17,19],[23,29]])

print(a*b)

c = np.pad(a, ((5,5),(5,5)), 'constant', constant_values=(0,0))
print(c)
d = c[5:5+2, 6:6+2]
print(d)
"""

from PIL import Image
import numpy as np

laplace1 = (1, 1, np.array([[0,1,0],[1,-4,1],[0,1,0]]))
laplace2 = (1, 3, np.array([[1,1,1],[1,-8,1],[1,1,1]]))
mv_laplace = (1, 3, np.array([[2,-1,2],[-1,-4,-1],[2,-1,2]]))

laplace_G = (5, 1,np.array(\
[[0,0,0,-1,-1,-2,-1,-1,0,0,0],\
[0,0,-2,-4,-8,-9,-8,-4,-2,0,0],\
[0,-2,-7,-15,-22,-23,-22,-15,-7,-2,0],\
[-1,-4,-15,-24,-14,-1,-14,-24,-15,-4,-1],\
[-1,-8,-22,-14,52,103,52,-14,-22,-8,-1],\
[-2,-9,-23,-1,103,178,103,-1,-23,-9,-2],\
[-1,-8,-22,-14,52,103,52,-14,-22,-8,-1],\
[-1,-4,-15,-24,-14,-1,-14,-24,-15,-4,-1],\
[0,-2,-7,-15,-22,-23,-22,-15,-7,-2,0],\
[0,0,-2,-4,-8,-9,-8,-4,-2,0,0],\
[0,0,0,-1,-1,-2,-1,-1,0,0,0]]))


Gauss1 = np.array(\
[[    0,    0,    0,    0,    1,     1,    1,    0,    0,    0,    0],\
[     0,    0,    1,   14,   55,    88,   55,   14,    1,    0,    0],\
[     0,    1,   36,  362, 1445,  2289, 1445,  362,   36,    1,    0],\
[     0,   14,  362, 3672,14648, 23204,14648, 3672,  362,   14,    0],\
[     1,   55, 1445,14648,58433, 92564,58433,14648, 1445,   55,    1],\
[     1,   88, 2289,23204,92564,146632,92564,23204, 2289,   88,    1],\
[     1,   55, 1445,14648,58433, 92564,58433,14648, 1445,   55,    1],\
[     0,   14,  362, 3672,14648, 23204,14648, 3672,  362,   14,    0],\
[     0,    1,   36,  362, 1445,  2289, 1445,  362,   36,    1,    0],\
[     0,    0,    1,   14,   55,    88,   55,   14,    1,    0,    0],\
[     0,    0,    0,    0,    1,     1,    1,    0,    0,    0,    0]])


Gauss3 = np.array(\
[[  1283,  2106,  3096,  4077,  4809,  5081,  4809,  4077,  3096,  2106,  1283],\
[   2106,  3456,  5081,  6691,  7892,  8339,  7892,  6691,  5081,  3456,  2106],\
[   3096,  5081,  7469,  9836, 11602, 12258, 11602,  9836,  7469,  5081,  3096],\
[   4077,  6691,  9836, 12952, 15277, 16142, 15277, 12952,  9836,  6691,  4077],\
[   4809,  7892, 11602, 15277, 18020, 19040, 18020, 15277, 11602,  7892,  4809],\
[   5081,  8339, 12258, 16142, 19040, 20117, 19040, 16142, 12258,  8339,  5081],\
[   4809,  7892, 11602, 15277, 18020, 19040, 18020, 15277, 11602,  7892,  4809],\
[   4077,  6691,  9836, 12952, 15277, 16142, 15277, 12952,  9836,  6691,  4077],\
[   3096,  5081,  7469,  9836, 11602, 12258, 11602,  9836,  7469,  5081,  3096],\
[   2106,  3456,  5081,  6691,  7892,  8339,  7892,  6691,  5081,  3456,  2106],\
[  1283,  2106,  3096,  4077,  4809,  5081,  4809,  4077,  3096,  2106,  1283]])


difference_G = (5, 1000000, np.subtract(Gauss3, Gauss1))






im = Image.open('lena.bmp')
(C,R), arr = im.size, np.pad(np.array(im), ((5,5),(5,5)), 'constant', constant_values=(0,0))
im.close()

def setWhite1(value, r, c, threshold):
	return True if value[r][c]<=threshold else False

"""
def setWhite2(value, r, c, threshold):
	if r>0 and np.absolute(value[r][c]-value[r-1][c])>threshold:
		return False
	if r<(R-1) and np.absolute(value[r][c]-value[r+1][c])>threshold:
		return False
	if c>0 and np.absolute(value[r][c]-value[r][c-1])>threshold:
		return False
	if c<(C-1) and np.absolute(value[r][c]-value[r][c+1])>threshold:
		return False
	return True
"""

def generatePicture(name, ker, threshold, setWhite):
	value = np.zeros((R,C), dtype=np.float32)
	ret = np.zeros((R,C), dtype=np.uint8)
	for r in range(5, 5+R):
		for c in range(5, 5+C):
			value[r-5][c-5] = sum((arr[r-ker[0]:r+ker[0]+1, c-ker[0]:c+ker[0]+1] * ker[2]).flatten()) / ker[1]
	for r in range(R):
		for c in range(C):
			ret[r][c] = 255 if setWhite(value, r, c, threshold) else 0
	Image.fromarray(ret).save(name)

generatePicture('laplace1.bmp', laplace1, 30, setWhite1)
generatePicture('laplace2.bmp', laplace2, 20, setWhite1)
generatePicture('min_var_laplace.bmp', mv_laplace, 20, setWhite1)
generatePicture('laplace_gauss.bmp', laplace_G, 6000, setWhite1)
generatePicture('difference_gauss.bmp', difference_G, 6, setWhite1)