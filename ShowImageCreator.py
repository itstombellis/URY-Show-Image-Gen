from PIL import Image, ImageFont, ImageDraw
from random import randint
import json, sys, requests
from datetime import time, datetime
from time import strftime

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
    
    #####
    ## Hack to get branding from show name
    branding = brandingFromShowName(showName)
    #####
    

    log("DEBUG", "Running applyBrand() function.", showID)
    showName = stripPrefix(showName)
    # Determines which overlay to apply to the show image.
    if branding == "Speech":
        log("DEBUG", "Show branding should be speech.", showID)
        brandingOverlay = "GreenSpeech.png"
    elif branding == "News":
        log("DEBUG", "Show branding should be news.", showID)
        brandingOverlay = "News.png"
    elif branding == "Music":
        log("DEBUG", "Show branding should be music.", showID)
        brandingOverlay = "PurpleMusic.png"
    elif branding == "OB":
        log("DEBUG", "Show branding should be OB.", showID)
        brandingOverlay = "RedOB.png"
    elif branding == "Old":
        log("DEBUG", "Show branding should be old.", showID)
        brandingOverlay = "WhitePreShowImageFormat.png"
    elif branding == "Flagship":
        log("DEBUG", "Show branding should be old.", showID)
        brandingOverlay = "Flagship.png"
    else:
        log("DEBUG", "Show branding should be generic show.", showID)
        brandingOverlay = "BlueGeneral.png"

    #maxNumberOfLines = 4
    normalizedText, lines, text = normalize(showName, True)
    if lines > 4:
        normalizedText, lines, text = normalize(showName, False)
        if lines > 6:
            log("DCM", "Show name is far too long, runs over 6 lines", showID, "Within function applyBrand().")
            raise Exception 

# Determines which background image to use for the show image.
    img = Image.open(backgroundImagePath + str(randint(1,16)) +".png")

# Opens overlay and pastes over the background image
    overlay = Image.open(colouredBarsPath + brandingOverlay)
    img.paste(overlay, (0, 0), overlay)

# ShowName formatting
    log("DEBUG", "Formatting the showName.", showID)
    # textFont = ImageFont.truetype(<font-file>, <font-size>)
    textFont = ImageFont.truetype("Raleway-Bold.ttf", text)
    
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(normalizedText, textFont)
        
    # changes the start position, to centre text vertically
    if lines == 3:
        textLineHeight = 230
    elif lines == 2:
        textLineHeight = 275
    elif lines == 1:
        textLineHeight = 300
    elif lines == 4:
        textLineHeight = 205
    else:
        textLineHeight = 205

    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((800-w)/2, textLineHeight),normalizedText,(255,255,255),textFont, align='center')

# website URY formatting
    log("DBEUG", "Applying website branding.", showID)
    websiteURL = 'URY.ORG.UK/LIVE \n @URY1350'
    websiteTextSize = 50
    websiteFont = ImageFont.truetype("Raleway-SemiBoldItalic.ttf", websiteTextSize)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(websiteURL, websiteFont)
    websiteURLHeight = 510 

    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((800-w)/2, websiteURLHeight), websiteURL,(255,255,255),websiteFont, align='center')

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
    elif showName == "URY SPORT: Grandstand":
        log("DEBUG", "Applying news branding.", showID)
        output = 'News'
    elif showName == "University Radio Talk":
        log("DEBUG", "Applying news branding.", showID)
        output = 'News'
    
    elif showName == "URY:PM - (( URY Music ))":
        log("DEBUG", "Applying music branding.", showID)
        output = 'Music'
    elif showName == "((URY)) Music: Bedtime Mix":
        log("DEBUG", "Applying music branding.", showID)
        output = 'Music'
    
    elif showName[:10] == "URY Brunch":
        log("DEBUG", "Applying flagship branding.", showID)
        output = 'Flagship'
    elif showName[:17] == "URY Afternoon Tea":
        log("DEBUG", "Applying flagship branding.", showID)
        output = 'Flagship'
    elif showName[:8] == "URY:PM -":
        log("DEBUG", "Applying flagship branding.", showID)
        output = 'Flagship'
    elif showName == "National Award Nominated URY:PM with National Award Nominated K-Spence":
        log("DEBUG", "Applying flagship branding.", showID)
        output = 'Flagship'

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
    elif showName[:9] == "URY:PM - ":
        log("DEBUG", "Removing 'URY:PM -' from the title.", showID)
        output = showName[9:]
    elif showName[:19] == "URY Afternoon Tea: ":
        log("DEBUG", "Removing 'URY:PM -' from the title.", showID)
        output = showName[19:]
    else:
        log("DEBUG", "No prefix to be removed from the title.", showID)
        output = showName
    return output


def normalize(input, firstAttmpt):
    """
    A function to split the show name into seperate lines of maximum lengths.
    Args:
        input (str): The Show name.
        firstAttmpt (Bool): Is this the first attempt at normalising the text?
    Return:
        Two strings. firstLine is the first line of text. otherLines is the string of other lines with line breaks inserted when necessary.
    """
    log("DEBUG", "Running normalize() function.", showID)
    words = input.split(" ")
    LinesList = []

    longestWord = 0
    for word in words:
        if len(word) > longestWord:
            longestWord

    if longestWord <= 17 and firstAttmpt:
        maxLineLength = 17
        text = 65
    else:
        maxLineLength = 34
        text = 40

    for word in words:
        if len(word) > maxLineLength:
            log("DCM", "Word too long for image.", showID, "Within function normalize().")
            raise Exception
        elif len(LinesList) > 0 and (len(LinesList[-1]) + len(word) < maxLineLength):
            LinesList[-1] += " " + word
        else:
            LinesList.append(word)

    normalizedText = "".join(item + "\n" for item in LinesList)
    lines = normalizedText.count('\n')
    return normalizedText, lines, text


def log(typeM="DEBUG", message="NONE", showNum="NULL", errorMessage="No exception error message."):
    """
    A function to output logs to a log file for debugging or exceptions.
    Args:
        typeM (str): The type of log to make.
        mesage (str): The message to explain the log.
        showNum (str): The show ID (if there is one).
        errorMessage (str): The exception (if there is one).
    """
    if  (debugMode == 'T') or (typeM == "DCM") or (typeM == "API"):
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