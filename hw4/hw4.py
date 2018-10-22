from PIL import Image
import numpy
import morph

im = Image.open('binarized.bmp')
(width,height), data_array = im.size, numpy.array(im)
pic = morph.PIC.imToPic(data_array)
Image.fromarray(pic.dilation(morph.tffft).toDataArray(), 'L').save('dilation.bmp')
print('dilation completed!')
Image.fromarray(pic.erosion(morph.tffft).toDataArray(), 'L').save('erosion.bmp')
print('erosion completed!')
Image.fromarray(pic.opening(morph.tffft).toDataArray(), 'L').save('opening.bmp')
print('opening completed!')
Image.fromarray(pic.closing(morph.tffft).toDataArray(), 'L').save('closing.bmp')
print('closing completed!')
Image.fromarray(pic.hitAndMiss(morph.J, morph.K).toDataArray(), 'L').save('rightUp.bmp')