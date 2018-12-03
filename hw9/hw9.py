from PIL import Image
import numpy as np

im = Image.open('lena.bmp')
(C,R), arr = im.size, np.array(im)

sqrt2 = np.sqrt(2)

roberts_mask = \
[[0,0,0,0,-1,0,0,0,1],\
[0,0,0,0,0,-1,0,1,0]]
prewitt_mask = \
[[-1,-1,-1,0,0,0,1,1,1],\
[-1,0,1,-1,0,1,-1,0,1]]
sobel_mask = \
[[-1,-2,-1,0,0,0,1,2,1],\
[-1,0,1,-2,0,2,-1,0,1]]
frei_chen_mask = \
[[-1,-sqrt2,-1,0,0,0,1,sqrt2,1],\
[-1,0,1,-sqrt2,0,sqrt2,-1,0,1]]
kirsch_mask = \
[[-3,-3,5,-3,0,5,-3,-3,5],\
[-3,5,5,-3,0,5,-3,-3,-3],\
[5,5,5,-3,0,-3,-3,-3,-3],\
[5,5,-3,5,0,-3,-3,-3,-3],\
[5,-3,-3,5,0,-3,5,-3,-3],\
[-3,-3,-3,5,0,-3,5,5,-3],\
[-3,-3,-3,-3,0,-3,5,5,5],\
[-3,-3,-3,-3,0,5,-3,5,5]]
robinson_mask = \
[[-1,0,1,-2,0,2,-1,0,1],\
[0,1,2,-1,0,1,-2,-1,0],\
[1,2,1,0,0,0,-1,-2,-1],\
[2,1,0,1,0,-1,0,-1,-2],\
[1,0,-1,2,0,-2,1,0,-1],\
[0,-1,-2,1,0,-1,2,1,0],\
[-1,-2,-1,0,0,0,1,2,1],\
[-2,-1,0,-1,0,1,0,1,2]]
nevatia_babu_mask = \
[[100]*10+[0]*5+[-100]*10,\
[100]*8+[78,-32,100,92,0,-92,-100,32,-78]+[-100]*8,\
[100]*3+[32,-100,100,100,92,-78,-100,100,100,0,-100,-100,100,78,-92,-100,-100,100,-32]+[-100]*3,\
[-100,-100,0,100,100]*5,\
[-100,32]+[100]*3+[-100,-78,92,100,100,-100,-100,0,100,100,-100,-100,-92,78,100]+[-100]*3+[-32,100],\
[100]*5+[-32,78]+[100]*3+[-100,-92,0,92,100]+[-100]*3+[-78,32]+[-100]*5]


def val(r, c):
	return float(arr[r][c]) if r>=0 and r<R and c>=0 and c<C else 0

def Mask(r, c, mask, mask_size):
	index, ret = 0, np.zeros(len(mask), dtype=np.float)
	for dr in range(-mask_size,mask_size+1):
		for dc in range(-mask_size,mask_size+1):
			tmp = val(r+dr, c+dc)
			for i, ma in enumerate(mask):
				ret[i] += tmp*ma[index]
			index += 1
	return ret

def pythagoras(input):
	ret = 0
	for tmp in input: ret += tmp*tmp
	return np.sqrt(ret)

def binarize(method, mask, mask_size, threshold):
	ret = np.zeros((R,C), dtype=np.uint8)
	for r in range(R):
		for c in range(C):
			if(method(Mask(r, c, mask, mask_size)) <= threshold): ret[r][c] = 255
	return ret

Image.fromarray(binarize(pythagoras, roberts_mask, 1, 30)).save('roberts.bmp')
Image.fromarray(binarize(pythagoras, prewitt_mask, 1, 90)).save('prewitt.bmp')
Image.fromarray(binarize(pythagoras, sobel_mask, 1, 120)).save('sobel.bmp')
Image.fromarray(binarize(pythagoras, frei_chen_mask, 1, 110)).save('freichen.bmp')
Image.fromarray(binarize(max, kirsch_mask, 1, 460)).save('kirsch.bmp')
Image.fromarray(binarize(max, robinson_mask, 1, 120)).save('robinson.bmp')
Image.fromarray(binarize(max, nevatia_babu_mask, 2, 32600)).save('nevatiababu.bmp')