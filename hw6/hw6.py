from PIL import Image
import numpy as np

im = Image.open('binarized.bmp')
arr = np.array(im)
arr = np.array([row[::8] for row in arr[::8]])
R, C = len(arr), len(arr[0])
#print(R, C)

def val(pos):
	r,c = pos
	return -1 if r<0 or c<0 or r>=R or c>=C else arr[r][c]

def h(a, b, c, d):
	va, vb, vc, vd = val(a), val(b), val(c), val(d)
	if va!=vb: return 's'
	return 'r' if vb==vc and vc==vd else 'q'

def f(r, c):
	ret = [h((r,c),(r,c+1),(r-1,c+1),(r-1,c)),\
	h((r,c),(r-1,c),(r-1,c-1),(r,c-1)),\
	h((r,c),(r,c-1),(r+1,c-1),(r+1,c)),\
	h((r,c),(r+1,c),(r+1,c+1),(r,c+1))]
	return 5 if(ret.count('r')==4) else ret.count('q')

file = open('output.txt', 'w')
for r in range(R):
	if r!=0: file.write('\n')
	for c in range(C):
		tmp = ' ' if arr[r][c]==0 else f(r,c)
		file.write(' ' if tmp==0 else str(tmp))
file.close()