!SLIDE

# PsychoPy 7: Prepare Text and Image Stimuli
   
    Created by Dr. Jibo He
    
    [mailto:hejibo@usee.tech](hejibo@usee.tech)

!SLIDE

### Table of Content
- Environment configuration
- Add image to another image
- Add text to image
- Add non-English text in an image

!SLIDE left
# Environment configuration
~~~~{python}
pip install pil
~~~~

or 

~~~~{python}
pip install pillow
~~~~

- Note: pil is depreciated, pillow replaces pil package. 

!SLIDE left
# Add image to another image
~~~~{python}
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
~~~~

!SLIDE left
# Add text to an image
~~~~{python}
from PIL import Image, ImageDraw, ImageFont

TopPadding =273
font_path = "Courier.ttf"
fontHighlited = ImageFont.truetype(font_path, 35)
fontNormal = ImageFont.truetype(font_path, 20)

new_im = Image.new('RGB', (1280,720),(255, 255, 255))
draw = ImageDraw.Draw(new_im)

draw.text((460, TopPadding),
'''Great on\n
overall\n
performance''',(255,0,0),font=fontHighlited)

new_im.save("output.png", "PNG")
new_im.show()
~~~~

!SLIDE left
# Add non-English text in an image
~~~~{python}
SyntaxError: Non-ASCII character '\xe6' in file /Users/hejibo/Documents/Python-for-Psychologist/Lecture 18. P
sychoPy 7 - Prepare Text and Image Stimuli/AddNonEnglishText.py on line 18, but no encoding declared; see htt
p://python.org/dev/peps/pep-0263/ for details
~~~~

!SLIDE left
# Add non-English text in an image
~~~~{python}
SyntaxError: Non-ASCII character '\xe6' in file /Users/hejibo/Documents/Python-for-Psychologist/Lecture 18. P
sychoPy 7 - Prepare Text and Image Stimuli/AddNonEnglishText.py on line 18, but no encoding declared; see htt
p://python.org/dev/peps/pep-0263/ for details
~~~~

!SLIDE left
# Add non-English text in an image
~~~~{python}
#!/usr/bin/python
#-*-coding:utf-8 -*-
~~~~





!SLIDE left
# A real project
* add both image and text to another image. 
~~~~{python}
from PIL import Image, ImageDraw, ImageFont

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
~~~~


!SLIDE left
# References

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