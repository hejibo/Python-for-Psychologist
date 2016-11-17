'''
By Jibo He @usee.tech
hejibo@usee.tech
add an image to an empty canvas
'''
from PIL import Image
#opens an image:
im = Image.open("baseFaceFoundationImage.png")
#creates a new empty image, RGB mode, and size 400 by 400.
new_im = Image.new('RGB', (1280,720),(255, 255, 255))
half = 0.7
imDownsized = im.resize( [int(half * s) for s in im.size] )
print "base image size:",imDownsized.size

TopPadding =273
new_im.paste(imDownsized, (20,TopPadding))
new_im.show()
new_im.save("output.png", "PNG")