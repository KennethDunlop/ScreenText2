# This program is intended to run in the background and close any previous instance of itself when it starts.
# This lets the i2C screen show more complex information like scrolling displays, countdowns, etc. while the togglepin.py is able to continue its routine.
# This program can be started by the 'ScreenText' argument in togglepin.py, followed by further arguments in single quotation marks. (See togglepin.py for more info.)

#import os # Import 'os' module for Unix commands
import time
import subprocess
import os
import sys
import smbus
#nameofprogramtoclose = "ScreenText2.py"
import psutil

# To wrap text I  need the 'wrap' module
from textwrap import wrap

#LCD screen stuff
from RPLCD import CharLCD, cleared, cursor
from PCF8574 import PCF8574_GPIO
import Adafruit_LCD1602
import Adafruit_CharLCDb
#import Adafruit_LCD1602 as Adafruit
from Adafruit_LCD1602 import Adafruit_CharLCD
#Adafruit.KenFunction2()
PCF8574_address = 0x27 # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F # I2C address of the PCF8574A chip.
try:
	mcp = PCF8574_GPIO(PCF8574_address)
except:
	try:
		mcp = PCF8574_GPIO(PCF8574A_address)
	except:
		print ("\033[1;31mI2C address error! Is the screen connected?\033[0m")
		exit(1)

# Adafruit_CharLCD.py stuff
#import Adafruit_CharLCD
#print ("I did it! I imported Adafruit_CharLCD.")

#Adafruit_LCD1602.KenFunction() # Testing the import of Adafruit_LCD1602.py by running the KenFunction() I added to it.
#bob = Adafruit_CharLCD()
#bob.KenFunction2()

#Create LCD, passing in MCP GPIO adapter.
bus = smbus.SMBus(1)
addr = 0x27
lcd = Adafruit_CharLCD (pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)
#lcd.KenFunction2()
mcp.output(3,1) # Turn on LCD backlight
lcd.begin(16,2) # Set number of LCD lines and columns
lcd.setCursor(0,0) # Set cursor position
#bus.write_byte(1, 0b1100)
sixteenerlist = []

# Custom characters
#lcd.lcd_load_custom_chars()
#import adafruit_character_lcd.character_lcd_i2c as character_lcd
same = (0b00000, 0b11111, 0b11111, 0b00000, 0b00000, 0b11111, 0b11111, 0b00000,) # Define custom character

#This is supposed to set up an equals character in the memory of the LCD screen
#lcd.create_char(0, same)

#lcd.create_char(0, same) # This should run the create_char function in Adafruit_LCD1602.py.
#Adafruit_CharLCD.__init__(self)
#Adafruit.clear()
#Adafruit.write4bits(0, same, char_mode=False)

#lcd.write8(pattern[1], char_mode=True)
#lcd.createChar(0, same)

#create_char(0, same)
#lcd.custom_char(0, same)
#Adafruit_CharLCD.createChar(0,same)
#CustomChars.CreateChar(1,[2,3,2,2,14,30,12,0])

# Temp: Reveal all the characters
#characterincrement = 0
#while characterincrement < 256:
#	print ("Character " + str(characterincrement) + " is " + unichr(characterincrement) + ".")
#	characterincrement = characterincrement + 1

#def write8 (self, value, char_mode=False):
	# Write 8-bit value in character or data mode. Value should be an int value from 0-255, and char_mode is True if character data or False if non-character data (default).
	# Taken from Adafruit_CharLCD.py
	#lcd._delay_microseconds(1000) # One millisecond delay to prevent writing too quickly.
	#lcd._gpio.output(lcd._rs, char_mode) # Set character / data bit.
	# Write upper 4 bits
	#lcd._gpio.output_pins({ lcd._d4: ((value >> 4) & 1) > 0,
	#			lcd._d5: ((value >> 5) & 1) > 0,
	#			lcd._d6: ((value >> 6) & 1) > 0,
	#			lcd._d7: ((value >> 7) & 1) > 0 })
	#lcd._pulse_enable()
	# Write lower 4 bits
	#lcd._gpio.output_pins({ lcd._d4: (value        & 1) > 0,
	#			lcd._d5: ((value >> 1) & 1) > 0,
	#			lcd._d6: ((value >> 2) & 1) > 0,
	#			lcd._d7: ((value >> 3) & 1) > 0 })
#	self._pulse_enable()

# Will this create a custom character?
#Adafruit_CharLCD.create_char(Adafruit_CharLCD, 1, same)

def StdoutThis (stdoutstring):
	#sys.stdout.write(stdoutstring)
	#sys.stdout.flush()
	pass
def StaticMessage(fullmessage):
	lcd.message(fullmessage)
	StdoutThis ("\033[1;33m" + fullmessage + "\033[0m")
def ScrollingMessage(split_strings):
	textincrement = 0
	#if sixteenerlist == []:
	#	sixteenerlist = [" " * OLEDscreenX]
	spinnerincrement = 0
	spinnerlist = ["+", "X", "+", "X"]
	if OLEDLinesAvailableAtOnce == 2:
		#print ("2 lines are available at once, will add odd spaces to list if needed.")
		#print ("Length of sixteener list is " + str(len(sixteenerlist)) + ".")
		if (len(sixteenerlist) % OLEDscreenY) == 0:
			#print ("That's an even number! No need to add anything.")
			pass
		else:
			#print ("That's an odd number! Will need to add more sets of spaces to the list.")
			sixteenerlist.append(" " * OLEDscreenX) # Add another sixteen-character item to the sixteener list, of sixteen spaces
			#print ("Sixteener list now says '" + str(sixteenerlist)  + "'.")
	while True:
		textincrement = textincrement + 1
		spinnerincrement = spinnerincrement + 1
		if textincrement > (len(sixteenerlist)):
			textincrement = 1
		if spinnerincrement > 3:
			spinnerincrement = 0
		lcd.setCursor(0,0) # Set cursor position back again
		scrollingmessage = sixteenerlist[textincrement-1]
		spacesneeded = 0
		if len(scrollingmessage) < 16:
			spacesneeded = (16 - len(scrollingmessage))
			#print (str(spacesneeded) + " spaces needed.")
		scrollingmessage = scrollingmessage + " " * spacesneeded
		spinnerform = spinnerlist[spinnerincrement-1]
		if MessageHasALoadingBar == True:
			#loadingbarmessage = "!!!!!!!" + spinnerform + "!!!!!!!!"
			loadingbarmessage = str(loadingbarstart) + "/" + str(loadingbartimecode)
			secondssincestart = (gettimecodenow() - loadingbarstart)
			lengthoftimer = (loadingbartimecode - gettimecodenow())
			percentage = (((100*secondssincestart) / loadingbarrawtime))
			if percentage > 100:
				percentage = 100
			sixteenth = ((OLEDscreenX * secondssincestart)/ loadingbarrawtime)
			if sixteenth > OLEDscreenX:
				sixteenth = OLEDscreenX
			#loadingbarmessage = (str(secondssincestart) + "|" + str(loadingbarrawtime) + " = " + str(sixteenth) + "|16")
			loadingbarmessage = "-" * sixteenth
			if sixteenth == OLEDscreenX:
				loadingbarmessage = "------DONE------"
			lcd.message(scrollingmessage + "\n" + loadingbarmessage)
			#print ("\033[1;33m" + scrollingmessage + "\n" + loadingbarmessage + "\033[0m")
			time.sleep(1.5)
		if MessageHasALoadingBar == False:
			scrollingmessage2 = sixteenerlist[textincrement]
			spacesneeded2 = 0
			if len(scrollingmessage2) < 16:
				spacesneeded2 = (16 - len(scrollingmessage2))
			scrollingmessage2 = scrollingmessage2 + " " * spacesneeded2
			lcd.message(scrollingmessage + "\n" + scrollingmessage2)
			textincrement = textincrement + 1
			time.sleep(3)
def appendsixteener(sixteener):
	sixteenerlist.append(sixteener)
	if len(item) <= OLEDscreenX:
		sixteener = item
	#print ("Sixteener list now says '" + str(sixteenerlist) + "'.")
	return(sixteener,sixteenerlist)

def gettimecodenow():
	# Get timecode of now. (Hours x 3600 plus minutes x 60 plus seconds.)
	timehint = int(time.strftime("%H", time.localtime()))
	timemint = int(time.strftime("%M", time.localtime()))
	timesint = int(time.strftime("%S", time.localtime()))
	tcint = (timehint * 3600) + (timemint * 60) + timesint
	#print ("Timecode now is " + str(tcint) + ".")
	timecoderesult = tcint
	#print ("Time code result result is " + str(timecoderesult) + ".")
	return timecoderesult

print ("\033[0;32mWelcome to ScreenText2. This program was created by Ken Dunlop to show messages on the Raspberry Pi's LCD screen.")
print ("It automatically closes previous iterations of itself as it starts.")
print ("Append arguments after the filename in the command prompt to add a message to send to the screen. (E.g.: python ScreenText2.py 'Testing for 30 seconds until TimeCodeNow30 LoadingBar30')")
print ("This program is intended to be run in the background using 'nohup python ScreenText2.py &'. It can then show complex messages on the LCD screen while togglepin.py continues.")
print ("See togglepin.py for more on using ScreenText commands in that program.")
print ("'LoadingBarX', where 'X' is a number of seconds, is a keyword that will make the screen show a loading bar in its lower line.")
print ("'TimeCodeNowX', where 'X' is a number of seconds, will make the screen show the time now plus the given number of seconds.")
print ("Note that ScreenText2.py will turn any underscores ('_') it's given into spaces.")
print ("If you need to quit this program, use Ctrl + C.\033[0m")

OLEDscreenX = 16
OLEDscreenY = 2
PIDforthisprogram = os.getpid()
print ("PID found for this program is " + str(PIDforthisprogram) + ".")
#print ("Screen is set to " + str(OLEDscreenX) + "x" + str(OLEDscreenY) + ".")
OLEDLinesStillAvailable = OLEDscreenY
OLEDLinesAvailableAtOnce = OLEDscreenY
MessageHasALoadingBar = False

#pythonProcess = subprocess.check_output("ps -ef | grep .py", shell=True).decode()
pythonProcess = subprocess.check_output("ps aux", shell=True).decode()
pythonProcess = pythonProcess.split("\n")
increment = 0
loadingbartimecode = 0
listofPIDstokill = ""
listofPIDtimes = ""
for process in pythonProcess:
	if increment < (len(pythonProcess)-1):
		#print("Process " + str(increment) + " says '" + process + "'.")
		stringsplit = process.split()
		#print (stringsplit)
		increment = increment + 1
		PID = (stringsplit[1])
		timecode = (stringsplit[8])
		#print "PID is " + PID
		programtofind = "ScreenText2.py"
		result = process.find(programtofind)
		if (process.find(programtofind) != -1) and (process.find('python') != -1):
			#print ("This line has " + programtofind  + " and python in it! Adding to list.")
			#print ("Stringsplit is '" + str(stringsplit) + "'.")
			listofPIDstokill = listofPIDstokill + str(PID) + " "
			listofPIDtimes = listofPIDtimes + str(timecode) + " "
#print (pythonProcess)
#print ("List of PIDs to kill is '" + listofPIDstokill + "', that's " + str(len(listofPIDstokill.split())) + " items.")
#print ("List of PID times is '" + listofPIDtimes + "', that's " + str(len(listofPIDtimes.split())) + " items.")
splitlist = listofPIDstokill.split()
splitPIDtimes = listofPIDtimes.split()
#print ("Split list says '" + str(splitlist) + "', that's " + str(len(splitlist)) + " items.")
increment = 0
itemstotal = len(splitlist)
loadingbarrawtime = 0
highesttimecodefound = 0
for item in splitlist:
	itemshouldbekilled = 0
	timeforitem = (splitPIDtimes[increment])
	increment = increment + 1
	#print ("Item " + str(increment) + " is '" + item + "', '" + timeforitem + "'.")
	colonisfound = timeforitem.find(":")
	#print ("Colon is found: " + str(colonisfound) + ".")
	#if colonisfound > -1:
	#	print ("Colon found at position " + str(colonisfound) + ".")
	#	colonlist = timeforitem.split(":")
	#	print ("Colon list says '" + str(colonlist) + "'.")
	#	int1 = int(colonlist[0])
	#	int2 = int(colonlist[1])
	#	print ("Integers are " + str(int1) + ", " + str(int2) + ".")
	#	timecode = (int1 * 60) + int2
	#	print ("Timecode is therefore " + str(timecode) + ".")
	#	if timecode > highesttimecodefound:
	#		highesttimecodefound = timecode
	#		print ("New highest timecode found is " + str(highesttimecodefound) + ".")
	#else:
	#	itemshouldbekilled = 1
	if int(item) == PIDforthisprogram:
		print ("This (" + item + ") is the PID for this program! (" + str(PIDforthisprogram) + ") Should not kill.")
		itemshouldbekilled = 0
	else:
		itemshouldbekilled = 1
		#print ("This PID (" + item + ") should be killed.")
	if itemshouldbekilled == 1:
		os.system("kill " + item)
	#if itemshouldbekilled == 1:
	#	print ("This item ('" + item  + "') should be killed.")
	#print ("Item " + str(increment) + "/" + str(itemstotal) + " is '" + item  + "'.")
	#if increment <= itemstotal:
		#print ("\033[1mKilling old ScreenText2 process PID " + item + ".\033[0m")
		#print ("\033[1mWould kill this PID (" + item + ") normally.\033[0m")
		#os.system("kill " + item)
		#pass
	#else:
		#print ("I think that's this program.")
		#pass

# Go through each argument the ScreenText2 program is given and parse it
#print ("Arguments list reads '" + str(sys.argv) + "'. (" + str(len(sys.argv)) + " items.)")
increment = 0
loadinbbarstart = 0
#Get all arguments dealt with beforehand to deal with underscores
argumentsparsed = ""
argumentsparsedlist = []
for item in sys.argv:
	increment = increment + 1
	argument = sys.argv[increment-1]
	argument = argument.replace("_", " ")
	print ("Argument " + str(increment-1) + " says '" + argument + "'.")
	argumentaslist = argument.split()
	print ("Argument as list says '" + str(argumentaslist) + "'.")
	increment2 = 0
	increment3 = 0
	minilist = []
	for item in argumentaslist:
		increment3 = increment3 + 1
		aalfragment = argumentaslist[increment3 -1]
		#print ("AAL fragment says '" + aalfragment  + "'.")
		increment4 = 0
		aalsubfragmentslist = wrap (aalfragment, OLEDscreenX)
		#print ("aalsubfragmentslist says '" + str(aalsubfragmentslist)  + "'.")
		for item in aalsubfragmentslist:
			increment4 = increment4 + 1
			minilist.append(item)
		#print ("Minilist now says '" + str(minilist) + "'.")
	if increment > 1:
		#minilist = wrap(argument, OLEDscreenX)
		#print ("Mini list says '" + str(minilist)  + "'.")
		for item in minilist:
			increment2 = increment2 + 1
			minilistitem = minilist[increment2 -1]
			#print ("Minilistitem is '" + minilistitem  + "'.")
			argumentsparsed = argumentsparsed + minilistitem
			if increment2 < len(minilist):
				argumentsparsed = argumentsparsed + " "
			argumentsparsedlist.append(minilistitem)

print ("Total arguments parsed are '" + argumentsparsed  + "'.")
print ("Arguments parsed list says '" + str(argumentsparsedlist) + "'.")
increment = 0
#for item in sys.argv:
for item in argumentsparsedlist:
	increment = increment + 1
	argument = argumentsparsedlist[increment-1]
	sixteenerlist = []
	numberofliteralshandled = 0
	messagefitsthescreen = 1
	#print ("Examining item " + str(increment) + " in arguments list, '" + argument + "'.")
	if increment > 0:
		#print ("'" + argument + "' isn't just the filename.")
		argumentaslist = argument.split()
		#print ("As a list, it's '" + str(argumentaslist) + "'.")
		incrementB = 0
		lengthofarglist = len(argumentaslist)
		collatedstringsofar = ""
		messageoneline = ""
		messagefitsthescreen = 1
		lengthonline = 0
		numberoflines = 1
		sixteener = ""
		#for item in argumentaslist:
		for item in argumentsparsedlist:
			incrementB = incrementB + 1
			#print ("Part " + str(incrementB) + "/" + str(len(argumentsparsedlist)) + " says '" + item + "'.")
			itemisaliteral = 1
			if item.lower() == "newline":
				itemisaliteral = 0
				spacesneeded = OLEDscreenX - len(sixteener)
				print ("NewLine found: It'd take " + str(spacesneeded) + " spaces to finish this line.")
				sixteener = sixteener + " " * spacesneeded
			if "loadingbar" in item.lower():
				print ("This item contains 'loadingbar'.")
				messagefitsthescreen = 0
				MessageHasALoadingBar = True
				OLEDLinesAvailableAtOnce = 1
				itemisaliteral = 0
				timecodeinput = item.lower().replace("loadingbar", "")
				b = unicode(timecodeinput, "utf-8")
				if b.isnumeric() is False:
					print("\033[131m'" + timecodeinput + "' is not numeric, will treat as zero.\033[0m")
					timecodeinput = 0
				if b.isnumeric() is True or b.isnumeric() is False:
					print (str(timecodeinput) + " is numeric.")
					loadingbartimecode = int(timecodeinput) + gettimecodenow()
					loadingbarrawtime = int(timecodeinput)
					if loadingbarrawtime == 0:
						loadingbarrawtime = 1
					#print ("Set loadingbartimecode to " + str(loadingbartimecode) + ".")
				loadingbarstart = gettimecodenow()
				print ("Loading bar start time registered as " + str(loadingbarstart) + ".")
			if "timecodenow" in item.lower():
				messagefitsthescreen = 0
				print ("This item contains 'timecodenow'.")
				timecoderesult = gettimecodenow()
				timecodeinput = item.lower().replace("timecodenow", "")
				print ("Time code input now says '" + timecodeinput + "'.")
				b = unicode(timecodeinput, "utf-8")
				if b.isnumeric() is False:
					print ("\033[1;31m'" + timecodeinput + "' is not numeric, will treat as zero.\033[0m")
					timecodeinput = 0
				if b.isnumeric() is True or b.isnumeric() is False:
					print (str(timecodeinput) + " is numeric.")
					timecodeneeded = int(timecodeinput) + int(timecoderesult)
					print ("Time code needed is " + str(timecodeneeded) + ".")
					tcnhours = timecodeneeded / 3600
					tcnminutes = (timecodeneeded / 60) - (tcnhours * 60)
					tcnseconds = timecodeneeded - ((tcnhours * 3600) - (tcnminutes * 60))
					tcnhoursstr = str(tcnhours)
					tcnminutesstr = str(tcnminutes)
					tcnsecondsstr = str(tcnseconds)
					if len(tcnminutesstr) < 2:
						tcnminutesstr = "0" + tcnminutesstr
					if len(tcnsecondsstr) < 2:
						tcnsecondsstr = "0" + tcnsecondsstr
					tcnhms = tcnhoursstr + ":" + tcnminutesstr
					print ("Time code needed HMS is " + tcnhoursstr + ":" + tcnminutesstr)
					item = tcnhms
			lengthofitem = 0
			if itemisaliteral == 0:
				item = ""
			if itemisaliteral == 1:
				lengthofitem = len(item)
				numberofliteralshandled = numberofliteralshandled + 1
			lengthofsixteener = len(sixteener)
			if itemisaliteral == 1:
				if numberofliteralshandled > 1 and (incrementB -1) < len(argumentsparsedlist):
					sixteener = sixteener + " "
					lengthofsixteener = len(sixteener)
				if (lengthofsixteener + lengthofitem) <= OLEDscreenX:
					sixteener = sixteener + item
					#sixteener = sixteener + " " + item
				else:
					appendsixteener(sixteener)
					#sixteenerlist.append(sixteener)
					if len(item) <= OLEDscreenX:
						sixteener = item
					#print ("Sixteener list now says '" + str(sixteenerlist) + "'.")
			#print ("Sixteener says '" + sixteener + "'. (Length " + str(len(sixteener)) + ").")
			#print ("This item is " + str(lengthofitem) + " characters long.")
			lengthofargsofar = len(collatedstringsofar)
			#print ("Length of argument so far is " + str(lengthofargsofar) + ".")
			totallength = lengthofargsofar + lengthofitem
			lengthonline = lengthonline + lengthofitem
			#print ("Total length is " + str(totallength) + ".")
			#print ("Length on line is " + str(lengthonline) + ".")
			if lengthofitem > OLEDscreenX:
				#messagefitsthescreen = 0
				print ("That doesn't fit the screen! (" + str(OLEDscreenX) + ").")
			if lengthonline > OLEDscreenX and lengthofitem <= OLEDscreenX:
				#print ("Projected line length is more than " + str(OLEDscreenX) + "! Adding return.")
				collatedstringsofar = collatedstringsofar + "\r\n"
				numberoflines = numberoflines + 1
				lengthonline = lengthofitem
				OLEDLinesStillAvailable = OLEDLinesStillAvailable - 1
				#print (str(OLEDLinesStillAvailable) + " line still available to be used.")
			collatedstringsofar = collatedstringsofar + item + " "
			messageoneline = messageoneline + item
			if incrementB < lengthofarglist:
				#collatedstringsofar = collatedstringsofar + " "
				#if len(sixteener) < OLEDscreenX:
				#	sixteener = sixteener + " "
				messageoneline = messageoneline + " "
				totallength = totallength + 1
				lengthonline = lengthonline + 1
			#print ("String so far is '" + collatedstringsofar  + "'.")
		if sixteener == "":
			print ("Sixteener is empty now.")
			pass
		else:
			#print ("There's still text left in the sixteener ('" + sixteener + "').")
			appendsixteener(sixteener)
			#sixteenerlist.append(sixteener)
			#print ("Sixteenerlist now says '" + str(sixteenerlist) + "'.")
			sixteener = ""
		collatedstringsofar = ""
		increment = 0
		for item in sixteenerlist:
			increment = increment + 1
			collatedstringsofar = collatedstringsofar + item
			if increment > 1:
				collatedstringsofar = collatedstringsofar + " "
		x = collatedstringsofar.replace(" \r\n", "\r\n")
		#x = x.replace(" ", "_")
		x = x.replace("\r", "")
		#print ("Collated string now says:\r\n '" + x + "'.")
		#print ("Sixteener says: " + sixteener  + ".")
		if len(sixteenerlist) > OLEDscreenY:
			messagefitsthescreen = 0
		#if messagefitsthescreen == 1:
		if sixteenerlist == []:
			print ("Sixteenerlist is blank, setting to " + str(OLEDscreenX) + " spaces.")
			sixteenerlist = [" " * OLEDscreenX]
			messagefitsthescreen = 1
		if 1 == 2:
			print ("This message fits the screen (" + str(OLEDscreenX) + "x" + str(OLEDscreenY) + ").")
			print ("Displaying as static message.")
			StaticMessage(x)
		else:
			print ("Will display message in " + str(OLEDscreenX) + "-character pieces.")
			print ("Sixteener list reads '" + str(sixteenerlist) + "'.")
			split_strings = []
			n = OLEDscreenX
			for index in range (0, len(messageoneline), n):
				split_strings.append(messageoneline[index : index + n])
			#print (split_strings)
			ScrollingMessage(split_strings)
		#lengthofcollatedstring = len(collatedstringsofar)
		#print ("That's " + str(lengthofcollatedstring) + " characters.")

if sixteenerlist != []:
	print ("Will sleep for 99999 seconds. (Use Ctrl + C to quit.)")
	time.sleep(99999)
