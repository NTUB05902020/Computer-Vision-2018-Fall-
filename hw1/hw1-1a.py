from PIL import Image
im = Image.open('lena.bmp')
width, height = im.size
newIm = im.copy()

#up-side-down
for i in range(width):
	for j in range(height//2):
		index = ((i, j), (i, height-j-1))
		inform = tuple([newIm.getpixel(where) for where in index])
		for count in range(2): newIm.putpixel(index[count], inform[1-count])
#save-close
newIm.save("output/1a.bmp")
newIm.close()
im.close()
