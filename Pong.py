"""
PONG

Written by Mayur Saxena
Written for Mr. Reid
ICS3U, Culminating Project
Date Started: December 3, 2012
Date Completed: December 10, 2012

This is a Pong game, with 1 player and 2 player modes.
It also has a highscore feature.
Program is written in Python, using the pygame library.
"""

# Just as a note, every time we make a new screen, we need to make our corner pixel (0,0) a different color.
# The reason for this is that in our main game loop, we check whether the mouse is clicked in a certain boundary
# This boundary exists all the time, even when we're not on that specific screen, so we need something to determine which screen we're on
# And add that to our click check
# That where the pixel colors come in

# BLACK - Main Menu
# WHITE - Help Screen
# RED - Pick Controls ( after 1 Player)
# GREEN - 2P
# BLUE - Highscores
# YELLOW - Instructions for controls
# AQUA - Play screen
# GREY - Difficulty

# In most of the things in this game, there are many animations and movements. Unfortunately, there is no delete function or anything like that
# And I have to do a SCREEN.fill(BLACK), that's partially why there are so many functions
# I originally thought I could just make the item black, and I know something happened that it didn't work, I just can't remember what
# Or I was just doing it wrong :)

import pygame, random, sys, math, datetime # We need the pygame library, random, and sys, and math and datetime

from pygame.locals import * # This imports all the constants from pygame.locals such as mouse events and keys

import pygame.mixer # This is for sounds

now = datetime.datetime.now() # We put this here on the off chance that the user leaves Pong open all the time, so that highscore dates keep updating

# Function called initialize, does all the necessary stuff
def initialize():

	pygame.init() # Initialize pygame

	global FPS, FPSCLOCK, WINDOWWIDTH, WINDOWHEIGHT, TITLEFONT, TEXTFONT, CREDITFONT, SCREEN, BLACK, WHITE, RED, GREEN, BLUE, YELLOW, AQUA, GREY, running, scoreOne, scoreTwo, count, leftExit, rightExit, wallHit, paddleHit, sound # Make these vars global, to be used outside the function

	scoreOne = -1 # Scores used in the game, scoreOne is also used in 1P mode, to save variable creation space... Set them to -1 so showWin doesn't write to file on startup
	scoreTwo = -1
	count = 0 # This is our file writing counter, to make sure we don't get 50 million lines because the user can't click at the same speed as the processor
	FPS = 60 # Set our max FPS to 60
	FPSCLOCK = pygame.time.Clock() # Used to set max FPS
	WINDOWWIDTH = 640 # The width of the window
	WINDOWHEIGHT = 480 # The height of the window
	TITLEFONT = pygame.font.Font('data/arcadeclassic.ttf',128) # Font used for headings, eg. PONG, HELP, etc.
	TEXTFONT = pygame.font.Font('data/arcadeclassic.ttf',48) # Font used on main menu for play, help, quit
	CREDITFONT = pygame.font.Font('data/arcadeclassic.ttf',36) # Font used for credits on main menu
	APPICON = pygame.image.load('data/pong.png')#Load our pong image
	pygame.display.set_icon(APPICON) # Set it to our game icon	
	SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT)) # A blank canvas, made with our size, no end to the possibilities
	BLACK = (0,0,0) # Black has this value in RGB, every color after this is made on the same basis (it makes the code easier to type and read)
	WHITE = (255,255,255)
	RED = (255,0,0)
	GREEN = (0,255,0)
	BLUE = (0,0,255)
	YELLOW = (255,255,0)
	AQUA = (0,255,255)
	GREY = (84,84,84)
	pygame.display.set_caption("Pong") # The title bar says Pong
	running = 1 # A variable to keep the game running

	try: # This is for error catching, do we have a method to play sound? Unfortuantely, the school computers don't work without headphones.
		pygame.mixer.init() # If we do, initialize the mixer
		sound = True # Set sound to True, which will be used
		leftExit = pygame.mixer.Sound('data/Exit Left.ogg') # 4 Sounds, made global vars
		rightExit = pygame.mixer.Sound('data/Exit Right.ogg')
		wallHit = pygame.mixer.Sound('data/Wall Hit.ogg')
		paddleHit = pygame.mixer.Sound('data/Paddle Hit.ogg')
	except: # If it throws an error, ignore it, and:
		sound = False # Tell the program we don't have sound
		print "Sound not initialized... No audio device found!" # Print this message, to where, I have no idea

	return # end the function

initialize() # Call the initialize function so that we can use the variables and such in our future code

class Label: # This is a label class, which makes it easier to make labels... myLabel = Label(TITLEFONT,"Hello, World", 240), self == myLabel
	def __init__(self, font, text, y, x=320, surface=SCREEN): # Parameters which are needed to make the label, the last two, x and surface, have default values, so they are optional
		self.textSurface = font.render(text, True, WHITE, BLACK) # The label has a property called textSurface, which is a Surface object containing text
		self.textRect = self.textSurface.get_rect() # It also has a property called textRect, which is a rectangle made to the size of the textSurface
		self.textRect.center = (x, y) # Let's set the position of the textRect, anchored from the center, as that makes more sense than topLeft
		surface.blit(self.textSurface, self.textRect) # Output the textSurface to SCREEN, using the coordinates of textRect as a destination
						   # The reason we make a rect is because blit uses the top left of the rectangle, and it is hard to calculate that
		return

class Button(Label): # This is a button class, which inherits the same __init__ from label, because a button is the same as a label, just with extra stuff... Created same as label

	def wasClicked(self, pixelColor, linePos = 10, surface=SCREEN): # The button has a method wasClicked, which takes in a pixelColor (screen identity), an optional lineShift down and an optional surface
		if event.type == pygame.MOUSEBUTTONDOWN: # If our event was a mouse button down, aka a click (derived from global variable in getInput function)
			mouseX, mouseY = event.pos # We'll have two vars, mouseX and mouseY, referring to the x+y pos of where the mouse was clicked
										# If the mouseX is between our passed in element's right and left boundaries, and mouseY is between top and bottom, and our left corner pixel is a certain color
			if (mouseX < self.textRect.right) and (mouseX > self.textRect.left) and (mouseY > self.textRect.top) and (mouseY < self.textRect.bottom) and surface.get_at((0,0)) == pixelColor:
				return True # end the function, giving back True

		if event.type == pygame.MOUSEMOTION: # If our event was a mouse movement (derived from the for loop in the main game loop)
			mouseX, mouseY = event.pos # We'll have two vars, mouseX and mouseY, referring to the x+y pos of where the mouse was clicked
										# If the mouseX is between our passed in element's right and left boundaries, and mouseY is between top and bottom, and our left corner pixel is a certain color
			if (mouseX < self.textRect.right) and (mouseX > self.textRect.left) and (mouseY > self.textRect.top) and (mouseY < self.textRect.bottom) and surface.get_at((0,0)) == pixelColor:
				pygame.draw.line(surface, WHITE, (self.textRect.left,self.textRect.bottom-linePos),(self.textRect.right,self.textRect.bottom-linePos)) # Draw a white line at the coordinates of the textRect (see Label), and take away 10, so that the line is closer to the text
				return
			elif surface.get_at((0,0)) == pixelColor: # If you're still on the same screen as the button being tested
				pygame.draw.line(surface, BLACK, (self.textRect.left,self.textRect.bottom-linePos),(self.textRect.right,self.textRect.bottom-linePos)) # Draw a black line in the exact same spot as the white, so that when the mouse moves away, it looks like the line disappeared
				return

class Paddle: # A class to make our paddles
	def __init__(self,x,y): # Takes two parameters, an xPos and a yPos
		self.rect = pygame.Rect(x,y,10,60) # Property called rect, a Rectangle object with set size of 10W x 60H
		return

	def move(self,yShift): # A move method
		self.rect = self.rect.move(0,yShift) # Taking advantage of builtin Rect.move(x,y), where rect is a Rect object

		# This code here checks whether the paddle is touching the walls (bounds checking)
		if self.rect.top < topWall.bottom: # If the y, according to top of the rectangle is less than the bottom of topWall,
			self.rect.top = topWall.bottom # make y touch the topWall
			return
		elif self.rect.bottom > bottomWall.top: # If the bottom of the rect is more than the top of bottomWall
			self.rect.bottom = bottomWall.top # make y the bottomWall's top pos
			return
		# topWall and bottomWall are declared in createArena

class Ball(): # A ball class

	def __init__(self): # The first call, no parameters required, as we are only creating 1 ball, and it will be moving right after spawn

		self.rect = pygame.Rect(320,240,20,20) # make a rectangle (20x20 square), at (320,240)

		self.rect.centerx = WINDOWWIDTH / 2 # Center the rectangle x-wise
		self.rect.centery = WINDOWHEIGHT / 2 # Center the rectangle y-wise
		self.speed = 0 # Our inital speed is 0, so the ball doesn't start abruptly
		self.angle = random.randint(-45, 45) # Our serve angle is a random integer between -45 and 45 (from 315 to 0 and 0 to 45)

		if abs(self.angle) < 15: # If our angle (in positive form) is between 0 and 14 inclusive
			self.angle = random.randint(20,40) # randomize the angle in a more reasonable range, because from 0-14 is very close to a flat line
		if random.random() > .5: # If a random decimal number between 0 and 1 is more than 0.5, subtract 180 from it, to reverse the serve direction
			#i.e an angle of 30 becomes 150
			self.angle = 180 - self.angle

		return

	def reset(self): #Put the ball back in the middle and stop it from moving

		self.rect.centerx = WINDOWWIDTH / 2 # Ball centered in screen x-wise
		self.rect.centery = WINDOWHEIGHT / 2 # Ball centered in screen y-wise
		self.speed = 0 # Change our speed to 0
		self.angle = random.randint(-45, 45) # Do the whole angle thing again from __init__, so that each serve generates a new game, so to speak

		if abs(self.angle) < 15:
			self.angle = random.randint(20,40)
		if random.random() > .5:
			self.angle = 180 - self.angle

		return

	def beginMovement(self): # This is the real deal, the layers in the cake, the meat of the game, etc.

		global scoreOne, scoreTwo # As Google and I discovered, using global variables is fine, but as soon as you update them, they change their scope from global to local, only to be used in this function
		# To combat that issue, we declare them as global in the top of our function
		# http://bobobobo.wordpress.com/2009/03/21/unboundlocalerror-local-variable-referenced-before-assignment/

		# Although I know basic trigonometry, which helped quite a bit, I still needed some help from the Internet
		# For the next two lines, I'd like to thank http://www.pygame.org/docs/tut/tom/games4.html for this page on vector physics,
		# and Mr. Doyle and my dad for giving me a solid understanding of trig, so I know what this code is doing

		# Also this picture is good for angle references
		# http://en.wikipedia.org/wiki/File:Degree-Radian_Conversion.svg

		# All this will happen regardless of being a 1P or 2P game

		self.rect.x += self.speed * math.cos(math.radians(self.angle)) # in this triangle, speed is like the hypotenuse, and the angle is in relation to the origin, at the top left of the screen cosA = ADJ/HYP -> cos(angle) = x/speed -> cos(angle) * speed = x
		# We add it to the existing x so that the ball's current position is increased by the x amount
		self.rect.y += self.speed * math.sin(math.radians(self.angle)) # same as above, except sinA = OPP/HYP -> sin(angle) = y/speed -> sin(angle)*speed = y

		if self.rect.top < topWall.bottom: # Did the top of the ball hit the bottom of topWall (declared in createArena)
			if sound == True: # If we do have sound
				wallHit.play() # play this sound
			self.rect.top = topWall.bottom + 1 # separate the ball from the top wall, so it doesn't stick
			self.angle *= -1 # multiply the angle by -1, so that it bounces ie. 80 becomes -280
			self.speed += incrementValue # add increment value to the speed, so that speed gradually increases

		elif self.rect.bottom > bottomWall.top: # Same thing as the above, except using bottom wall
			if sound == True: # If we do have sound
				wallHit.play() # play this sound
			self.rect.bottom = bottomWall.top - 1 # and move the ball up instead of down (- vs +)
			self.angle *= -1
			self.speed += incrementValue

		if self.speed == 0: # If the ball is stopped
			if pygame.key.get_pressed()[K_SPACE]: # And the user presses space
				self.speed = 8 # Make the speed 8

		if self.speed < 8 and self.speed > 0 : # If the speed ends up decreasing to less than 8
			self.speed = 8 # Make it 8
				# We need to have more than 0 otherwise ball.reset doesn't work

		if gameMode == "1P": # Things specific to happen in a 1P game
			if self.rect.colliderect(paddle1.rect): # Taking advantage of builtin function colliderect, which returns True if 2 rectangles overlap each other
				if sound == True: # If we do have sound
					paddleHit.play() # play this sound
				scoreOne += 1 # Increase scoreOne, which, in this case, is counting returns, but I thought I would just reuse variables
				self.angle = 180 - self.angle # This time we subtract the angle from 180, to make it bounce
				self.rect.left = paddle1.rect.right+1 # Move the ball so it doesn't stick

			elif self.rect.right > rightWall.left: # If the ball hits rightWall, also declared in createArena
				if sound == True: # If we do have sound
					paddleHit.play() # I can't decide whether this should be a wall hit or a paddle, but I stuck with paddle
				self.angle = 180 - self.angle # Bounce the ball
				self.speed += random.uniform(-(incrementValue*2),incrementValue*2) # Increase or decrease the speed using decimal numbers between -1 and +1, to simulate opponent hitting back with more force or less
				self.rect.right = rightWall.left - 1 # Move the ball away from the all
				self.rect.y += random.randint(-20,20)/3.0 # This line is supposed to simulate backspin on a ball
				# Does it work... Maybe, but I'd have to get some user feedback as to whether it messes them up

		else: # Things happening specific in a 2P game

			if self.rect.left < 0: # The ball leaves the arena, on the left side
				if sound == True: # If we do have sound
					leftExit.play() # play sound
				scoreTwo+=1 # scoreTwo, which is the right player's score, is increased
				createArena(scoreOne,scoreTwo) # Make the arena, passing in scoreOne and scoreTwo
				self.reset() # Call the reset method, to put the ball in the middle, and stop it

			elif self.rect.right > 640: # Ball leaves on the right side
				if sound == True: # If we do have sound
					rightExit.play() # play sound
				scoreOne +=1 # Increase left player's score
				createArena(scoreOne,scoreTwo) # Make the arena again
				self.reset() # Reset the ball

			elif self.rect.colliderect(paddle1.rect): # Paddle and ball collide
				if sound == True: # If we do have sound
					paddleHit.play() # play sound
				self.angle = 180 - self.angle # Bounce the ball
				self.speed -= 0.25 # Decrease the speed by a bit
				self.rect.left = paddle1.rect.right+1 # Move the ball away
				self.rect.y += random.randint(-20,20)/3.0 # Again, an attempt at backspin

			elif self.rect.colliderect(paddle2.rect): # Same as above, except "unstick" the ball in the opposite direction
				if sound == True: # If we do have sound
					paddleHit.play() # play sound
				self.angle = 180 - self.angle
				self.speed -= 0.25
				self.rect.right = paddle2.rect.left - 1
				self.rect.y += random.randint(-20,20)/3.0

# Function called createMainMenu
def createMainMenu():

	global oneplayer, twoplayer, highscores, help, quit # Global variables so that we can check mouse pos with their pos (buttons, wasClicked)

	SCREEN.fill(BLACK) # The background color for our screen is BLACK... For some reason the screen is black without this anyways

	# Make a whole bunch of labels and buttons

	title = Label(TITLEFONT,"PONG", 40)
	oneplayer = Button(TEXTFONT,"1 joueur", 120)
	twoplayer = Button(TEXTFONT,"2 joueurs", 200)
	highscores = Button(TEXTFONT,"scores", 270)
	help = Button(TEXTFONT,"aide", 340)
	quit = Button(TEXTFONT,"quitter", 410)
	credits = Label(CREDITFONT,"Par Mayur Saxena Copyright 2013",460)
	#beta = Label(CREDITFONT,"BETA", 30, 510)

	SCREEN.set_at((0,0),BLACK) # Make the screen identifying pixel black

	return # End the function

# Function called createHelpScreen
def createHelpScreen():

	global back # Our global variable back, which is our back button

	SCREEN.fill(BLACK) # Let's fill our screen with black

	# Make a whole bunch of labels and buttons

	back = Button(CREDITFONT,"Back",13,42)
	title = Label(TITLEFONT,"HELP",40)
	line1 = Label(CREDITFONT,"DEPOSIT QUARTER",130)
	line2 = Label(CREDITFONT,"SPACE  TO  SERVE",170)
	oneplayer = Label(TEXTFONT,"One Player",240)
	line3 = Label(CREDITFONT,"AVOID MISSING FOR HIGHSCORE",280)
	twoplayer = Label(TEXTFONT,"Two Player",360)
	line6 = Label(CREDITFONT,"FIRST TO 10 WINS",400)

	SCREEN.set_at((0,0),WHITE) # Oh look, a white pixel in the corner this time!

	return # End the function

def createHighscores():

	global back, f, reset # Back button and file f is global

	SCREEN.fill(BLACK) # Fill the screen

	title = Label(TITLEFONT,"SCORES", 40) # Make a title and a back button
	back = Button(CREDITFONT,"Back",13,42)
	reset = Button(CREDITFONT,"Reset",13,590)

	lineList = [] # A blank list to start off with
	f = open("data/highscores.txt","r+") # Open up highscores.txt, in both read and write mode

	for line in f: # For each line in our file, which is a list element
		line = line.replace("\n","") # Replace the new line character with nothing, because our font generates a square for that char
		lineList.append(line) # And append it to our list

	lineList.sort(reverse = True) # Sort our new list from big to small, going by the first digit
	# This is why we need to add a 00 to our 1 digit scores, and a 0 to 2 digit scores, and I don't think anybody is going to get above 999, so I didn't worry about it
	# If all first digits are the same, it moves on to second digits

	for i in range(0,len(lineList)): # For i in range 0 to the length of the list (remember range excludes the last number, which works out fine because lists are 0-indexed

		score = lineList[i][:lineList[i].index(",")] + "  returns" # Score is the current list element, substringed (is this even a word), up until the comma
		# Nothing in front of the colon means from the beginning, could have also used 0
		date = lineList[i][lineList[i].index(",")+1:lineList[i].rindex(",")] # The date is the current list element, going from one more than the comma, to the last comma found
		# Recall the 0-indexing and the exclusion of last number
		level = lineList[i][lineList[i].rindex(",")+1:len(lineList[i])] # From the last comma plus one, to the end of the line

		Label(CREDITFONT,str(date),50+(50*(i+1)), 120) # Make a label, with no specific name, using the date as the score, starting 50 down from the top
		# and incrementing by 50 for each label (50x1, 50x2, 50x3, etc.), and the x is 120
		Label(CREDITFONT,str(score),50+(50*(i+1)), 360) # Same thing, except use score text, y-pos being identical to the date label, but move it over to the right to 440

		Label(CREDITFONT,str(level),50+(50*(i+1)), 560) # Same thing, different text, more to the right

	SCREEN.set_at((0,0),BLUE) # Our screen identifier is BLUE

	return #get out of the function

def pickControls():

	global back, keyboard, mouse # More global vars

	SCREEN.fill(BLACK) # Black screen

	# Make a whole bunch of labels and buttons

	back = Button(CREDITFONT,"retourne",13,82)
	title = Label(TITLEFONT,"Controles", 150)
	keyboard = Button(TEXTFONT,"clavier", 250)
	mouse = Button(TEXTFONT,"souris d ordinateur", 310)

	SCREEN.set_at((0,0),RED) # Red screen identifier

	return

def chooseDifficulty():

	global back, easy, med, hard # Global vars

	SCREEN.fill(BLACK) # Black screen

	back = Button(CREDITFONT,"Back",13,42) # Buttons and labels
	title = Label(TITLEFONT,"NIVEAU",150)
	easy = Button(TEXTFONT,"facile",250)
	med = Button(TEXTFONT,"Moyen",310)
	hard = Button(TEXTFONT,"difficile",370)

	SCREEN.set_at((0,0),GREY) # Grey screen identifier

	return

def showInstructions(controlMethod, whichGame):

	global back, start # More global vars

	SCREEN.fill(BLACK) # Black screen

	back = Button(CREDITFONT,"Back",13,42) # Back button
	start = Button(TEXTFONT,"START",440) # Start button

	if whichGame == "1P": # The user selected 1 Player
		if controlMethod == "keyboard": # The user clicked keyboard
			instruction = Label(TEXTFONT,"Use   W   for up and   S   for down",240) # Make this label
		else: # The user clicked mouse
			instruction = Label(TEXTFONT,"Move mouse up and down",240) # Make this label

	else: # User chose 2 Player, so keyboard is assumed
		instruction = Label(TEXTFONT,"P1    Use    W    and    S",210) # Make this label
		instruction2 = Label(TEXTFONT,"P2    Use    UP    and    DOWN",270) # Make this label

	SCREEN.set_at((0,0),YELLOW) # Yellow pixel

	return

def createArena(lScore, rScore): # A method to create the playing screen, everything except paddles
								# 2 scores are passed in
	global topWall, bottomWall, rightWall
	SCREEN.fill(BLACK) # fill the screen with black


	if gameMode == "1P": # The game is a 1P game
		rightWall = pygame.Rect(635,0,5,WINDOWHEIGHT) # Make a right wall, which is like a person in real life using a wall
		pygame.draw.rect(SCREEN,WHITE,rightWall) # Draw the white wall on the screen
		hits = Label(CREDITFONT,"COUPS", 20, 260) # Make a hits label
		hitNum = Label(CREDITFONT,str(lScore), 20, 370) # Make a hits score label, which has the text set to the string of lScore, which is scoreOne

	else: # Game is a 2P game

		leftScore = Label(TEXTFONT,str(lScore),20,290) # make a label for the score of the left side
		rightScore = Label(TEXTFONT,str(rScore),20,350) # and the right side, converting ints to strs

	# This stuff here happens regardless of game mode
	topWall = pygame.Rect(0,0,WINDOWWIDTH,5) # make a top wall, starting at 0,0, as wide as the window, and as tall as 5 pixels
	bottomWall = pygame.Rect(0,475,WINDOWWIDTH,5) # same thing, except at the bottom
	pygame.draw.rect(SCREEN,WHITE,topWall) # actually draw the wall
	pygame.draw.rect(SCREEN,WHITE,bottomWall) # actually draw the wall
	pygame.draw.line(SCREEN,WHITE,(320,0),(320,480)) # a line down the middle, similar to real Pong

	SCREEN.set_at((0,0),AQUA) # a new screen identifier

	return

def initializeGameComponents(gameType): # Make some paddles and a ball, based on which game

	global paddle1, paddle2, ball, scoreOne, scoreTwo, count # We need to be able to access these paddles, and remember that global variable update fiasco?

	if gameType == "1P": # If the user chose 1 player
		paddle1 = Paddle(20,230) # make paddle1 here

	else: # The user chose 2P
		paddle1 = Paddle(20,230) # make paddle1 here
		paddle2 = Paddle(600,230) # and paddle2 here

	# Make a ball no matter what
	ball = Ball()
	scoreOne = 0 # Reset the scores, or set the scores from -1 to 0
	scoreTwo = 0
	count = 0 # Reset our file writing counter

def moveGameComponents(): # moveGameComponents function, different than Paddle.move

	global scoreOne, scoreTwo

	if SCREEN.get_at((0,0)) == AQUA: # If we are on the play screen
		if gameMode == "1P": # and this is a 1P game
			if inputSystem == "keyboard": # and we are using a keyboard
				if pygame.key.get_pressed()[K_w]: # W is being pressed
					paddle1.move(-13) # Do Paddle.move(yShift), where yShift is -30
										# because 0,0 is at the top, so we actually get closer to 0
				if pygame.key.get_pressed()[K_s]: # S is being pressed
					paddle1.move(13) # Move down 13 instead

			else: # We are using a mouse
				if event.type == pygame.MOUSEMOTION: # If our event is MOUSEMOTION, according to the for loop in the while
					mouseY = event.pos[1] # lets set mouseY to the second element of event.pos tuple (array) (0-indexed)
					paddle1.move(mouseY - paddle1.rect.center[1]) # Do paddle.move, where the shift is current mouse pos - the y pos of the paddle's center, rect.center is an array of x,y coords

			if ball.rect.right < 0: # If the ball leaves the screen
				showWin("not left or right") # call showWin
				return # get out of this function so that the text of show win can stay on screen


		else: # 2P game
			if pygame.key.get_pressed()[K_w]: # Same as 1P, except do the same thing for another paddle
				paddle1.move(-13)
			if pygame.key.get_pressed()[K_s]:
				paddle1.move(13)
			if pygame.key.get_pressed()[K_UP]: # Using the UP and DOWN arrows for second paddle
				paddle2.move(-13)
			if pygame.key.get_pressed()[K_DOWN]:
				paddle2.move(13)

			if scoreOne == 10: # If scoreOne is equal to 10
				showWin("left") # call showWin
				return # get out of this function
			elif scoreTwo == 10:
				showWin("right") # call showWin
				return #get out of this function
		
		# Regardless of game mode, call the ball's beginMovement method
		ball.beginMovement()

		createArena(scoreOne,scoreTwo)
		 # Create an arena again, to wipe out everything and use the scores

		drawChanges(gameMode) # draw the changes, function defined below

def drawChanges(gameType):

	if gameType == "1P": # In a 1P game
		pygame.draw.rect(SCREEN,WHITE,paddle1.rect) # We need to redraw paddle1

	else:  # In a 2P game
		pygame.draw.rect(SCREEN,WHITE,paddle1.rect) # We need to redraw 2 paddles
		pygame.draw.rect(SCREEN,WHITE,paddle2.rect)

	pygame.draw.rect(SCREEN,WHITE,ball.rect) # Regardless, we need to draw the ball
		# We can't use initializeGameComponents, because there we have hardcoded positions for our paddles
	return

def showWin(winner):

	global count, menu, playagain # We need to have count global to modify it

	if winner == "left": # If we passed in left, meaning scoreOne is 10
		win = Label(TITLEFONT,"WIN", 200, 160) # Make all this
		menu = Button(TEXTFONT,"Main  Menu", 280, 160)
		playagain = Button(TEXTFONT,"Play  Again", 360, 160)
		return

	elif winner == "right":

		win = Label(TITLEFONT,"WIN", 200, 480) # Make all this here instead
		menu = Button(TEXTFONT,"Main  Menu", 280, 480)
		playagain = Button(TEXTFONT,"Play  Again", 360, 480)
		return

	else:
		win = Label(CREDITFONT,"votre Score est " + str(scoreOne), 200, 480) # Make all this here instead
		menu = Button(TEXTFONT,"Menu", 280, 480)
		playagain = Button(TEXTFONT,"Jouer Encore", 360, 480)
		pygame.event.set_grab(False)
		
		if scoreOne < 10 and scoreOne > -1 and count == 0: # Anywhere from 0-9, ignoring -1 so no write on startup and count is 0
			if sound == True: # If we do have sound
				leftExit.play() # We play this sound here so it only does it once and no infinite looping of it
			count += 1 # Increment count so that the same line isn't written over and over (refer to initialize)
			f.write("00"+str(scoreOne)+","+str(now.year) + "  " + str(now.month) + "  " + str(now.day) + "," + levelChoice + "\n")
			# Write in a 00 plus the score, so 8 results in 008 (needed for sorting), then a comma, then the year, month, and day eg. 08,2012  12  9

		elif scoreOne > 9 and scoreOne < 100 and count == 0: # Above 9, count is 0
			if sound == True: # If we do have sound
				leftExit.play() # We play this sound here so it only does it once and no infinite looping of it
			count += 1 # Increment count
			f.write("0"+str(scoreOne)+","+str(now.year) + "  " + str(now.month) + "  " + str(now.day) + "," + levelChoice + "\n")
			# Same thing here, just with one 0
			
		elif scoreOne > 99 and count == 0:
			if sound == True: # If we do have sound
				leftExit.play() # We play this sound here so it only does it once and no infinite looping of it
			count += 1 # Increment count
			f.write(str(scoreOne)+","+str(now.year) + "  " + str(now.month) + "  " + str(now.day) + "," + levelChoice + "\n") # With no extra 0
			
		return

def getInput():

	global event, incrementValue, levelChoice, gameMode, inputSystem # Event is global for button.wasClicked, and gameMode and inputSystem are required elsewhere

	for event in pygame.event.get():

		if oneplayer.wasClicked(BLACK): # Refer to wasClicked in the Button class
			gameMode = "1P" # Set gameMode to "1P", to be passed into showInstructions
			pickControls() # The user has to pick controls
	
		elif mouse.wasClicked(RED):
			pygame.event.set_grab(True)
			inputSystem = "mouse" # Set inputSystem to mouse,  to be passed in
			chooseDifficulty()
	
		elif keyboard.wasClicked(RED):
			inputSystem = "keyboard"
			chooseDifficulty()
	
		elif twoplayer.wasClicked(BLACK):
			inputSystem = "keyboard" # Keyboard is assumed
			gameMode = "2P" # Two player
			incrementValue = 0.5
			showInstructions(inputSystem,gameMode) # Show the instructions
	
		elif highscores.wasClicked(BLACK):
			createHighscores()
	
		elif help.wasClicked(BLACK): # User clicked help on main menu
			createHelpScreen() # Make a help screen
	
		elif quit.wasClicked(BLACK): # User clicked quit
			pygame.quit() #deinitialize pygame
			sys.exit() #exit the program
	
		elif back.wasClicked(WHITE,7) or back.wasClicked(RED,7) or back.wasClicked(GREEN,7) or back.wasClicked(BLUE,7): # User clicks back on any screen except the preStart screen (YELLOW)
			createMainMenu() # Go to the main menu
	
		elif back.wasClicked(GREY,7): # User clicks back on pre-start and they chose 1 Player
			pygame.event.set_grab(False) # Unlock mouse cursor from screen
			pickControls() # The previous screen was picking controls
	
		elif back.wasClicked(YELLOW,7) and gameMode == "1P": # User clicks back on pre-start and they chose 1 Player
			chooseDifficulty() # The previous screen was picking controls
	
		elif back.wasClicked(YELLOW,7) and gameMode != "1P": # User clicks back on pre-start and they chose anything but 1 Player
			createMainMenu() # The previous screen was a main menu
	
		elif start.wasClicked(YELLOW): # User clicks start
			createArena(scoreOne,scoreTwo)
			initializeGameComponents(gameMode)
	
		elif reset.wasClicked(BLUE):
			f = open("data/highscores.txt","w") # Opening a file in write only mode erases everything
			f.close() # Close the file, free up memory
			createHighscores() # Reflect the changes on screen
	
		elif menu.wasClicked(AQUA,0): # If they click menu on win screen, and for some reason the line only works when the line is at the rect border
			pygame.event.set_grab(False) # Unlock mouse cursor from screen
			createMainMenu() # make a menu
	
		elif playagain.wasClicked(AQUA,0): # if play again was clicked on win screen, and same story with the line not working
			createArena(0,0) # make an arena with scores 0,0
			initializeGameComponents(gameMode) # make new paddle(s) and a ball
			if inputSystem == "mouse":
				pygame.event.set_grab(True)
	
		elif easy.wasClicked(GREY): # Easy was clicked on level select
			incrementValue = 0.1
			levelChoice = "easy"
			showInstructions(inputSystem, gameMode)
	
		elif med.wasClicked(GREY):
			incrementValue = 0.3
			levelChoice = "medium"
			showInstructions(inputSystem, gameMode)
	
		elif hard.wasClicked(GREY):
			incrementValue = 0.5
			levelChoice = "hard"
			#showInstructions(inputSystem, gameMode)
			createArena(scoreOne,scoreTwo)
			initializeGameComponents(gameMode)
			
	
		elif event.type == pygame.QUIT: # enables use of red X on window bar
			pygame.quit() # same as the quit button
			sys.exit()

chooseDifficulty() # Initialize some vars
createHighscores() # We need to open the file f
showWin("herpaderp") # Call showWin passing anything to initialize menu and playagain
showInstructions("keyboard","1P") # Call this to initialize the vars, otherwise errors occur
pickControls() # Call this to initialize the vars, otherwise errors occur
createMainMenu() # The main menu overwrites the help screen, so let's make one and keep it here

while running: # 1 is the same as True, so back in our initialize(), we made a variable called running
	
	getInput() # Get all our button clicks and such
	moveGameComponents() # Keep moving the paddle and ball while the game is running

	pygame.display.update() # constantly update the display, looking for any blits or fills or things like that
	FPSCLOCK.tick(FPS) # Our FPS of 60
