from PIL import Image, ImageDraw, ImageFont
import when
import glob
"""YOU CAN CHANGE THESE"""
#Nothing here oops
"""Nothing Below This"""
watermark = Image.open("watermark.png")
filetypes = ["jpg", "JPG", "png", "PNG", "JPEG", "jpeg"]
copyright_symbol = u"\N{COPYRIGHT SIGN}"

def draw_stroke(x,y, screen, font, border_size=1,text="DARE", shadowcolor=(255,255,255,128),fill_color=(0,0,0,128), rotate=0):
    txt = Image.new('RGBA', screen.size, (0,0,0,0))
    draw = ImageDraw.Draw(txt)
    #Thick Border
    draw.text((x-border_size, y-border_size), text, font=font, fill=shadowcolor)
    draw.text((x+border_size, y-border_size), text, font=font, fill=shadowcolor)
    draw.text((x-border_size, y+border_size), text, font=font, fill=shadowcolor)
    draw.text((x+border_size, y+border_size), text, font=font, fill=shadowcolor)
    #Text
    draw.text((x, y), text, font=font, fill=fill_color)
    return Image.alpha_composite(screen,txt)

def first_font():
    for infile in glob.glob("*.ttf"):
        return infile
    for infile in glob.glob("*.otf"):
        return infile

def tag_image(image, name, fill_color=(0,0,0,128), shadowcolor=(227,43,23,128)):
    font_name = first_font()
    screen = image.convert("RGBA")
    font_size = 1
    img_fraction = 0.90
    font = ImageFont.truetype(font_name, font_size)
    border_size = 5
    scaler = 1.25
    year = str(when.today()).partition("-")[0]
    text = "%s %s %s" % (copyright_symbol, name, year)
    while font.getsize(text)[0] < img_fraction*image.size[0]:
        # iterate until the text size is just larger than the criteria
        font_size += 1
        font = ImageFont.truetype(font_name, font_size)
    #Draw Name
    x = screen.width * 0.05
    y = screen.height-(font_size*scaler)
    font = ImageFont.truetype(font_name, font_size)
    out = draw_stroke(x, y, screen, font, border_size=border_size, text=text, shadowcolor=shadowcolor, fill_color=fill_color)
    #Save Image
    return out

def watermark_image(image, skip=0):
    x = 0
    y = 0
    count = 0
    while y < image.height:
        while x < image.width:
            if count == skip:
                image.paste(watermark, (x,y), mask=watermark)
                count = 0
            elif count < skip:
                count += 1

            x += watermark.width
        x = 0
        y += watermark.height

    return image

def watermark_the_files(cext, skip=0):
    for infile in glob.glob("*.%s" % cext):
        if "watermark" not in infile:
            im = Image.open(infile)
            im = watermark_image(im, skip)
            im.save("watermarked/%s" % infile)

def tag_the_files(cext, name, fill, stroke):
    for infile in glob.glob("*.%s" % cext):
        if "watermark" not in infile:
            im = Image.open(infile)
            im = tag_image(im, name, fill_color=fill, shadowcolor=stroke)
            im.save("tagged/%s" % infile)

options = ["Watermark Files", "Tag Files"]
for y in range(len(options)):
    print("%d. %s" % (y+1, options[y]))
inp = str(raw_input("Enter an option number: "))
name = ""
skip = 0
opacity = 128
fc = (0,0,0, opacity)
sc = (255, 255, 255, opacity)

if "1" in inp:
    skip = int(raw_input("Skip Count (Ex. 1, 2, 3): "))
elif "2" in inp:
    name = str(raw_input("Name of Owner: "))
    print("LEAVE FOLLOWING BLANK FOR DEFAULT")
    try:
        opacity = int(raw_input("Opacity (0-255): "))
    except ValueError:
        opacity = 128
    print("Color (0-255) Example: '23, 43, 27'")
    fc = (int(raw_input("Red Fill Color: ")), int(raw_input("Green Fill Color: ")), int(raw_input("Blue Fill Color: ")), opacity)
    sc = (int(raw_input("Red Stroke Color: ")), int(raw_input("Green Stroke Color: ")), int(raw_input("Blue Stroke Color: ")), opacity)

for x in filetypes:
    if "1" in inp:
        watermark_the_files(x, skip)
    elif "2" in inp:
        tag_the_files(x, name, fc, sc)
raw_input("The Program Has Complete Its Run\nPress Enter Key To Exit...")

