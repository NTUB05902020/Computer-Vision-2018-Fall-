from PIL import Image
im = Image.open('lena.bmp')
width, height = im.size
newIm = im.copy()

#right-side-left
for j in range(height):
	for i in range(width//2):
		index = ((i, j), (width-i-1, j))
		inform = tuple([newIm.getpixel(where) for where in index])
		for count in range(2): newIm.putpixel(index[count], inform[1-count])
#save-close
newIm.save("output/1b.bmp")
newIm.close()
im.close()
