from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from random import randint
import json, sys, requests


# Defines location of different image files to create show image.
backgroundImagePath = "GenericShowBackgrounds/"
colouredBarsPath = "ColouredBars/"

apiKey = sys.argv[1]

url = "https://ury.org.uk/api/v2/show/allshows?current_term_only=1&api_key=" + apiKey


def getShows():
    """
    A function to return a dictionary of shows with show id mapping to the show title.
    Return:
        The dictionary of shows with show ids mapping to the show title.
    """
    data = requests.get(url).json()

    shows = {}

    for show in data["payload"]:
        shows[data["payload"][show]["show_id"]] = data["payload"][show]["title"]

    return shows


def applyBrand(showName, outputName, branding):
    """
    A function to create a show image for given show name and output file name.
    Args:
        showName (str): Show name to add to image.
        outputName (str): The name of the outputfile, standard form including the show id.
    Return:
        The function outputs a JPG image to a sub folder called ShowImages.
    """
    # Determines which overlay to apply to the show image.
    if branding == "Speech":
        brandingOverlay = "GreenSpeech.png"
    elif branding == "News":
        brandingOverlay = "GreenSpeech.png"
    elif branding == "Music":
        brandingOverlay = "PurpleMusic.png"
    elif branding == "OB":
        brandingOverlay = "RedOB.png"
    else:
        brandingOverlay = "BlueGeneral.png"

# Determines which background image to use for the show image.
    img = Image.open(backgroundImagePath + str(randint(1,16)) +".png")

# Opens overlay and pastes over the background image
    overlay = Image.open(colouredBarsPath + brandingOverlay)
    img.paste(overlay, (0, 0), overlay)

# First line formatting
    firstLineText, otherLines = firstLineNormalize(showName)
    firstLineFontSize = 85
    # firstLineFont = ImageFont.truetype(<font-file>, <font-size>)
    firstLineFont = ImageFont.truetype("Raleway-Bold.ttf", firstLineFontSize)
    
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(firstLineText, firstLineFont)
    firstLineHeight = 210
    
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((800-w)/2, firstLineHeight),firstLineText,(255,255,255),firstLineFont, align='center')

# Other Lines Show Text formatting
    otherLinesTextSize = 50
    # firstLineFont = ImageFont.truetype(<font-file>, <font-size>)
    otherLinesFont = ImageFont.truetype("Raleway-LightItalic.ttf", otherLinesTextSize)
    
    formattedOtherLines = otherLinesNormalize(otherLines)

    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(formattedOtherLines, otherLinesFont)
    otherLinesTextHeight = 300
    
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((800-w)/2, otherLinesTextHeight), formattedOtherLines,(255,255,255),otherLinesFont, align='center')

# website URY formatting
    websiteURL = 'URY.ORG.UK | @URY1350'
    websiteFont = ImageFont.truetype("Raleway-SemiBoldItalic.ttf", otherLinesTextSize)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(websiteURL, otherLinesFont)
    otherLinesTextHeight = 490 
    
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((800-w)/2, otherLinesTextHeight), websiteURL,(255,255,255),otherLinesFont, align='center')

# Saves the image as the output name in a subfolder ShowImages    
    img.save('ShowImages/%s.jpg' %outputName)


def firstLineNormalize(input):
    maxFirstLineLength = 13
    output = ''
    unused = ''
    for word in input.split(" "):
        if (len(word) > maxFirstLineLength) & (len(output) < maxFirstLineLength):
            #raise Exception("Word too long for image. Contact DCM.")
            break
        elif len(output+ ' ' + word) < maxFirstLineLength:
            output += str(word.upper()) + ' '
        else:
            unused += str(word.upper()) + ' '
    return output, unused


def otherLinesNormalize(input):
    maxFirstLineLength = 22
    output = []
    for word in input.split(" "):
        if len(word) > maxFirstLineLength:
            raise Exception("Word too long for image. Contact DCM.")
        elif len(output) > 0 and (len(output[-1]) + len(word) < maxFirstLineLength):
            output[-1] += " " + word
        else:
            output.append(word)

    if len(output) > 4:
        raise Exception("Spans too many lines for image. Contact DCM.")

    return "".join(item + "\n" for item in output)

################
#### Tests #####
################
"""
add_text('URY Brunch Some Show Name')
add_text('URY:PM Some Show Name')
add_text('Some Show Name')
add_text('Building Bridges - TheRoadtoRockandRoll and Roll')
print(normalize("Building Bridges - The Road to Rock and Roll"))
"""

## This runs through a file to generate show images.
"""
output =[]
f = open('Shows.txt', 'r')
for line in f:
    output.append(line)
f.close()
for i in range(0,len(output)):
    output[i] = output[i].rstrip('\n')
for el in output:
    add_text(el)
"""

ShowsDict = getShows()

for key in ShowsDict:
    applyBrand(ShowsDict[key], str(key), 'OB')
