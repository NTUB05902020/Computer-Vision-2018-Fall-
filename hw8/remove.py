from PIL import Image
import numpy as np

inputs = ['gauss_10.bmp', 'gauss_30.bmp', 'SandP_05.bmp', 'SandP_10.bmp']
kernel = [(-2,-1),(-2,0),(-2,1),(-1,-2),(-1,-1),(-1,0),(-1,1),(-1,2),\
(0,-2),(0,-1),(0,0),(0,1),(0,2),(1,-2),(1,-1),(1,0),(1,1),(1,2),(2,-1),(2,0),(2,1)]

def toInt(a):
	if a >= 255: return 255
	elif a <= 0: return 0
	return round(a)

def getNeighbors(Arr, r, c, n):
	ret, n = [], n//2
	for dr in range(-n, n+1):
		for dc in range(-n, n+1):
			new_r, new_c = r+dr, c+dc
			if new_r>=0 and new_c>=0 and new_r<R and new_c<C:
				ret += [Arr[new_r][new_c]]
	return ret

def dilate(arr):
	height, width = len(arr), len(arr[0])
	ret = np.zeros((height, width), dtype=np.uint8)
	for r in range(height):
		for c in range(width):
			for r2,c2 in kernel:
				try: ret[r][c] = max(ret[r][c], arr[r-r2][c-c2])
				except IndexError: continue
	return ret
def erose(arr):
	height, width = len(arr), len(arr[0])
	ret = np.full((height, width), 255, dtype=np.uint8)
	for r in range(height):
		for c in range(width):
			for r2,c2 in kernel:
				try: ret[r][c] = min(arr[r+r2][c+c2], ret[r][c])
				except IndexError: continue
	return ret

def opening(arr):
	return dilate(erose(arr))

def closing(arr):
	return erose(dilate(arr))

for inName in inputs:
	im = Image.open(inName)
	arr = np.array(im)
	im.close()
	R, C = len(arr), len(arr[0])
	tmp1, tmp2 = np.zeros((R,C), dtype=np.uint8), np.zeros((R,C), dtype=np.uint8)
	tmp3, tmp4 = np.zeros((R,C), dtype=np.uint8), np.zeros((R,C), dtype=np.uint8)
	for r in range(R):
		for c in range(C):
			neig3, neig5 = getNeighbors(arr, r, c, 3), getNeighbors(arr, r, c, 5)
			tmp1[r][c], tmp2[r][c] = toInt(sum(neig3)/len(neig3)), toInt(sum(neig5)/len(neig5))
			tmp3[r][c], tmp4[r][c] = toInt(np.median(neig3)), toInt(np.median(neig5))
	tmp5, tmp6 = closing(opening(arr)), opening(closing(arr))
	Image.fromarray(tmp1).save(inName[0:-4]+'box3.bmp')
	Image.fromarray(tmp2).save(inName[0:-4]+'box5.bmp')
	Image.fromarray(tmp3).save(inName[0:-4]+'median3.bmp')
	Image.fromarray(tmp4).save(inName[0:-4]+'median5.bmp')
	Image.fromarray(tmp5).save(inName[0:-4]+'open-close.bmp')
	Image.fromarray(tmp6).save(inName[0:-4]+'close-open.bmp')