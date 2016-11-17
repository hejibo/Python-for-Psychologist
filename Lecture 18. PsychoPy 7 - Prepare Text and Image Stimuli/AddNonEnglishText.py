#!/usr/bin/python
# - *- coding: utf- 8 - *-
'''
Developed by Dr. Jibo He @USEE.TECH
hejibo@usee.tech

'''


from PIL import Image, ImageDraw, ImageFont

TopPadding =273
font_path = "Courier.ttf"
fontHighlited = ImageFont.truetype(font_path, 35)
fontNormal = ImageFont.truetype(font_path, 20)

new_im = Image.new('RGB', (1280,720),(255, 255, 255))
draw = ImageDraw.Draw(new_im)

textCN = unicode('我爱PsychoPy', 'utf-8') 

draw.text((460, TopPadding),
textCN,(255,0,0),font=fontHighlited)

new_im.save("output.png", "PNG")
new_im.show()
