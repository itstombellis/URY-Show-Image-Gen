from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from random import randint

imagePath = "images/"

def add_text(showName, outputName):
    """
    Args:
        showName (str): Show name to add to image.
    Output:
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
    Args:
        input (str): Takes in a string for a show name.
    Returns:
        A string containg line breaks so the text is not longer that 14 characters (including spaces)
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
    '''
    Takes the output of normalise and counts the number of line breaks. 
    Returns the height depen
    '''
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
#add_text('URY Brunch Some Show Name')
#add_text('URY:PM Some Show Name')
#add_text('Some Show Name')
#add_text('Building Bridges - TheRoadtoRockandRoll and Roll')
#print(normalize("Building Bridges - The Road to Rock and Roll"))


## This runs through a file to generate show images.
'''output =[]
f = open('Shows.txt', 'r')
for line in f:
    output.append(line)
f.close()
for i in range(0,len(output)):
    output[i] = output[i].rstrip('\n')
for el in output:
    add_text(el)
'''
ShowsDict = {12209: 'URY:PM - URY Chart Show', 12868: 'URY:PM - Roku Radio', 12374: 'URY Newshour', 12928: 'No Ducks Given', 12957: '(20,000 Leagues) Into the Void', 13000: "What's That Topic?", 13008: 'Stage', 13049: 'York Sport Report', 13065: 'URY Brunch: The Saturday Lie-In', 13067: "Georgie and Angie's Book Corner", 13070: 'Gully Riddems', 13071: 'Indie Unearthed', 13073: 'Building Bridges - The Road to Rock and Roll', 13074: 'Castle Sessions', 13120: 'Pardon my French', 13123: 'Your Opinion is Wrong', 13125: 'The Night Call', 13126: 'InsomniHour', 13130: "What's on my playlist?", 13134: "Diggin' Deep", 13140: 'Barry Tomes', 13141: 'Topics & Tunes', 13149: 'RapChat', 13156: 'Morning Glory', 13159: 'The 20th Century Collection', 11628: 'Retrospectre!', 13167: 'Star Struck Jack and The Mystery Cat', 13177: 'Kick back Sundays with Kate ', 13179: 'URY:PM (( URY Music ))', 13184: 'The Late Night Bass Podcast', 13186: 'These Charming Girls', 13189: 'Grumpy Youngish Men', 13192: "Leckie's listeners", 13202: 'Dylan with a Mike!', 13204: 'The Right Faces For Radio', 13209: 'Things Can Only Get Bitter', 13227: 'Fringe: Full Metal Racket', 13228: 'URY Brunch: Star-Struck Jack and the Mystery Cat', 13232: 'URY Brunch - Breakfast Club', 13233: "URY Brunch - We're All Ears", 13235: 'Catchy Chunes', 13245: 'In Between Days', 13246: 'No DLC Required', 13255: 'The Breakz Showcase ', 13256: 'URY Brunch - Amateur Hour', 13257: "Grandad's Jazz", 13258: 'URY:PM - Peculiarities', 13259: 'Tales from the Phantasmagoria', 13260: 'URY:PM - Willis Weekly', 13261: 'Almost Audible', 13262: 'Cream Cheese', 13263: "#URYonTOUR: Freshers' 2016", 13264: 'URY:PM - No Ducks Given', 13265: 'Screen', 13266: 'URY Brunch - The Culture Show', 13267: 'URY Whisper Show', 13268: 'URY Brunch - Smile!', 13269: 'Midweek Marauders', 13270: 'Hidden Gems', 13271: 'Go Funk Yourself', 13272: 'The Brighter Side of Life', 13273: "Peck's Picks", 13274: 'Toons in the Afternoons', 13275: 'Roger That', 13276: 'The Eclectic Mix', 13277: 'The Alternative Music Show', 13278: 'DESERT ISLAND DISCO', 13279: 'coHEARence', 13280: 'Formula 1 Analysis', 13282: 'AM-bassador', 13283: 'Liv and the guy', 13284: 'Monday Chills ', 13285: 'Your Weekend', 13287: 'Non-Stop-Tom', 13288: 'Cool Britannia', 13289: 'Nothing but Chuuuunes with Hayds', 13290: 'The Ben and Jasper Show', 13291: 'Why Not?', 13292: 'Alternative Juice', 13293: "Chef Will - Where there's a Will, there's a...", 13294: 'NOUVEAU.', 13295: 'Kiltie Pleasures with Jonny ', 13296: 'Brain Waves', 13297: 'The Sounds of Time', 13298: "Josh and Tom's Afternoon Antics", 13299: 'Music for Old People', 13300: 'GAYdio', 13301: 'PolChat', 13302: 'Vanbrugh Chair Debate', 13303: 'URY Presents: UYCB 2016 Winter Concert', 13304: 'NICturnal', 13305: 'Speech Showcase', 13306: 'More Songs About Chocolate And Girls...', 13307: 'URY Does RAG Courtyard Takeover'}
for key in ShowsDict:
    add_text(ShowsDict[key], str(key))