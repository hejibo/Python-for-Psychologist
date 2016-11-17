'''
Developed by Dr. Jibo He @USEE.TECH
hejibo@usee.tech

## Goal
Tobii eye tracker's Tobii studio does not provide a way to design the presentation stimuli. 
I created this script to combine images and text to create the presentation stumuli.

The resolution of the Tobii eyetracker display is 1280 * 720 pixels

## dependency
pip install pil 

## References

* add text and images to canvas in python
    http://code.activestate.com/recipes/579013-draw-text-to-image/

    http://stackoverflow.com/questions/16373425/add-text-on-image-using-pil

    http://stackoverflow.com/questions/10647311/how-do-you-merge-images-into-a-canvas-using-pil-pillow

    http://stackoverflow.com/questions/30227466/combine-several-images-horizontally-with-python

* Attention: PIL is deprecated, and pillow is the successor.
    * http://stackoverflow.com/questions/8863917/importerror-no-module-named-pil

* change text font size
    * http://stackoverflow.com/questions/2726171/how-to-change-font-size-using-the-python-imagedraw-library

* resize and image
    *http://stackoverflow.com/questions/273946/how-do-i-resize-an-image-using-pil-and-maintain-its-aspect-ratio
    half = 0.5
    out = im.resize( [int(half * s) for s in im.size] )

# Note the baseFaceFoundationImage.png is 615 *248. To fit the image and text into the canvas, 
I resized the baseFaceFoundationImage to 70% of its original size, which is (430, 173)
The top padding is (720-173)/2
'''

from PIL import Image, ImageDraw, ImageFont


text = "Hello World!"
# textColor = (255, 255, 0) # RGB Yellow
# textBackgroundColor = (255, 0, 0) # RGB Red
textX = 400 # text width in pixels
textY = 100 # text height in pixels
textTopLeftX = 0
textTopLeftY = 0



#opens an image:
im = Image.open("baseFaceFoundationImage.png")
#creates a new empty image, RGB mode, and size 400 by 400.
new_im = Image.new('RGB', (1280,720),(255, 255, 255))

TopPadding =273

half = 0.7
imDownsized = im.resize( [int(half * s) for s in im.size] )
print "base image size:",imDownsized.size

new_im.paste(imDownsized, (20,TopPadding))

#new_im.show()

font_path = "Courier.ttf"
fontHighlited = ImageFont.truetype(font_path, 35)
fontNormal = ImageFont.truetype(font_path, 20)

draw = ImageDraw.Draw(new_im)

draw.text((720, TopPadding),
'''Glycerin and shea\n
butter keep skin\n
feeling moisturized\n
while a gel base\n
creates a lightweight\n
finish that stays color-\n
true.''',
    (0,0,0),
    font=fontNormal
    )

draw.text((1000, TopPadding),'''
This long-wearing\n
perfectly balanced\n
formula evens skin\n
tone, minimizes\n
the appearance of\n
pores, and conceals\n
imperfections.
''',(0,0,0),font=fontNormal)


draw.text((460, TopPadding),
'''Great on\n
overall\n
performance''',(255,0,0),font=fontHighlited)


new_im.save("output.png", "PNG")
new_im.show()

print '-_-!'