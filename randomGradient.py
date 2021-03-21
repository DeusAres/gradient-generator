from PIL import Image, ImageDraw
from random import randint
import drawerFunctions

def checkNumber(num):
    while num > 359:
        num -= 360
    while num < 0:
        num = abs(num)
        while num > 359:
            num -= 360
    return num

def complementary(firstColor):
    secondColor = (checkNumber(180 - firstColor[0]), firstColor[1], firstColor[2])
    return secondColor

def monochromatic(firstColor):
    secondColor = (firstColor[0], checkNumber(firstColor[1]), checkNumber(firstColor[2] - 30))
    thirdColor = (firstColor[0], checkNumber(firstColor[1]), checkNumber(firstColor[2] - 40))
    return secondColor, thirdColor

def analogous(firstColor):
    secondColor = (checkNumber(firstColor[0] + 30), firstColor[1], firstColor[2])
    thirdColor = (checkNumber(firstColor[0] - 30), firstColor[1], firstColor[2])
    return secondColor, thirdColor

def split(firstColor): 
    half = firstColor[0] + 180
    secondColor = (checkNumber(half + 20), firstColor[1], firstColor[2])
    thirdColor = (checkNumber(half - 20), firstColor[1], firstColor[2])

    return secondColor, thirdColor

def triadic(firstColor):    
    half = firstColor[0] + 180
    secondColor = (checkNumber(half + 45), firstColor[1], firstColor[2])
    thirdColor = (checkNumber(half - 45), firstColor[1], firstColor[2])
    return secondColor, thirdColor

def sixColors(firstColor):
    adder = 60
    colorList = []
    for i in range(1, 6, 1):
        colorList.append((checkNumber(firstColor[0]+adder*i), firstColor[1], firstColor[2]))
    return colorList

def random_gradient(W, H):
    img = Image.new("RGBA", (W,H), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    hslColor = (randint(0, 359), randint(80, 100), randint(50, 60))
    hslList = [hslColor]    
    
    randomFunction = randint(1, 6)
    if randomFunction == 1: hslList.append((complementary(hslColor)))
    if randomFunction == 2: 
        second, third = monochromatic(hslColor)
        hslList.append(second)
        hslList.append(third)
    if randomFunction == 3: 
        second, third = analogous(hslColor)
        hslList.append(second)
        hslList.append(third)
    if randomFunction == 4: 
        second, third = split(hslColor)
        hslList.append(second)
        hslList.append(third)
    if randomFunction == 5:
        second, third = triadic(hslColor)
        hslList.append(second)
        hslList.append(third)
    if randomFunction == 6:
        hslList += sixColors(hslColor)
    
    colors = []
    for color in hslList:
        colors.append(drawerFunctions.hslToRgb(color[0], color[1], color[2]))

    add = []
    numberOfSteps = int(W / (len(colors)-1))
    lastCoord = 0
    nextCoord = numberOfSteps

    for indexColor in range(1, len(colors), 1):
        add.clear()
        for indexTuple in range(3):
            add.append((colors[indexColor][indexTuple] - colors[indexColor-1][indexTuple]) / (W / (len(colors)-1)))

        r,g,b = colors[indexColor-1]
    
        for i in range(lastCoord, nextCoord, 1):
            r,g,b = r+add[0], g+add[1], b+add[2]
            draw.line((i,0,i,H), fill=(int(r),int(g),int(b)))
        
        lastCoord = nextCoord
        nextCoord += numberOfSteps
    img = drawerFunctions.blurImage(img, 2)
    img = drawerFunctions.rotate(img, 90)
    return img

