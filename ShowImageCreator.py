from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from random import randint
import json, sys, requests


imagePath = "images/"

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


def add_text(showName, outputName):
    """
    A function to create a show image for given show name and output file name.
    Args:
        showName (str): Show name to add to image.
        outputName (str): The name of the outputfile, standard form including the show id.
    Return:
        The function outputs a JPG image to a sub folder called ShowImages.
    """
    print(showName) #Prints to the console which show is being processed.

    # This looks at the name of the show whether it is a flagship or not.
    if showName == '':
        raise Exception("No show name provided.")
    elif showName[:10] == 'URY Brunch': #AM Flagship
        img = Image.open(imagePath + "AMFlagshipBackground.png")
    elif showName[:6] == 'URY:PM': #PM Flagship
        img = Image.open(imagePath + "PMFlagshipBackground.png")
    
    # If the show is not flagship, there is a list of backgrounds to randomly generate a show image.
    else:
        rGI = randint(1,15)
        img = Image.open(imagePath + "Other" + str(rGI) +".png") #Image backgrounds must be in the form of "Other[int].png" adjust the random int function depending on the amount of other images.
    
    #This works out if the show name will fit neatly on the image, if the show name is less than 14 characters the normalize function will not be called.
    if len(showName) <= 14:
        prshowName = showName
    else:
        prshowName = normalize(showName)
    
    #Adds the text to the selected image.
    font_size = 85
    # font = ImageFont.truetype(<font-file>, <font-size>)
    font = ImageFont.truetype("Raleway-SemiBoldItalic.ttf", font_size)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(prshowName, font)
    height = lineCount(prshowName)
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw.text(((800-w)/2, height),prshowName,(255,255,255),font, align='center')
    img.save('Showimages/%s.jpg' %outputName)

def normalize(input):
    """
    A funtion to insert line breaks so that the text is no longer than 14 characters (including spaces) so that it will fit in the drawn box.
    Args:
        input (str): Takes in a string for a show name.
    Return:
        A string containg line breaks so the text is not longer than 14 characters (including spaces).
    """
    output = []
    for word in input.split(" "):
        if len(word) > 14:
            raise Exception("Word too long for image. Contact DCM.")
        elif len(output) > 0 and (len(output[-1]) + len(word) < 14):
            output[-1] += " " + word
        else:
            output.append(word)

    if len(output) > 4:
        raise Exception("Spans too many lines for image. Contact DCM.")

    return "".join(item + "\n" for item in output)

def lineCount(input):
    """
    A function that takes the output of normalise and counts the number of line breaks.
    Args:
        input (str): The string to have number of lines calculated after being normalized
    Return:
        The height depenending on the number of lines the string will occupy.
    """
    lines = input.count('\n')
    if lines == 0:
        output = 190
    elif lines == 2:
        output = 150
    elif lines == 3:
        output = 105
    else:
        output = 65
    return (output)

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
    add_text(ShowsDict[key], str(key))
