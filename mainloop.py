import pygame
import pygame_menu
import sys
import time
import csv
import os
import pygame_widgets
from pygame_widgets.button import ButtonArray
from PIL import Image, ImageDraw, ImageFont
from fillpdf import fillpdfs

import ctypes

if not ctypes.windll.shell32.IsUserAnAdmin():
    print('Not enough priviledge, restarting...')
    import sys
    ctypes.windll.shell32.ShellExecuteW(
        None, 'runas', sys.executable, ' '.join(sys.argv), None, None)
else:
    print('Elevated privilege acquired')

# Temporary definitions to troubleshoot file etc. TODO: fix these
expInfo = {}

expInfo['date'] = 'Date'


os.environ["SDL_VIDEO_CENTERED"] = "1"
# Set up Pygame
padding = 100
pygame.init()
pygame.font.init() # you have to call this at the start if you want to use the module
clock = pygame.time.Clock()

# Setup the display
surface = pygame.display.set_mode()
displayX, displayY = surface.get_size()
surface = pygame.display.set_mode((displayX-10, displayY-10),pygame.RESIZABLE,display=0)
x, y = surface.get_size()
surfaceRectangle = surface.get_rect()

## Let's set up everything for the text
font1 = pygame.font.Font(pygame.font.match_font('arial'), 50)
font2 = pygame.font.Font(pygame.font.match_font('impact'), 55)
my_font = pygame.font.Font('freesansbold.ttf', 50)
fontslist=[font1,font1,font1,font1,font1]
black = (0,0,0)
textTopPadding = 200
menuPadding = 100 # value in pixels


### Boolean Values go here ###
textDrawn = False
run = True
stimShow = False
displayStimuli = False
showInstructions = False
stimClear = False
mainMenuShow = True

## Here's how we work with our time stuff
# currentTime = pygame.time.get_ticks()
trialDict = {}
trialResponses = {}
dictIndex = 0
trialIndex = 0
danvasubtest = 'Adult' # TODO: make this dependent on selection from menu
data_dict = {}
stimsList = {}
correctAnswers = {}
incorrectAnswers = {}
errorList = []
NamesCorrectAnswers = {}
intensity = ''
gender = ''
genderOfAnswer = ''
intensityOfAnswer = ''
correctAnswerForString = ''
currentAnswer = 0

# This is a begin experiment comment in the code section of the readymessage section
highIntensityErrors = 0
lowIntensityErrors = 0
errorList = []
skippedErrors = 0
errorsByMisjudgement = 0
totalErrors = 0
totalerrors = 0
happyHighIntensityErrors = 0
happyLowIntensityErrors = 0
sadHighIntensityErrors = 0
sadLowIntensityErrors = 0
angryHighIntensityErrors = 0
angryLowIntensityErrors = 0
fearfulHighIntensityErrors = 0
fearfulLowIntensityErrors = 0
happyErrors = 0
sadErrors = 0
angryErrors = 0
fearfulErrors = 0
lowIntensityErrors = 0
misattributedHappySad = 0
misattributedHappyAngry = 0
misattributedHappyFearful = 0
misattributedSadHappy = 0
misattributedSadAngry = 0
misattributedSadFearful = 0
misattributedAngryHappy = 0
misattributedAngrySad = 0
misattributedAngryFearful = 0
misattributedFearfulHappy = 0
misattributedFearfulSad = 0
misattributedFearfulAngry = 0
maleHappyErrors = 0
maleSadErrors = 0
maleAngryErrors = 0
maleFearfulErrors = 0
maleTotalErrors = 0
femaleHappyErrors = 0
femaleSadErrors = 0
femaleAngryErrors = 0
femaleFearfulErrors = 0
femaleTotalErrors = 0

dictionaryloop = 0
dictionaryloop2 = 0
# This is to set the number of the trial for scoring the right data

dictionarydefinitions = ["participant","age","skippedErrors","totalErrors","totalerrors","happyHighIntensityErrors","happyLowIntensityErrors",
                         "sadHighIntensityErrors","sadLowIntensityErrors","angryHighIntensityErrors",
                         "angryLowIntensityErrors","fearfulHighIntensityErrors","fearfulLowIntensityErrors",
                         "happyErrors","sadErrors","angryErrors","fearfulErrors","lowIntensityErrors",
                         "highIntensityErrors","misattributedHappySad","misattributedHappyAngry",
                         "misattributedHappyFearful","misattributedSadHappy","misattributedSadAngry",
                         "misattributedSadFearful","misattributedAngryHappy","misattributedAngrySad",
                         "misattributedAngryFearful","misattributedFearfulHappy","misattributedFearfulSad",
                         "misattributedFearfulAngry","errorsByMisjudgement","danvasubtest","maleHappyErrors",
                         "maleSadErrors","maleAngryErrors","maleFearfulErrors","maleTotalErrors",
                         "femaleHappyErrors","femaleSadErrors","femaleAngryErrors","femaleFearfulErrors","femaleTotalErrors",
                         "totalErrors1","totalErrors2","happyErrors2","sadErrors2","angryErrors2","fearfulErrors2",]
# this is a comment "before experiment"

file = ('data/adult.csv')
with open(file, newline='') as csvfile:
    trialSetupConditions = csv.DictReader(csvfile)
    # trialConditions = csv.reader(csvfile, delimiter=',', quotechar='|')
    for lines in trialSetupConditions:
        trialDict[dictIndex] = (lines)
        dictIndex = dictIndex + 1
        
print (trialDict)

def showStim(showStim):
    global displayStimuli, stimShow
    if showStim == True:
        displayStimuli = True
        #print('ShowStim is' + str(stimShow))
        
    
def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    global textDrawn
    rect = rect
    y = pygame.Rect(rect).top
    lineSpacing = -2
    # get the height of the font
    fontHeight = font.size("Tg")[1]
    while text:
        i = 1
        # determine if the row of text will be outside our area
        if y + fontHeight > pygame.Rect(rect).bottom:
            break
        # determine maximum width of line
        while font.size(text[:i])[0] < pygame.Rect(rect).width and i < len(text):
            i += 1
        # if we've wrapped the text, then adjust the wrap to the last word
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1
        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)
        surface.blit(image, (pygame.Rect(rect).left, y))
        y += fontHeight + lineSpacing
        # remove the text we just blitted
        text = text[i:]
    # textDrawn = True
    return text

def printClicked(emotion):
    # print(emotion)
    pass
    
def colorClickedButton(button):
    global fontslist # this is so we can alter the list outside this function
    for index, item in enumerate(fontslist):
        fontslist[index] = font1
    fontslist[button - 1] = font2 # we must subtract 1 since we changed the button numbers for continue to be 0
    
    if button == 0:
        fontslist[button] = font1
        for index, item in enumerate(fontslist):
            fontslist[index] = font1

def handleClickedButton(button):
    global currentAnswer
    # some counters are: trialIndex 
    global trialIndex
    colorClickedButton(button)
    if button == 0:
        trialDict[trialIndex]['response'] = str(currentAnswer)
        print(currentAnswer)
        currentAnswer = 0
        print(currentAnswer)
        trialIndex = trialIndex + 1 # update trial index
    else:
        currentAnswer = button
        
    
# Creates an array of buttons
def drawButtons():
    global displayStimuli
    ButtonArray(
    # Mandatory Parameters
    surface,  # Surface to place button array on
    x/9,  # X-coordinate
    y-(y/8),  # Y-coordinate
    x*(8/10),  # Width
    100,  # Height
    (5, 1),  # Shape: 2 buttons wide, 2 buttons tall
    border=10,  # Distance between buttons and edge of array
    texts=('Happy','Sad','Angry','Fearful','Continue'),  # Sets the texts of each button (counts left to right then top to bottom)
    # When clicked, print number
    fonts=(tuple(fontslist)),
    onClicks=((lambda: (printClicked('Happy'), handleClickedButton(1), ), lambda: (printClicked('Sad'),handleClickedButton(2)), lambda: (printClicked('Angry'), handleClickedButton(3)), lambda: (printClicked('Fearful'), handleClickedButton(4)),lambda: (printClicked('Continue'),handleClickedButton(0),showStim(True)))),
    colour = (255,255,255))
    
def displayInstructions():
    # surface.fill((200,200,200))
    textbox = ((surfaceRectangle[0]+padding),(surfaceRectangle[1]+textTopPadding),(surfaceRectangle[2]-padding*2),(surfaceRectangle[2]-padding))
    instructions = "I am going to show you some people's faces and I want you to tell me how they feel. I want you to tell me if they are happy, sad, angry, or fearful (scared). Let's get started. Click anywhere to begin. (Esc will quit)"
    drawText(surface, instructions, black, textbox, my_font)
    # pygame.display.flip()
    waitForStart()
    # run_the_game()
def displayUpdate(clear = 0):
    if clear == 0:
        events = pygame.event.get()
        pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
        pygame.display.update()
    else:
        surface.fill((200, 200, 200))
        events = pygame.event.get()
        pygame_widgets.update(events)
        pygame.display.update()
    
def waitForStart():
    global showInstructions, stimShow, displayStimuli
    # pygame.display.update()
    # pygame.display.flip()
    # time.sleep(.3)
    # display_stimuli()
    # drawButtons()
    waitingForStart = True
    while waitingForStart:        
        events = pygame.event.get()
        pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # stop here to debug with blit commands 
                # it will deactivate the pygame library
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                else:
                    showInstructions = True
                    stimShow = True
            if pygame.mouse.get_pressed()[0]:
                print("click!")
                showInstructions = True
                stimShow = True
                waitingForStart = False
                surface.fill((200,200,200))
                pygame.display.flip()
                pygame.display.update()
                displayStimuli = True
                pass

def display_stimuli(displayTime,stimuliStart,stimuliEndTime,currentTime):
    global mainMenuShow
    mainMenuShow = False
    global trialIndex
    
    print('Got into display stimuli function')
    global displayStimuli, stimShow
    (trialDict[trialIndex]['stimFile'])
    
    if displayStimuli == True:
        while currentTime < stimuliEndTime:
            currentTime = pygame.time.get_ticks()
            # print('Displaying Stimuli')
            try:
                print(trialDict[trialIndex]['stimFile'])
                displayUpdate()
                stimuli = pygame.image.load((trialDict[trialIndex]['stimFile'])).convert() # i did use (file).convert()
                stimuliWidth = stimuli.get_width()
                stimuliHeight = stimuli.get_height()
                
                    # pygame.display.flip()
                width, height = surface.get_size()
                pictureScale = .6
                # let's make sure we can scale the image according to actual window size.  Note I based
                # scaling off the display height to deal better with widescreen displays and different aspect ratios
                    # Here we will make the scaled picture pixel height
                scaledPictureHeight = height*(pictureScale)
                    # Here we will make the scaled picture pixel width.  Note we must base it
                    # off of the scaled picture height because we want to maintain the relation
                    # of the picture X being a multiple of the height.  
                scaledPictureWidth = (scaledPictureHeight/stimuliHeight)*stimuliWidth
                # Define variables according to scaled picture information
                pictureXCenter = (scaledPictureWidth/2)
                pictureYCenter = (scaledPictureHeight/2)
                pictureXStart = (width/2)-pictureXCenter
                pictureYStart = (height/2)-pictureYCenter
                # lets put the picture on the screen
                surface.blit(pygame.transform.scale(stimuli, (scaledPictureWidth, scaledPictureHeight)), (pictureXStart,pictureYStart))
            except:
                pass
        if currentTime >= stimuliEndTime:# and displayStimuli == True:
            surface.fill((200,200,200))
            pygame.display.flip()
            pygame.display.update()
            print('Surface filled')
            displayStimuli = False
            stimShow = False
            # trialIndex = trialIndex + 1

def createDictionary():
    global dictionaryloop, skippedErrors, totalErrors, data_dict, errorList,NamesCorrectAnswers, trialDict, incorrectAnswers, correctAnswers, stimsList, correctAnswerForString, femaleTotalErrors, maleTotalErrors
    global highIntensityErrors, lowIntensityErrors, happyErrors, sadErrors, angryErrors, fearfulErrors
    global happyHighIntensityErrors, happyLowIntensityErrors, sadHighIntensityErrors, sadLowIntensityErrors, angryHighIntensityErrors, angryLowIntensityErrors, fearfulHighIntensityErrors, fearfulLowIntensityErrors
    global femaleHappyErrors, femaleSadErrors, femaleAngryErrors, femaleFearfulErrors
    global maleHappyErrors, maleSadErrors, maleAngryErrors, maleFearfulErrors, misattributedHappySad, misattributedHappyAngry, misattributedHappyFearful, misattributedSadHappy, misattributedSadAngry, misattributedSadFearful, misattributedAngryHappy, misattributedAngrySad, misattributedAngryFearful, misattributedFearfulHappy, misattributedFearfulSad, misattributedFearfulAngry
    danvasubtest = 'Adult'
    data_dict = {}
    stimsList = {}
    incorrectAnswers = {}
    errorList = []
    NamesCorrectAnswers = {}
    intensity = ''
    gender = ''
    genderOfAnswer = ''
    intensityOfAnswer = ''
    
    for i in trialDict:
        # Let's do the basic things first:
        stimsList['stim' + str(dictionaryloop)] = (trialDict[dictionaryloop]['stimFile'])
        if trialDict[dictionaryloop]['response'] == '0':
            skippedErrors = skippedErrors + 1
        
        # Let's concact a string to fill in the correct answer with intensity and gender column, we'll start with emotion
        if trialDict[dictionaryloop]['correctAnswer'] == '1':
            correctAnswerForString = 'Happy '
        elif trialDict[dictionaryloop]['correctAnswer'] == '2':
            correctAnswerForString = 'Sad '
        elif trialDict[dictionaryloop]['correctAnswer'] == '3':
            correctAnswerForString = 'Angry '
        elif trialDict[dictionaryloop]['correctAnswer'] == '4':
            correctAnswerForString = 'Fearful '
        # Now let's grab the intensity
        if  trialDict[dictionaryloop]['intensity'] == '1':
            intensityOfAnswer = 'Low '
            
        elif trialDict[dictionaryloop]['intensity'] == '2':
            intensityOfAnswer = 'High '
        else:
            pass
        # Now let's grab the gender:
        if  trialDict[dictionaryloop]['stimuliGender'] == '1':
            genderOfAnswer = 'Female'
        elif trialDict[dictionaryloop]['stimuliGender'] == '2':
            genderOfAnswer = 'Male'
        else:
            pass
        # Now let's plug that into the PDF
        correctAnswers['correctAnswer'+ str(dictionaryloop)] = (correctAnswerForString) + (intensityOfAnswer) + (genderOfAnswer)

        if trialDict[dictionaryloop]['response'] != trialDict[dictionaryloop]['correctAnswer']:
            totalErrors = totalErrors + 1
            response = int(trialDict[dictionaryloop]['response'])
            correctAnswerKey = trialDict[dictionaryloop]['correctAnswer']
            
            if trialDict[dictionaryloop]['stimuliGender'] == '2':
                maleTotalErrors = maleTotalErrors + 1
            elif trialDict[dictionaryloop]['stimuliGender'] == '1':
                femaleTotalErrors = femaleTotalErrors + 1
            else:
                pass
            
            
            
            if  trialDict[dictionaryloop]['intensity'] == '1':
                lowIntensityErrors = lowIntensityErrors + 1
            elif trialDict[dictionaryloop]['intensity'] == '2':
                highIntensityErrors = highIntensityErrors + 1
            else:
                pass        
            
            if correctAnswerKey == '1':
                happyErrors = happyErrors + 1
                #correctAnswers['correctAnswer'+ str(dictionaryloop)] = 'Happy'
                if  trialDict[dictionaryloop]['intensity'] == '1':
                    happyLowIntensityErrors = happyLowIntensityErrors + 1
                elif trialDict[dictionaryloop]['intensity'] == '2':
                    happyHighIntensityErrors = happyHighIntensityErrors + 1
                else:
                    pass        

                if response == 2:
                    misattributedHappySad = misattributedHappySad + 1
                elif response == 3:
                    misattributedHappyAngry = misattributedHappyAngry + 1
                elif response == 4:
                    misattributedHappyFearful = misattributedHappyFearful + 1
                else:
                    pass
                if trialDict[dictionaryloop]['stimuliGender'] == '2':
                    maleHappyErrors = maleHappyErrors + 1
                elif trialDict[dictionaryloop]['stimuliGender'] == '1':
                    femaleHappyErrors = femaleHappyErrors + 1
                else: 
                    pass
                
            if correctAnswerKey == '2':
                sadErrors = sadErrors + 1
                if  trialDict[dictionaryloop]['intensity'] == '1':
                    sadLowIntensityErrors = sadLowIntensityErrors + 1     
                elif trialDict[dictionaryloop]['intensity'] == '2':
                    sadHighIntensityErrors = sadHighIntensityErrors + 1                
                else:
                    pass

                if response == 1:
                    misattributedSadHappy = misattributedSadHappy + 1
                elif response == 3:
                    misattributedSadAngry = misattributedSadAngry + 1
                elif response == 4:
                    misattributedSadFearful = misattributedSadFearful + 1
                else:
                    pass
                
                if trialDict[dictionaryloop]['stimuliGender'] == '2':
                    maleSadErrors = maleSadErrors + 1
                elif trialDict[dictionaryloop]['stimuliGender'] == '1':
                    femaleSadErrors = femaleSadErrors + 1
                else: 
                    pass
                
            if correctAnswerKey == '3':
                angryErrors = angryErrors + 1
                if  trialDict[dictionaryloop]['intensity'] == '1':
                    angryLowIntensityErrors = angryLowIntensityErrors + 1        
                elif trialDict[dictionaryloop]['intensity'] == '2':
                    angryHighIntensityErrors = angryHighIntensityErrors + 1                
                else:
                    pass
                
                if response == 1:
                    misattributedAngryHappy = misattributedAngryHappy + 1
                elif response == 2:
                    misattributedAngrySad = misattributedAngrySad + 1
                elif response == 4:
                    misattributedAngryFearful = misattributedAngryFearful + 1
                else:
                    pass
                
                if trialDict[dictionaryloop]['stimuliGender'] == '2':
                    maleAngryErrors = maleAngryErrors + 1
                elif trialDict[dictionaryloop]['stimuliGender'] == '1':
                    femaleAngryErrors = femaleAngryErrors + 1
                else: 
                    pass
                
            if correctAnswerKey == '4':
                fearfulErrors = fearfulErrors + 1
                if  trialDict[dictionaryloop]['intensity'] == '1':
                    fearfulLowIntensityErrors = fearfulLowIntensityErrors + 1
                elif trialDict[dictionaryloop]['intensity'] == '2':
                    fearfulHighIntensityErrors = fearfulHighIntensityErrors + 1
                else:
                    pass
                
                if response == 1:
                    misattributedFearfulHappy = misattributedFearfulHappy + 1
                elif response == 2:
                    misattributedFearfulSad = misattributedFearfulSad + 1
                elif response == 3:
                    misattributedFearfulAngry = misattributedFearfulAngry + 1
                else:
                    pass
                
                if trialDict[dictionaryloop]['stimuliGender'] == '2':
                    maleFearfulErrors = maleFearfulErrors + 1
                elif trialDict[dictionaryloop]['stimuliGender'] == '1':
                    femaleFearfulErrors = femaleFearfulErrors + 1
                else:
                    pass
                
            else:
                pass

            if response == 1:
                incorrectAnswers['incorrectAnswer'+ str(dictionaryloop)] = 'Happy'        
            elif response == 2:
                incorrectAnswers['incorrectAnswer'+ str(dictionaryloop)] = 'Sad'
            elif response == 3:
                incorrectAnswers['incorrectAnswer'+ str(dictionaryloop)] = 'Angry'
            elif response == 4:
                incorrectAnswers['incorrectAnswer'+ str(dictionaryloop)] = 'Fearful'
            else:
                incorrectAnswers['incorrectAnswer'+ str(dictionaryloop)] = 'Skipped'
        
        dictionaryloop = dictionaryloop + 1

def createPDF():
    global dictionaryloop, dictionaryloop2, correctAnswers, age, participant, errorsByMisjudgement
    age = ageInput.get_value()
    participant = participantInput.get_value()
    totalerrors = totalErrors
    errorsByMisjudgement = totalErrors - skippedErrors

    totalErrors1 = totalerrors
    totalErrors2 = totalerrors
    happyErrors2 = happyErrors
    sadErrors2 = sadErrors
    angryErrors2 = angryErrors
    fearfulErrors2 = fearfulErrors

    for i in (dictionarydefinitions):
        data_dict [dictionarydefinitions[dictionaryloop2]] = (eval(dictionarydefinitions[dictionaryloop2]))
        dictionaryloop2 = dictionaryloop2 + 1


    # data_dict.update(stimsList)
    # data_dict.update(expInfo)
    data_dict.update(stimsList)
    data_dict.update(expInfo)
    data_dict.update(incorrectAnswers)
    data_dict.update(correctAnswers)

    happycolor = "#00FF00"
    sadcolor = "#0000FF"
    angrycolor = "#FF0000"
    fearfulcolor = "#FFFF00"
    malecolor = "#FF8300"
    femalecolor = "#7800E1"

    widthmain = 480
    heightmain = 30

    totalerrorsincrement = widthmain/24

    widthmisattributions = 378
    heightmisattributions = 20
    errorsincrementmisattribute = widthmisattributions/18
    misattributionerrorsincrement = widthmisattributions/18

    widthgendererrors = 378
    errorsincrementgender = widthgendererrors/24
    gendererrorsincrement = widthgendererrors/24

    shape = [(0, 0), (widthmain, heightmain)]

    happystartx = 0
    happyendx = (happyErrors * totalerrorsincrement)
    sadstartx = happyendx
    sadendx = sadstartx + (sadErrors * totalerrorsincrement)
    angrystartx = sadendx
    angryendx = angrystartx + (angryErrors * totalerrorsincrement)
    fearfulstartx = angryendx
    fearfulendx = fearfulstartx + (fearfulErrors * totalerrorsincrement)

    happyrectangle = [(0, 0), (happyendx , heightmain)]
    sadrectangle = [(sadstartx,0),(sadendx,heightmain) ]
    angryrectangle = [(angrystartx,0), (angryendx, heightmain)]
    fearfulrectangle = [(fearfulstartx,0), (fearfulendx,heightmain)]
    
    # creating new Image object
    totalerrorsgraph = Image.new("RGB", (widthmain, heightmain),color = "#FFFFFF")
    # create rectangle image for happy errors
    happyerrorsrectangle = ImageDraw.Draw(totalerrorsgraph)
    saderrorsrectangle = ImageDraw.Draw(totalerrorsgraph)
    angryerrorsrectangle = ImageDraw.Draw(totalerrorsgraph)
    fearfulerrorsrectangle = ImageDraw.Draw(totalerrorsgraph)

    happyerrorsrectangle.rectangle(happyrectangle, fill =happycolor, outline=None)
    saderrorsrectangle.rectangle(sadrectangle, fill =sadcolor, outline=None)
    angryerrorsrectangle.rectangle(angryrectangle, fill =angrycolor, outline=None)
    fearfulerrorsrectangle.rectangle(fearfulrectangle, fill =fearfulcolor, outline=None)

    # totalerrorsgraph.show()
    totalerrorsgraph.save("src/graphPictures/totalerrorsgraph.jpg")
    # totalerrorsgraph.show()

    #create picture for happy misattributions

    happystartx = 0
    happyendx = (0) # only since we're on the happy misattributions graph
    sadstartx = happyendx
    sadendx = sadstartx + (misattributedHappySad * misattributionerrorsincrement)
    angrystartx = sadendx
    angryendx = angrystartx + (misattributedHappyAngry * misattributionerrorsincrement)
    fearfulstartx = angryendx
    fearfulendx = fearfulstartx + (misattributedHappyFearful * misattributionerrorsincrement)

    happyrectangle = [(0, 0), (happyendx , heightmisattributions)]
    sadrectangle = [(sadstartx,0),(sadendx,heightmisattributions) ]
    angryrectangle = [(angrystartx,0), (angryendx, heightmisattributions)]
    fearfulrectangle = [(fearfulstartx,0), (fearfulendx,heightmisattributions)]
    # creating new Image object
    happyMisattributionsGraph = Image.new("RGB", (widthmisattributions, heightmisattributions),color = "#FFFFFF")

    # create rectangle image for happy Errors
    happyErrorsrectangle = ImageDraw.Draw(happyMisattributionsGraph)
    sadErrorsrectangle = ImageDraw.Draw(happyMisattributionsGraph)
    angryErrorsrectangle = ImageDraw.Draw(happyMisattributionsGraph)
    fearfulErrorsrectangle = ImageDraw.Draw(happyMisattributionsGraph)

    sadErrorsrectangle.rectangle(sadrectangle, fill =sadcolor, outline=None)
    angryErrorsrectangle.rectangle(angryrectangle, fill =angrycolor, outline=None)
    fearfulErrorsrectangle.rectangle(fearfulrectangle, fill =fearfulcolor, outline=None)

    # happyMisattributionsGraph.show()
    happyMisattributionsGraph.save("src/graphPictures/happyMisattributions.jpg")

    happystartx = 0
    happyendx = (misattributedSadHappy * misattributionerrorsincrement) 
    sadstartx = happyendx
    sadendx = sadstartx # only since we're on the sad misattributions graph
    angrystartx = sadendx
    angryendx = angrystartx + (misattributedSadAngry * misattributionerrorsincrement)
    fearfulstartx = angryendx
    fearfulendx = fearfulstartx + (misattributedSadFearful*misattributionerrorsincrement)

    happyrectangle = [(0, 0), (happyendx , heightmisattributions)]
    angryrectangle = [(angrystartx,0), (angryendx, heightmisattributions)]
    fearfulrectangle = [(fearfulstartx,0), (fearfulendx,heightmisattributions)]


    # creating new Image object
    sadMisattributionsGraph = Image.new("RGB", (widthmisattributions, heightmisattributions),color = "#FFFFFF")

    # create rectangle image for happy Errors
    happyErrorsrectangle = ImageDraw.Draw(sadMisattributionsGraph)
    angryErrorsrectangle = ImageDraw.Draw(sadMisattributionsGraph)
    fearfulErrorsrectangle = ImageDraw.Draw(sadMisattributionsGraph)

    happyErrorsrectangle.rectangle(happyrectangle, fill =happycolor, outline=None)
    angryErrorsrectangle.rectangle(angryrectangle, fill =angrycolor, outline=None)
    fearfulErrorsrectangle.rectangle(fearfulrectangle, fill =fearfulcolor, outline=None)

    # sadMisattributionsGraph.show()
    sadMisattributionsGraph.save("src/graphPictures/sadMisattributions.jpg")

    happystartx = 0
    happyendx = happystartx + (misattributedAngryHappy * misattributionerrorsincrement) 
    sadstartx = happyendx
    sadendx = sadstartx + (misattributedAngrySad * misattributionerrorsincrement)
    angrystartx = sadendx
    angryendx = angrystartx # only since we're on the Angry misattributions graph
    fearfulstartx = angryendx
    fearfulendx = fearfulstartx + (misattributedAngryFearful * misattributionerrorsincrement)

    happyrectangle = [(0, 0), (happyendx , heightmisattributions)]
    sadrectangle = [(sadstartx,0),(sadendx,heightmisattributions) ]
    fearfulrectangle = [(fearfulstartx,0), (fearfulendx,heightmisattributions)]


    # creating new Image object
    angryMisattributionsGraph = Image.new("RGB", (widthmisattributions, heightmisattributions),color = "#FFFFFF")

    # create rectangle image for happy Errors
    happyErrorsrectangle = ImageDraw.Draw(angryMisattributionsGraph)
    sadErrorsrectangle = ImageDraw.Draw(angryMisattributionsGraph)
    fearfulErrorsrectangle = ImageDraw.Draw(angryMisattributionsGraph)

    happyErrorsrectangle.rectangle(happyrectangle, fill =happycolor, outline=None)
    sadErrorsrectangle.rectangle(sadrectangle, fill =sadcolor, outline=None)
    fearfulErrorsrectangle.rectangle(fearfulrectangle, fill =fearfulcolor, outline=None)

    # angryMisattributionsGraph.show()
    angryMisattributionsGraph.save("src/graphPictures/angryMisattributions.jpg")

    happystartx = 0
    happyendx = (misattributedFearfulHappy * misattributionerrorsincrement) 
    sadstartx = happyendx
    sadendx = sadstartx + (misattributedFearfulSad*misattributionerrorsincrement)
    angrystartx = sadendx
    angryendx = angrystartx + (misattributedFearfulAngry*misattributionerrorsincrement)
    fearfulstartx = angryendx
    fearfulendx = fearfulstartx # because we are making the fearful graph

    happyrectangle = [(0, 0), (happyendx , heightmisattributions)]
    sadrectangle = [(sadstartx,0),(sadendx,heightmisattributions) ]
    angryrectangle = [(angrystartx,0), (angryendx, heightmisattributions)]
    fearfulrectangle = [(fearfulstartx,0), (fearfulendx,heightmisattributions)]


    # creating new Image object
    fearfulMisattributionsGraph = Image.new("RGB", (widthmisattributions, heightmisattributions),color = "#FFFFFF")
    happyErrorsrectangle = ImageDraw.Draw(fearfulMisattributionsGraph) # create rectangle image for happy Errors
    sadErrorsrectangle = ImageDraw.Draw(fearfulMisattributionsGraph) 
    angryErrorsrectangle = ImageDraw.Draw(fearfulMisattributionsGraph) 
    happyErrorsrectangle.rectangle(happyrectangle, fill =happycolor, outline=None) 
    sadErrorsrectangle.rectangle(sadrectangle, fill =sadcolor, outline=None) 
    angryErrorsrectangle.rectangle(angryrectangle, fill =angrycolor, outline=None) 
    fearfulMisattributionsGraph.save("src/graphPictures/fearfulMisattributions.jpg")
    # fearfulMisattributionsGraph.show()
    # Gender Errors Graph
    malestartx = 0
    maleendx = malestartx + (maleTotalErrors * errorsincrementgender) 
    femalestartx = maleendx
    femaleendx = femalestartx + (femaleTotalErrors * errorsincrementgender)
    malerectangle = [(0, 0), (maleendx , heightmisattributions)]
    femalerectangle = [(femalestartx,0),(femaleendx,heightmisattributions) ]
    # creating new Image object
    genderErrorsGraph = Image.new("RGB", (widthgendererrors, heightmisattributions),color = "#FFFFFF")
    # create rectangle image for happy Errors
    maleTotalErrorsrectangle = ImageDraw.Draw(genderErrorsGraph)
    femaleTotalErrorsrectangle = ImageDraw.Draw(genderErrorsGraph)
    maleTotalErrorsrectangle.rectangle(malerectangle, fill =malecolor, outline=None)
    femaleTotalErrorsrectangle.rectangle(femalerectangle, fill =femalecolor, outline=None)
    # genderErrorsGraph.show()
    genderErrorsGraph.save("src/graphPictures/errorsbygender.jpg")



    # data_dict
    # Now let's insert the images

    fillpdfs.place_image('src/graphPictures/totalerrorsgraph.jpg', 124, 769, 'src/pdfMagic/blankDocumentNumberLine.pdf', 'src/pdfMagic/completed.pdf', 1, width=636, height=165)

    # These were the values before changing to the document with the number lines
    page2GraphStart = 120
    # page2GraphWidth = 283
    # page2GraphHeight = 15

    happygraphstarty = 161
    #The following are for the other graphs
    fillpdfs.place_image('src/graphPictures/happyMisattributions.jpg', page2GraphStart, happygraphstarty, 'src/pdfMagic/completed.pdf', 'src/pdfMagic/completed1.pdf', 2, width=widthmisattributions, height=heightmisattributions)
    fillpdfs.place_image('src/graphPictures/sadMisattributions.jpg', page2GraphStart, happygraphstarty-43, 'src/pdfMagic/completed1.pdf', 'src/pdfMagic/completed2.pdf', 2, width=widthmisattributions, height=heightmisattributions)
    fillpdfs.place_image('src/graphPictures/angryMisattributions.jpg', page2GraphStart, happygraphstarty-85, 'src/pdfMagic/completed2.pdf', 'src/pdfMagic/completed3.pdf', 2, width=widthmisattributions, height=heightmisattributions)
    fillpdfs.place_image('src/graphPictures/fearfulMisattributions.jpg', page2GraphStart, happygraphstarty-126, 'src/pdfMagic/completed3.pdf', 'src/pdfMagic/completed4.pdf', 2, width=widthmisattributions, height=heightmisattributions)
    fillpdfs.place_image('src/graphPictures/errorsbygender.jpg',page2GraphStart, happygraphstarty-238, 'src/pdfMagic/completed4.pdf', 'src/pdfMagic/completed.pdf', 2, width=widthmisattributions, height=heightmisattributions)

    fillpdfs.write_fillable_pdf('src/pdfMagic/completed.pdf', ('reports/'+participant+expInfo['date']+'completed.pdf'), data_dict, flatten=False) # was fillpdfs.write_fillable_pdf('src/pdfMagic/completed.pdf', 'reports/completed.pdf', data_dict, flatten=False)


    # for some reason I am not having luck directly openint the file, and some coding other than the most obvious seems necesary

    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath('reports/'+participant+expInfo['date']+'completed.pdf', cur_path)
    os.startfile(new_path)

def selectTest(value, test):
    # Do the job here !
    print(value)
    print(test)

def mainMenuState():#(state)
    global mainMenuShow, showInstructions
    print('mainMenyState')
    # if state == 0:
    mainMenuShow = False
    showInstructions = True
    displayInstructions()

width, height = surface.get_size()
# mainMenuShow = False

menu = pygame_menu.Menu('Welcome to the DANVA II test, please enter your information below', width - menuPadding, height - menuPadding,
                    theme=pygame_menu.themes.THEME_BLUE)

session = menu.add.text_input('Session :  ', default='001', onchange=print('this'))
participantInput = menu.add.text_input('Participant :  ', default='')
participant = participantInput.get_value() # put this in the pdf function
ageInput = menu.add.text_input('Age :    ', default='', onchange=print('this'))
#age = ageInput.get_value()


testSelector = menu.add.dropselect(
    title='Select Test',
    items=[('Adult', 1),
        ('African American', 2),
        ('Paralanguage', 3),
        ('Child', 4),
        ],
    # font_size=20,
    default=0,
    open_middle=False,  # Opens in the middle of the menu
    selection_box_height=10,
    selection_box_width=300,
    selection_infinite=True,

)
menu.add.button('Play', mainMenuState)
menu.add.button('Quit', pygame_menu.events.EXIT)
# menu.mainloop(surface)


while run:
    events = [pygame.event.wait()]
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            run = False
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                print("escape pressed")
                pygame.quit()
                run = False
                quit()
        if event.type == pygame.VIDEORESIZE:
            # There's some code to add back window content here.
            surface = pygame.display.set_mode((event.w, event.h),
                                            pygame.RESIZABLE)
            print(surface)
            print (surface.get_size())
            x, y = surface.get_size()
            surface.fill((200, 200, 200))
            pygame.display.flip()
    

    surface.fill((200, 200, 200))
    if mainMenuShow == True:
        menu.update(events)
        menu.draw(surface)  
        displayUpdate()  
        pygame.display.update()
        pygame.display.flip()
    if showInstructions == False and mainMenuShow == False: 
        print('Showing instructions')
        displayInstructions()
    if showInstructions == True:
        drawButtons()
    if displayStimuli == True:
        surface.fill((200, 200, 200))
        displayUpdate()  
        pygame.display.update()
        pygame.display.flip()
        drawButtons()
        stimuliStart = pygame.time.get_ticks()
        displayTime = 2
        stimuliEndTime = stimuliStart + (displayTime * 1000)
        currentTime = pygame.time.get_ticks()
        display_stimuli(displayTime,stimuliStart,stimuliEndTime,currentTime)

          
    # events = pygame.event.get()
    # pygame_widgets.update(events)  # Call once every loop to allow widgets to render and listen
    # pygame.display.update()
    displayUpdate()
    clock.tick(30)
    if trialIndex >= len(trialDict):
        createDictionary()
        createPDF()
        run = False
        pygame.quit()
        
