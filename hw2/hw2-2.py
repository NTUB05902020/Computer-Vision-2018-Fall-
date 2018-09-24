from PIL import Image
import matplotlib.pyplot as plt

im = Image.open('lena.bmp')
width, height = im.size

#caculate the histogram
xaxis, count = [i for i in range(256)], [0]*256
for i in range(width):
	for j in range(height):
		count[im.getpixel((i,j))] += 1
#draw
plt.bar(xaxis, count, color='blue')
plt.savefig('output/histogram.jpg')
im.close()
