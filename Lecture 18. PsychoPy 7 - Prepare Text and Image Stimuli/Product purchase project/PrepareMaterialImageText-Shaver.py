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

#opens an image:
im = Image.open("ShaverBase.png")
#creates a new empty image, RGB mode, and size 400 by 400.
new_im = Image.new('RGB', (1280,1024),(255, 255, 255))

TopPadding =180
TopPaddingText = 323

half = 0.7
imDownsized = im.resize( [int(half * s) for s in im.size] )
print "base image size:",imDownsized.size

new_im.paste(imDownsized, (25,TopPadding))

#new_im.show()

font_path = "Courier.ttf"
fontHighlited = ImageFont.truetype(font_path, 30)
fontNormal = ImageFont.truetype(font_path, 18)

draw = ImageDraw.Draw(new_im)




draw.text((670, TopPaddingText-50),'''
 Even though cheap,\n this one-of-a-kind\n product offers value\n to novices and\n experienced shavers\n alike. It is easy to\n use, durable, and\n comes with an array\n of professional-\ngrade accessories
''',(0,0,0),font=fontNormal)


draw.text((940, TopPaddingText-50),'''
This model, made\n from high-grade\n aluminum, has all\n the impressive\n qualitites you'd\n expect from a razor,\n with a lightweight\n design that smacks\n of fast cars and\n fighter jets.
''',(0,0,0),font=fontNormal)



#draw.text((370, TopPaddingText),
#'''Great on overall\n
#performance
#''',(255,0,0),font=fontHighlited)

draw.text((400, TopPaddingText),
'''Great on \n
lightness
''',(255,0,0),font=fontHighlited)


new_im.save("output.png", "PNG")
new_im.show()

print '-_-!'