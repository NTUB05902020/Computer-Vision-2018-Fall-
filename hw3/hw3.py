from PIL import Image
import matplotlib.pyplot as plt

im = Image.open('lena.bmp')
width, height = im.size
count, sk, total = [0 for i in range(256)], [], width*height

#get histogram
for i in range(width):
	for j in range(height):	count[im.getpixel((i, j))] += 1
#prepare sk
sk += [count[0]]
for i in range(1, 256):	sk += [sk[i-1] + count[i]]
#modify image
for i in range(width):
	for j in range(height):
		where = (i, j)
		im.putpixel(where, sk[im.getpixel(where)] * 255 // total)
im.show()
im.save("equalized.bmp")
im.close()

#draw histogram of new image
im = Image.open('equalized.bmp')
width, height = im.size

#caculate the histogram
xaxis, count = [i for i in range(256)], [0]*256
for i in range(width):
	for j in range(height):
		count[im.getpixel((i,j))] += 1
#draw
plt.bar(xaxis, count, color='blue')
plt.savefig('histogram.jpg')
im.close()
