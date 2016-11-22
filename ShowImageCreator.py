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

debugMode = sys.argv[2]

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
    except:
        log("API","Could not acess API.")
        sys.exit(0)


def applyBrand(showName, outputName, branding):
    """
    A function to create a show image for given show name and output file name.
    Args:
        showName (str): Show name to add to image.
        outputName (str): The name of the outputfile, standard form including the show id.
    Return:
        The function outputs a JPG image to a sub folder called ShowImages.
    """
    # Hack to get branding from show name
    branding = brandingFromShowName(showName)
    showName = stripPrefix(showName)
    # Determines which overlay to apply to the show image.
    if branding == "Speech":
        brandingOverlay = "GreenSpeech.png"
    elif branding == "News":
        brandingOverlay = "BlueGeneral.png"
    elif branding == "Music":
        brandingOverlay = "PurpleMusic.png"
    elif branding == "OB":
        brandingOverlay = "RedOB.png"
    elif branding == "Old":
        brandingOverlay = "WhitePreShowImageFormat.png"
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

def brandingFromShowName(showName):
    if showName[:13] == "URY Presents:":
        output = 'OB'
    elif showName == "The URY Pantomime 2016: Beauty and the Beast":
        output = 'OB'
    elif showName[:1] == "#":
        output = 'OB'
    elif showName == "Georgie and Angie's Book Corner":
        output = 'Speech'
    elif showName == "Stage":
        output = 'Speech'
    elif showName == "Speech Showcase":
        output = 'Speech'
    elif showName == "Screen":
        output = 'Speech'
    elif showName == "URY Newshour":
        output = 'News'
    elif showName == "York Sport Report":
        output = 'News'
    elif showName == "URY:PM - (( URY Music ))":
        output = 'Music'
    else:
        output = ''
    return output


def stripPrefix(showName):
    if showName[:12] == "URY Brunch -":
        output = showName[12:]
    elif showName[:8] == "URY:PM -":
        output = showName[8:]
    else:
        output = showName
    return output


def normalize(input):
    words = input.split(" ")
    maxFirstLineLength = 13
    firstLine = ''
    otherLinesList = []
    firstLineFull = False

    for word in words:
        if firstLineFull == False:
            if (len(word) > maxFirstLineLength) and (len(firstLine) < maxFirstLineLength) and (len(firstLine) > 0):
                firstLineFull = True
                otherLinesList = dealWithOtherLines(otherLinesList, word)
            elif (len(word) > maxFirstLineLength) and (len(firstLine) < maxFirstLineLength):
                log("DCM", word +" is too long for first line of image.", showID)
                break
            elif len(firstLine + word) <= maxFirstLineLength:
                firstLine += str(word) + ' '
            else:
                firstLineFull = True
                otherLinesList = dealWithOtherLines(otherLinesList, word)
        else:
            otherLinesList = dealWithOtherLines(otherLinesList, word)
    otherLines = "".join(item + "\n" for item in otherLinesList)
    return firstLine, otherLines


def dealWithOtherLines(otherLinesList, word):
    maxOtherLinesLength = 22
    if len(word) > maxOtherLinesLength:
        log("DCM", "Word too long for image.", showID, "Within function dealWithOtherLines().")
        raise Exception
    elif len(otherLinesList) > 0 and (len(otherLinesList[-1]) + len(word) < maxOtherLinesLength):
        otherLinesList[-1] += " " + word
    else:
        otherLinesList.append(word)
    return otherLinesList


def log(type="DEBUG", message="NONE", showNum="NULL", errorMessage="No exception error message.", mode="WARNING"):
    if  mode == "DEBUG" || type == "DCM" || type == "API":
        f=open("logfile.log","a")
        curTime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        f.write(curTime + " - [" + type.upper() + "] Show ID: {" + showNum + "} " + message + "\n" + errorMessage + "\n")
        f.close()
        if type == "DCM" || type == "API":
            pass #Call send email function to DCM or computing
    else:
        pass

################################
################################
#### Uses API To Get Shows #####
################################
################################

ShowsDict = getShows()

print(debugMode)

for key in ShowsDict:
    
    showName = ShowsDict[key]
    showID = str(key)
    branding = 'OB'

    applyBrand(showName, showID, branding)