from PIL import Image
import numpy as np

def toInt(a):
	if a >= 255: return 255
	elif a <= 0: return 0
	return round(a)

def gauss(val, arg):
	return toInt(val + arg[0]*np.random.normal(0,1))

def SandP(val, arg):
	x = np.random.uniform(0, 1)
	if x < arg[0]: return 0
	elif x > arg[1]: return 255
	return val

def generateImage(name, method, arg):
	tmparr = np.zeros((R,C), dtype=np.uint8)
	for r in range(R):
		for c in range(C):
			tmparr[r][c] = method(arr[r][c], arg)
	Image.fromarray(tmparr).save(name)

im = Image.open('lena.bmp')
arr = np.array(im)
im.close()
R, C = len(arr), len(arr[0])

generateImage('gauss_10.bmp', gauss, [10])
generateImage('gauss_30.bmp', gauss, [30])
generateImage('SandP_05.bmp', SandP, [0.05, 0.95])
generateImage('SandP_10.bmp', SandP, [0.1, 0.9])