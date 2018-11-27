from PIL import Image
import numpy as np

def SNR(narr, arr):
	return 10*np.log10(np.var(arr)/np.var(np.subtract(narr,arr)))

methods = ['box3', 'box5', 'median3', 'median5', 'open-close', 'close-open']
inputs = ['gauss_10.bmp', 'gauss_30.bmp', 'SandP_05.bmp', 'SandP_10.bmp']
im = Image.open('lena.bmp')
arr = np.array(im)
im.close()
for inName in inputs:
	print(inName)
	im1 = Image.open(inName)
	arr1 = np.array(im1)
	im1.close()
	R, C = len(arr1), len(arr1[0])
	print('    unmodified', SNR(arr1, arr))
	for method in methods:
		im2 = Image.open(inName[0:-4]+method+'.bmp')
		arr2 = np.array(im2)
		im2.close()
		print('    '+method, SNR(arr2,arr))