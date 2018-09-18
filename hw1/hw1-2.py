from PIL import Image
im = Image.open('lena.bmp')
width, height = im.size

#rotate -45 degrees
im.rotate(-45).save("output/2a.bmp")

#shrink in half
im.resize((width//2, height//2)).save("output/2b.bmp")

#binarize at 128
for i in range(width):
	for j in range(height):
		im.putpixel((i,j), 0 if im.getpixel((i,j)) < 128 else 255)
im.save("output/2c.bmp")
im.close()
