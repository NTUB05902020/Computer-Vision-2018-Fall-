from PIL import Image
import numpy as np

im = Image.open('binarized.bmp')
arr = np.array(im)
arr = np.array([row[::8] for row in arr[::8]])
R, C = len(arr), len(arr[0])

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

def ispair(r,c,yokois):
	if r>0 and yokois[r-1][c]==1: return True
	if c>0 and yokois[r][c-1]==1: return True
	if r<(R-1) and yokois[r+1][c]==1: return True
	if c<(C-1) and yokois[r][c+1]==1: return True
	return False

i=0
while True:
	i = i+1
	yokoiarr = np.array([[f(r,c) if arr[r][c]!=0 else -1 for c in range(C)] for r in range(R)])
	pairarr = np.array([(r,c)for r in range(R) for c in range(C) if yokoiarr[r][c]==1 and ispair(r,c,yokoiarr)])
	if len(pairarr)==0: break
	for r,c in pairarr:
		if(f(r,c)==1): arr[r][c] = 0
Image.fromarray(arr).save('output.bmp')
