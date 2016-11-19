from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from random import randint
import json, sys, requests
from time import gmtime, strftime


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
    try:
        data = requests.get(url).json()
        shows = {}

        for show in data["payload"]:
            shows[data["payload"][show]["show_id"]] = data["payload"][show]["title"]

        return shows
    except Exception, e:
        log("Error","Could not acess API.",str(e))


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
    firstLineText, otherLines = normalize(showName)
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

    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(otherLines, otherLinesFont)
    otherLinesTextHeight = 300
    
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((800-w)/2, otherLinesTextHeight), otherLines,(255,255,255),otherLinesFont, align='center')

# website URY formatting
    websiteURL = 'URY.ORG.UK/LIVE \n @URY1350'
    websiteFont = ImageFont.truetype("Raleway-SemiBoldItalic.ttf", otherLinesTextSize)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(websiteURL, otherLinesFont)
    websiteURLHeight = 510 
    
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((800-w)/2, websiteURLHeight), websiteURL,(255,255,255),otherLinesFont, align='center')

# Saves the image as the output name in a subfolder ShowImages    
    img.save('ShowImages/%s.jpg' %outputName)


def normalize(input):
    words = input.split(" ")
    maxFirstLineLength = 13
    maxOtherLinesLength = 22
    firstLine = ''
    otherLinesList = []
    firstLineFull = False

    for word in words:
        if firstLineFull == False:
            if (len(word) > maxFirstLineLength) and (len(firstLine) < maxFirstLineLength):
                log("DCM","Word too long for image.")
                break
            elif len(firstLine + word) <= maxFirstLineLength:
                firstLine += str(word.upper()) + ' '
            else:
                firstLineFull = True
                otherLinesList = dealWithOtherLines(otherLinesList, word, maxOtherLinesLength)
        else:
            otherLinesList = dealWithOtherLines(otherLinesList, word, maxOtherLinesLength)
    otherLines = "".join(item + "\n" for item in otherLinesList)
    return firstLine, otherLines


def dealWithOtherLines(otherLinesList, word, maxOtherLinesLength):
    if len(word) > maxOtherLinesLength:
        log("DCM","Word too long for image.","Within function dealWithOtherLines().")
        raise Exception
    elif len(otherLinesList) > 0 and (len(otherLinesList[-1]) + len(word) < maxOtherLinesLength):
        otherLinesList[-1] += " " + word
    else:
        otherLinesList.append(word)
    return otherLinesList


def log(type, message, errorMessage="No error message."):
    f=open("logfile.log","a")
    curTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    f.write(curTime+" - ["+type.upper()+"] "+message+"\n"+errorMessage+"\n")
    f.close()
    if type=="DCM":
        pass #Call send email function to DCM


################################
#### Uses API To Get Shows #####
################################

ShowsDict = getShows()

for key in ShowsDict:
    applyBrand(ShowsDict[key], str(key), 'Music')
