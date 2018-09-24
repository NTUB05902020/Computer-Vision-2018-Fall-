from PIL import Image
im = Image.open('lena.bmp')
width, height = im.size

#binarize with threshold 128 (0~127, 128~255)
for i in range(width):
	for j in range(height):
		im.putpixel((i,j), 0 if im.getpixel((i,j)) < 128 else 255)
im.save("output/binarized.bmp")
im.close()
