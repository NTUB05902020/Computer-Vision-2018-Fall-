from PIL import Image
im = Image.open('lena.bmp')
width, height = im.size
newIm = im.copy()

#diagonally-mirror
for j in range(height):
	for i in range(j):
		index = ((i, j), (j, i))
		inform = tuple([newIm.getpixel(where) for where in index])
		for count in range(2): newIm.putpixel(index[count], inform[1-count])
#save-close
newIm.save("output/1c.bmp")
newIm.close()
im.close()
