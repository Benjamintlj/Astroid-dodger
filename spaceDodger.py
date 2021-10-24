#importing pygame and Initialising it aswell as random
import pygame, random, pickle
pygame.init()


#---global variables---
#creating the window
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
#declairing the rock object list
rockList = []


#---classes---
#class for the player, inherits object
class PlayerClass(object):
    #setting the variables for when the class is instantiated
    def __init__(self):
        #setting the height and width of the player
        self.height = 50
        self.width = 100
        #the players x and y coordinates 
        self.__x = 100
        self.__y = 150
        #image of the player
        self.__image = pygame.image.load('space-ship.png')
    
    def displaySelf(self):
        '''
        displays the player when called, ready for the next frame
        '''
        screen.blit(self.__image, (self.__x, self.__y))

    def boundarys(self):
        '''
        calculates the coordinates of where the image ends
        '''
        self.top = self.__y
        self.bottom = self.__y + self.height
        self.left = self.__x
        self.right = self.__x + self.width
        return (self.top, self.bottom, self.left, self.right)
    
    def reset(self):
        '''
        resets any variables that may have changed when playing the game
        '''
        self.__y = 150

    @property
    def y(self):
        '''
        returns the y value, necessary for the setter to work
        '''
        return self.__y

    @y.setter
    def y(self, newY):
        '''
        takes a input value for how much y should change, 
        if the player will go out of bounds then the new y value will be rejected
        '''
        if self.__y > 10 and self.__y < (screenHeight - 60):
            self.__y += newY
        elif self.__y >= (screenHeight - 60) and newY < 0:
            self.__y += newY
        elif self.__y <= 10 and newY > 0:
            self.__y += newY

#class for the enemy rocks
class Rock:
    #setting the variables for when the class is instantiated
    def __init__(self):
        #setting the height and width of the class
        self.height = 25
        self.width = 25
        #setting the image that will be displayed for the rock
        self.__image = pygame.image.load('small-Rock.png')
        #setting the spawn location of the rock on the x and y axis
        self.xLocationRock = screenWidth
        self.yLocationRock = random.randrange(0,screenHeight)
        #setting the speed and direction the rock will go in, speed on the x axis is dependent on the score
        self.xVelocityRock = (random.randrange(5,10) + scoreObject.scoreValue/100) * -1
        self.yVelocityRock = float(random.randrange(-10,10))/10
    
    def cornerTupleGenerator(self):
        '''
        calculates the coordinates of the rock images corners
        returns a tuple 
        '''
        self.topLeft = (self.xLocationRock, self.yLocationRock)
        self.topRight = (self.xLocationRock + self.width, self.yLocationRock)
        self.bottomLeft = (self.xLocationRock, self.yLocationRock + self.height)
        self.bottomRight = (self.xLocationRock + self.width, self.yLocationRock + self.height)
        return (self.topLeft, self.topRight, self.bottomLeft, self.bottomRight)

    def move(self):
        '''
        moves the rock by its pre defined velocity values
        '''
        self.xLocationRock += self.xVelocityRock
        self.yLocationRock += self.yVelocityRock

    def displaySelf(self):
        '''
        will call the move method to move the object
        will then display the object ready for the next frame
        '''
        self.move()
        screen.blit(self.__image, (self.xLocationRock, self.yLocationRock))

#class for the scoring system
class Score:
    #setting the variables for when the class is instantiated
    def __init__(self):
        #setting the score for when the game starts
        self.score = 0
        #setting the location the score will be displayed
        self.xLocationScore = screenWidth - 200
        self.yLocationScore = 10
        #sets the font style and size for the score
        self.font = pygame.font.Font('freesansbold.ttf', 32)
    
    def increaseScore(self):
        '''
        increments the score after each frame
        '''
        self.score += 5
    
    def displaySelf(self):
        '''
        defines the text content and colour
        displays it ready for the next frame in predefined x and y axis
        '''
        self.scoreText = self.font.render('score: ' + str(self.score), True, (255,255,255))
        screen.blit(self.scoreText, (self.xLocationScore, self.yLocationScore))
    
    @property
    def scoreValue(self):
        '''
        returns the current score
        '''
        return self.score

    def reset(self):
        '''
        sets all changed variables back to what they were when the game started
        '''
        self.score = 0


#---functions---
def eventCheckerQuit():
    '''
    if escape button pressed, quit the game
    '''
    for quitEvent in pygame.event.get():
        #if i press exit, the game will close
        if quitEvent.type == pygame.QUIT:
            pygame.quit()

def eventChecker():
    '''
    checks to see if if the user has press the up or down arrow
    if they press up then the spaceship will go up -y
    if they press down then the spaceship will go down +y
    '''
    keyPressed = pygame.key.get_pressed()
    if keyPressed[pygame.K_UP]:
        user.y = -10
    if keyPressed[pygame.K_DOWN]:
        user.y = 10

def baseSettingsUpdate(delayTime):
    '''
    delays the next frame so that the game will run at the same speed no matter the processing power
    sets the title at the top of the window
    sets the background colour to black
    '''
    pygame.time.delay(delayTime)
    pygame.display.set_caption('Space Dodger')
    screen.fill((0,0,0))

def displayObjects():
    '''
    this function displays all the objects
    '''
    user.displaySelf()

    for i in rockList:
        i.displaySelf()

def newRock():
    '''
    generates a new rock
    '''
    if random.randrange(0,20) == 1:
        rockList.append(Rock())

def collideCheck():
    '''
    checks to see if the player has collided with a rock
    if they have then the game ends
    '''
    global running
    #gets the boundarys from the user, type is tuple
    playerBoundarys = user.boundarys()
    #loops through each rock that has been made
    for rock in rockList:
        #gets the corner coordinates from the rock objects
        rockCorners = rock.cornerTupleGenerator()
        #loops though each of the corners
        for rockCorner in rockCorners:
            #if any one of the corners is within the player boundarys
            if rockCorner[1] < playerBoundarys[1] and rockCorner[1] > playerBoundarys[0] and rockCorner[0] > playerBoundarys[2] and rockCorner[0] < playerBoundarys[3]:
                #ends the game
                running = False

def reset():
    '''
    resets all the variables, back to what they were when the game started
    '''
    global rockList
    rockList = []
    user.reset()
    scoreObject.reset()

def game():
    '''
    main game function
    '''
    global running
    running = True
    reset()
    #---game loop---
    while running:
        #anythings that need to be done before the rest of the loop runs
        baseSettingsUpdate(50)

        #checking for events
        eventCheckerQuit()
        eventChecker()

        #displays all the objects
        displayObjects()

        #updates the score and places it onto the screen
        scoreObject.displaySelf()
        scoreObject.increaseScore()

        #updating the screen
        pygame.display.update()

        #collision detection
        collideCheck()

        #spawns a new rock
        newRock()
    
    return scoreObject.scoreValue

def scoreUploader(score):
    '''
    when game is over
    sets high score
    '''
    #sets the font
    fontGameOver = pygame.font.Font('freesansbold.ttf', 32)
    #set the content and font colour
    gameOverText = fontGameOver.render('GAME OVER', True, (255,255,255))
    scoreText = fontGameOver.render('Score: ' + str(score) , True, (255,255,255))
    enterNameText = fontGameOver.render('Enter name', True, (255,255,255))
    #setting variables
    textEntered = ''
    nameEntered = False
    #main loop
    while not nameEntered:
        baseSettingsUpdate(0)

        '''
        checks if the escape button has been pressed and will escape
        checks what key has been pressed
        if backspace, remove letter from textEntered
        if enter, upload name and score to file
        if char key, char appended to textEntered
        '''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    textEntered = textEntered[:-1]
                elif event.key == pygame.K_RETURN:
                    uploadData(textEntered, score)
                    nameEntered = True
                else:
                    if len(textEntered) < 12:
                        textEntered += event.unicode
        
        #displays text content
        screen.blit(gameOverText, ((screenWidth/2 -87), 100))
        screen.blit(scoreText, ((screenWidth/2 -87), 200))
        screen.blit(enterNameText, ((screenWidth/2 -87), 300))

        #generates a surface and displays it ready for next frame
        textEnteredWithFont = fontGameOver.render(textEntered,True,(255,255,255))
        screen.blit(textEnteredWithFont,((screenWidth/2 -87),400))

        #updates display
        pygame.display.flip()

def uploadData(name, score):
    '''
    appends the name and score to the file
    '''
    fileName = 'highScores.pkl'

    try:
        #loads file contents, appends new data, saves data to file
        file = open(fileName, 'rb')
        data = pickle.load(file)
        file.close()
        data += [[name, score]]
        file = open(fileName, 'wb')
        pickle.dump(data, file)
        file.close()
    except:
        #if no data can be loaded, just store data
        data = [[name, score]]
        file = open(fileName, 'wb')
        pickle.dump(data, file)
        file.close()

def downloadData():
    '''
    loads data, and orders it based on the second element in each element
    '''
    file = open('highScores.pkl', 'rb')
    data = pickle.load(file)
    data.sort(key=lambda x: x[1])
    return data

def leaderboard():
    '''
    displays the leaderboard
    '''
    #condition for the main loop
    leaderboardRunning = True
    #gets the sorted leaderboard
    sortedLeaderboard = downloadData()
    #sets the font
    fontLeaderboard = pygame.font.Font('freesansbold.ttf', 32)
    #sets the content and font colour
    leaderboardText = fontLeaderboard.render('Leaderboard', True, (255,255,255))
    menuText = fontLeaderboard.render('Menu', True, (255,255,255))
    #if there is content then display the player in nth postion, else say No sortedLeaderboard
    try:
        firstText = fontLeaderboard.render(('1st {} {}').format(sortedLeaderboard[-1][0], sortedLeaderboard[-1][1]), True, (255,255,255))
    except:
        firstText = fontLeaderboard.render(('1st No sortedLeaderboard'), True, (255,255,255))
    try:
        secondText = fontLeaderboard.render(('2nd {} {}').format(sortedLeaderboard[-2][0], sortedLeaderboard[-2][1]), True, (255,255,255))
    except:
        secondText = fontLeaderboard.render(('2nd No sortedLeaderboard'), True, (255,255,255))
    try:
        thirdText = fontLeaderboard.render(('3rd {} {}').format(sortedLeaderboard[-3][0], sortedLeaderboard[-3][1]), True, (255,255,255))
    except:
        thirdText = fontLeaderboard.render(('3rd No sortedLeaderboard'), True, (255,255,255))
    #main loop
    while leaderboardRunning:
        eventCheckerQuit()
        baseSettingsUpdate(0)
        #gets the mouse position
        mouseX, mouseY = pygame.mouse.get_pos()

        #displays content
        screen.blit(leaderboardText, ((screenWidth/2 -87), 100))
        screen.blit(firstText, ((screenWidth/2 -87), 200))
        screen.blit(secondText, ((screenWidth/2 -87), 300))
        screen.blit(thirdText, ((screenWidth/2 -87), 400))
        
        #menu button, if hover then go back to main menu
        menuButton = pygame.Rect(screenWidth/2 -100, 500, 200, 50)
        pygame.draw.rect(screen, (127, 143, 166), menuButton)
        screen.blit(menuText, (screenWidth/2 -25, 512))
        if menuButton.collidepoint((mouseX, mouseY)):
            leaderboardRunning = False

        #update the display
        pygame.display.update()

def menu():
    #so the loop runs
    running = True

    #setting the fonts
    fontHeader = pygame.font.Font('freesansbold.ttf', 32)
    fontButtons = pygame.font.Font('freesansbold.ttf', 25)

    #setting the content and the colours
    mainMenuText = fontHeader.render('Main Menu', True, (255,255,255))
    mainMenuGameText = fontButtons.render('Play', True, (255,255,255))
    mainMenuScoreText = fontButtons.render('Leader board', True, (255,255,255))

    #main loop
    while True:
        baseSettingsUpdate(0)
        eventCheckerQuit()
        #gets the postion of the mouse
        mouseX, mouseY = pygame.mouse.get_pos()
        
        #title
        screen.blit(mainMenuText, ((screenWidth/2 -87), 100))

        #buttons
        #game button, if hover then play the game
        gameButton = pygame.Rect(screenWidth/2 -100, 200, 200, 50)
        pygame.draw.rect(screen, (127, 143, 166), gameButton)
        screen.blit(mainMenuGameText, (screenWidth/2 -25, 212))
        if gameButton.collidepoint((mouseX, mouseY)):
            scoreUploader(game())

        #leaderboard button, if hover then show the leaderboard
        scoreButton = pygame.Rect(screenWidth/2 -100, 300, 200, 50)
        pygame.draw.rect(screen, (127, 143, 166), scoreButton)
        screen.blit(mainMenuScoreText, (screenWidth/2 -82, 312))
        if scoreButton.collidepoint((mouseX, mouseY)):
            leaderboard()

        #update the display
        pygame.display.update()


#---instantiating the classes---
user = PlayerClass()
scoreObject = Score()
newRock()


#---starting code---
menu()