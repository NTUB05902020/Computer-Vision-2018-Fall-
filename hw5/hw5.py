from PIL import Image
import numpy as np

K = [(-2,-1),(-2,0),(-2,1),\
(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),\
(0,-2),(0,-1),(0,0),(0,1),(0,2),\
(1,-2),(1,-1),(1,0),(1,1),(1,2),\
(2,-1),(2,0),(2,1)]



im = Image.open('lena.bmp')
(width,height), data_array = im.size, np.array(im)

def dilate(arr):
	ret = np.zeros((height, width), dtype=np.uint8)
	for r in range(height):
		for c in range(width):
			for r2,c2 in K:
				try: ret[r][c] = max(ret[r][c], arr[r-r2][c-c2])
				except IndexError: continue
	return ret
def erose(arr):
	ret = np.full((height, width), 255, dtype=np.uint8)
	for r in range(height):
		for c in range(width):
			for r2,c2 in K:
				try: ret[r][c] = min(arr[r+r2][c+c2], ret[r][c])
				except IndexError: continue
	return ret
Image.fromarray(dilate(data_array), 'L').save('dilation.bmp')
print('dilated')
Image.fromarray(erose(data_array), 'L').save('erosion.bmp')
print('erosed')
Image.fromarray(dilate(erose(data_array))).save('opening.bmp')
print('opened')
Image.fromarray(erose(dilate(data_array))).save('closing.bmp')
print('closed')