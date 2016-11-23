from PIL import Image, ImageFont, ImageDraw
from random import randint
import json, sys, requests
from datetime import time, datetime
from time import strftime

# Defines location of different image files to create show image.
backgroundImagePath = "GenericShowBackgrounds/"
colouredBarsPath = "ColouredBars/"
try:
	apiKey = sys.argv[1]
	url = "https://ury.org.uk/api/v2/show/allshows?current_term_only=1&api_key=" + apiKey
	debugMode = sys.argv[2]
except IndexError as e:
	log("ERROR", "System Argument(s) not passed in.", str(e))


def getShows():
    """
    A function to return a dictionary of shows with show id mapping to the show title.
    Return:
        The dictionary of shows with show ids mapping to the show title.
    """
    try:
        log("DEBUG", "Running getShows() function.")
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
    A function to create a show image for given show name, output file name and branding.
    Args:
        showName (str): Show name to add to image.
        outputName (str): The name of the outputfile, standard form including the show id.
        branding (str): The branding to be applied.
    Return:
        The function outputs a JPG image to a sub folder called ShowImages.
    """
    # Hack to get branding from show name
    log("DEBUG", "Running applyBrand() function.", showID)
    branding = brandingFromShowName(showName)
    showName = stripPrefix(showName)
    # Determines which overlay to apply to the show image.
    if branding == "Speech":
        log("DEBUG", "Show branding should be speech.", showID)
        brandingOverlay = "GreenSpeech.png"
    elif branding == "News":
        log("DEBUG", "Show branding should be news.", showID)
        brandingOverlay = "BlueGeneral.png"
    elif branding == "Music":
        log("DEBUG", "Show branding should be music.", showID)
        brandingOverlay = "PurpleMusic.png"
    elif branding == "OB":
        log("DEBUG", "Show branding should be OB.", showID)
        brandingOverlay = "RedOB.png"
    elif branding == "Old":
        log("DEBUG", "Show branding should be old.", showID)
        brandingOverlay = "WhitePreShowImageFormat.png"
    else:
        log("DEBUG", "Show branding should be generic show.", showID)
        brandingOverlay = "BlueGeneral.png"

# Determines which background image to use for the show image.
    img = Image.open(backgroundImagePath + str(randint(1,16)) +".png")

# Opens overlay and pastes over the background image
    overlay = Image.open(colouredBarsPath + brandingOverlay)
    img.paste(overlay, (0, 0), overlay)

# First line formatting
    log("DEBUG", "Formatting the first line.", showID)
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
    log("DEBUG", "Formatting further lines.", showID)
    otherLinesTextSize = 50
    # firstLineFont = ImageFont.truetype(<font-file>, <font-size>)
    otherLinesFont = ImageFont.truetype("Raleway-LightItalic.ttf", otherLinesTextSize)

    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(otherLines, otherLinesFont)
    otherLinesTextHeight = 300
    
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((800-w)/2, otherLinesTextHeight), otherLines,(255,255,255),otherLinesFont, align='center')

# website URY formatting
    log("DBEUG", "Applying website branding.", showID)
    websiteURL = 'URY.ORG.UK/LIVE \n @URY1350'
    websiteFont = ImageFont.truetype("Raleway-SemiBoldItalic.ttf", otherLinesTextSize)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(websiteURL, otherLinesFont)
    websiteURLHeight = 510 
    
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((800-w)/2, websiteURLHeight), websiteURL,(255,255,255),otherLinesFont, align='center')

# Saves the image as the output name in a subfolder ShowImages
    log("DEBUG", "Saving the final image.", showID)
    img.save('ShowImages/%s.jpg' %outputName)

def brandingFromShowName(showName):
	"""
    A function to determine the branding to be applied based on the show name.
    Args:
        showName (str): The show name.
    Return:
        A string of what branding to apply.
    """
    if showName[:13] == "URY Presents:":
        log("DEBUG", "Applying OB branding.", showID)
        output = 'OB'
    elif showName == "The URY Pantomime 2016: Beauty and the Beast":
        log("DEBUG", "Applying OB branding.", showID)
        output = 'OB'
    elif showName[:1] == "#":
        log("DEBUG", "Applying OB branding.", showID)
        output = 'OB'
    elif showName == "Georgie and Angie's Book Corner":
        log("DEBUG", "Applying speech branding.", showID)
        output = 'Speech'
    elif showName == "Stage":
        log("DEBUG", "Applying speech branding.", showID)
        output = 'Speech'
    elif showName == "Speech Showcase":
        log("DEBUG", "Applying speech branding.", showID)
        output = 'Speech'
    elif showName == "Screen":
        log("DEBUG", "Applying speech branding.", showID)
        output = 'Speech'
    elif showName == "URY Newshour":
        log("DEBUG", "Applying news branding.", showID)
        output = 'News'
    elif showName == "York Sport Report":
        log("DEBUG", "Applying news branding.", showID)
        output = 'News'
    elif showName == "URY:PM - (( URY Music ))":
        log("DEBUG", "Applying music branding.", showID)
        output = 'Music'
    else:
        log("DEBUG", "No branding to be applied.", showID)
        output = ''
    return output


def stripPrefix(showName):
	"""
    A function to strip the prefix from the show name.
    Args:
        showName (str): The show name.
    Return:
        The show name without the prefix.
    """
    if showName[:12] == "URY Brunch -":
        log("DEBUG", "Removing 'URY Brunch -' from the title.", showID)
        output = showName[12:]
    elif showName[:8] == "URY:PM -":
        log("DEBUG", "Removing 'URY:PM -' from the title.", showID)
        output = showName[8:]
    else:
        log("DEBUG", "No prefix to be removed from the title.", showID)
        output = showName
    return output


def normalize(input):
	"""
    A function to split the show name into seperate lines of maximum lengths.
    Args:
        input (str): The Show name.
    Return:
        Two strings. firstLine is the first line of text. otherLines is the string of other lines with line breaks inserted when necessary.
    """
    log("DEBUG", "Running normalize() function.", showID)
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
	"""
    A function to normalize the remaining lines of text (if any).
    Args:
        otherLinesList (list): A list representing the current lines.
        word (str): The word to append to the image.
    Return:
        A list representing each line. The word will be added to whichever line it can fit in.
    """
    log("DEBUG", "Running otherLinesList() function.", showID)
    maxOtherLinesLength = 22
    if len(word) > maxOtherLinesLength:
        log("DCM", "Word too long for image.", showID, "Within function dealWithOtherLines().")
        raise Exception
    elif len(otherLinesList) > 0 and (len(otherLinesList[-1]) + len(word) < maxOtherLinesLength):
        otherLinesList[-1] += " " + word
    else:
        otherLinesList.append(word)
    return otherLinesList


def log(typeM="DEBUG", message="NONE", showNum="NULL", errorMessage="No exception error message."):
    """
    A function to output logs to a log file for debugging or exceptions.
    Args:
        typeM (str): The type of log to make.
        mesage (str): The message to explain the log.
        showNum (str): The show ID (if there is one).
        errorMessage (str): The exception (if there is one).
    """
    if  (debugMode == 'T') or (typeM == "DCM") or (typeM == "API") or (typeM == "Error"):
        f=open("logfile.log","a")
        now = datetime.now()
        curTime = now.strftime("%Y-%m-%d %H:%M:%S.%f")
        f.write(curTime + " - [" + typeM.upper() + "] Show ID: {" + showNum + "} " + message + "\n" + errorMessage + "\n")
        f.close()
        if typeM == "DCM" or typeM == "API":
            pass #Call send email function to DCM or computing
    else:
        pass

################################
################################
#### Uses API To Get Shows #####
################################
################################
log("DEBUG", "Program Started!")
ShowsDict = getShows()

for key in ShowsDict:
    
    showName = ShowsDict[key]
    showID = str(key)
    branding = 'OB'

    applyBrand(showName, showID, branding)
log("DEBUG", "Program Complete!")