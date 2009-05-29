#from __future__ import nested_scopes
''' mainmenu.py
	Author:			Chad Rempp
	Date:			2009/05/15
	Purpose:		Sets up and manages all the main menus and related functions.
	Usage:			None
	References:		None
	Restrictions:	None
	License:		TBD
	Notes:			This is a HUGE mess! Clean this up.
'''

# Python imports
import os

# PSG imports
from direct.gui.OnscreenImage import OnscreenImage
from gui.keys import Keys
from gui.controls import *
from gui.widgets import *
from Settings import GameSettings
import Event

x_res = 640
y_res = 480

def tpc(coord,y=False): # To Panda Coordinate
	''' Helper function to convert from Panda coord system to interger screen
		coord system.'''
	
	ratio   = x_res/y_res # Ratio for aspect2d
	shifter = x_res/2
	if y:
		scaler = -1/shifter
	else:
		scaler = ratio/shifter
	return ((coord - shifter) * scaler)

class MainScreen:
	''' Controls the main menu screen. This is not the actual main menu, this
		object controls movement between the main menu forms'''
	
	# Size of the menu forms
	menusize = Vec2(420,300)
	menupad  = Vec4(20,20,30,0) # (l,r,t,b)
	
	_currentmenu = None
	
	# Variables to be used in the menus
	mapList = []
	playerList = []
	
	def __init__(self, gameclient, clientconnection):
		''' Create the menu forms and draw the background image.
			game (Game): the game created in the GameClient that the menus
						will finish setting up
			clientconnection (ClientConnection): the connection the GameClient
						made that the menus will use to connect to a server.'''
						
		self.menupos    = Vec2((x_res-self.menusize[0])/2,(y_res-self.menusize[1])/2+40)
		self.mapList    = []
		self.playerList = []
		self.gameList   = []
		self.gameclient = gameclient
		self.clientconnection = clientconnection
		
		self.buildOptionLists()
		
		# Background image
		self.background = OnscreenImage(image = 'data/images/menubackground.png',
		  					pos=(0.6,0,-1.1333),
		  					scale=(1.6,1,2.1333),
		  					parent=render2d)
		
		# Create menu forms
		self.main = MainForm(self)
		gui.add(self.main)
		
		self.single = SingleForm(self)
		gui.add(self.single)
		self.single.toggle()
		
		self.multi = MultiForm(self)
		gui.add(self.multi)
		self.multi.toggle()
		
		# Setup menu state
		self._currentmenu  = self.main
		
	def showMain(self, button, key, mouse):
		self._currentmenu.toggle()
		self._currentmenu = self.main
		self.main.toggle()
	
	def showSingle(self, button, key, mouse):
		self._currentmenu.toggle()
		self._currentmenu = self.single
		self.single.toggle()
		
	def showMulti(self, button, key, mouse):
		self._currentmenu.toggle()
		self._currentmenu = self.multi
		self.multi.toggle()
	
	def showPlayer(self, button, key, mouse):
		print('player')
	
	def showOptions(self, button, key, mouse):
		print('options')
	
	def showCredits(self, button, key, mouse):
		print('credits')
	
	def exit(self, button, key, mouse):
		print('exit')
		Event.Dispatcher().broadcast(Event.Event('E_ExitProgram',src=self))
		
	def buildOptionLists(self):
		''' This scans the maps directory and creates the list of available
			maps.'''
		
		for m in self.gameclient.maps:
			self.mapList.append(m.name)
		self.playerList = ['player 1','player 2','player 3','player 4','player 5']
		self.gameList = []
		
	def startGame(self, game):
		print('Start game:')
		self.background.destroy()
		self.main.hide()
		self.single.hide()
		self.multi.hide()
		del(self.main)
		del(self.single)
		del(self.multi)
		self.gameclient.startGame(game)
		

class MainForm(Form):
	''' The main game menu'''
	def __init__(self, parentmenu):
		Form.__init__(self,'Main Menu',pos=parentmenu.menupos, size=parentmenu.menusize)
		self.parentmenu = parentmenu
		# Dont show close or sizer button and disable drag.
		self.x.node.hide()
		self.sizer.node.hide()
		self.things[0].onClick=lambda b,k,m : None
		
		self.add(Button('Single Player',pos=Vec2(150,40), size=(80,20), point=16, onClick=self.parentmenu.showSingle));
		self.add(Button('Multi Player',pos=Vec2(150,80), size=(80,20), point=16,onClick=self.parentmenu.showMulti));
		self.add(Button('Player Setup',pos=Vec2(150,120), size=(80,20), point=16,onClick=self.parentmenu.showPlayer));
		self.add(Button('Options',pos=Vec2(150,160), size=(80,20), point=16,onClick=self.parentmenu.showOptions));
		self.add(Button('Credits',pos=Vec2(150,200), size=(80,20), point=16,onClick=self.parentmenu.showCredits));
		self.add(Button('Exit',pos=Vec2(150,240), size=(80,20), point=16,onClick=self.parentmenu.exit));
		
class SingleForm(Form):
	''' Single player game menu.'''
	def __init__(self, parentmenu):
		Form.__init__(self,'Main Menu',pos=parentmenu.menupos, size=parentmenu.menusize)
		self.parentmenu = parentmenu
		
		self.x.node.hide()
		self.sizer.node.hide()
		self.things[0].onClick=lambda b,k,m : None
		
		# Setup defaults
		if len(self.parentmenu.mapList) > 0:
			defaultMap = self.parentmenu.mapList[0]
		else:
			defaultMap = ''
		if len(self.parentmenu.playerList) > 0:
			defaultPlayer = self.parentmenu.playerList[0]
		else:
			defaultPlayer = ''
		
		# Draw widgets from bottom to top (this is for dropdown menu sort order)
		self.add(Button('Main Menu',pos=Vec2(self.parentmenu.menupad[0],self.parentmenu.menusize[1]-self.parentmenu.menupad[3]-20), onClick=self.parentmenu.showMain))
		self.add(Button('Start Game',pos=Vec2(self.parentmenu.menusize[0]-self.parentmenu.menupad[1]-50,self.parentmenu.menusize[1]-self.parentmenu.menupad[3]-20), onClick=self.parentmenu.startGame))
		
		r = range(1,5)
		r.reverse()
		for i in r:
			self.add(Lable('Player ' + str(i), pos=Vec2(self.parentmenu.menupad[0],self.parentmenu.menupad[2]+30+(30*i))))
			self.add(DropDown(self.parentmenu.playerList, defaultPlayer, pos=Vec2(self.parentmenu.menupad[0]+60,self.parentmenu.menupad[2]+30+(30*i))))
			self.add(DropDown(['Human','Computer'], 'Computer', pos=Vec2(self.parentmenu.menupad[0]+220,self.parentmenu.menupad[2]+30+(30*i))))
		
		self.add(Lable('Map',pos=Vec2(self.parentmenu.menupad[0],self.parentmenu.menupad[2])))
		self.add(DropDown(self.parentmenu.mapList, defaultMap, pos=Vec2(self.parentmenu.menupad[0]+50,self.parentmenu.menupad[2]), size=Vec2(280,20)))

class MultiForm(Form):
	''' Multi player game menu.'''
	def __init__(self, parentmenu):
		Form.__init__(self,'Multiplayer Game',pos=parentmenu.menupos, size=parentmenu.menusize)
		self.parentmenu = parentmenu
		
		self.x.node.hide()
		self.sizer.node.hide()
		self.things[0].onClick=lambda b,k,m : None
		
		server   = self.parentmenu.clientconnection.getAddress()
		username = 'chad'
		password = 'password1'
		port     = self.parentmenu.clientconnection.getPort()
		
		self.add(Lable('Username:',\
				pos=Vec2(self.parentmenu.menupad[0],\
						 self.parentmenu.menupad[2])))
		self.i_username = Input(username,\
				pos=Vec2(self.parentmenu.menupad[0]+60,\
						 self.parentmenu.menupad[2]))
		self.add(self.i_username)
		self.add(Lable('Password:',pos=Vec2(self.parentmenu.menupad[0]+200,self.parentmenu.menupad[2])))
		self.i_password = Input(password, pos=Vec2(self.parentmenu.menupad[0]+260,self.parentmenu.menupad[2]))
		self.add(self.i_password)
		self.add(Lable('Server:',pos=Vec2(self.parentmenu.menupad[0],self.parentmenu.menupad[2]+25)))
		self.i_server = Input(server, pos=Vec2(self.parentmenu.menupad[0]+60,self.parentmenu.menupad[2]+25), size=Vec2(130,20))
		self.add(self.i_server)
		self.add(Lable('Port:',pos=Vec2(self.parentmenu.menupad[0]+200,self.parentmenu.menupad[2]+25)))
		self.i_port = Input(port, pos=Vec2(self.parentmenu.menupad[0]+260,self.parentmenu.menupad[2]+25), size=Vec2(130,20))
		self.add(self.i_port)
		self.add(Button('Create Game',pos=Vec2(self.parentmenu.menupad[0],self.parentmenu.menupad[2]+50), onClick=self.createGame))
		self.add(Button('Connect',pos=Vec2(self.parentmenu.menusize[0]-90,self.parentmenu.menupad[2]+50), onClick=self.connect))
		self.add(Lable('Games:',pos=Vec2(self.parentmenu.menupad[0],self.parentmenu.menupad[2]+70)))
		self.l_games = SelectList([], pos=Vec2(self.parentmenu.menupad[0],self.parentmenu.menupad[2]+90), size=Vec2(200,200))
		self.add(self.l_games)
		
		self.add(Button('Main Menu',pos=Vec2(self.parentmenu.menupad[0],self.parentmenu.menusize[1]-self.parentmenu.menupad[3]-20), onClick=self.parentmenu.showMain))
		self.add(Button('Join',pos=Vec2(self.parentmenu.menusize[0]-self.parentmenu.menupad[1]-50,self.parentmenu.menusize[1]-self.parentmenu.menupad[3]-20), onClick=self.joinGame))
	
	def updateGameList(self):
		''' Request game list from the server and update the local list upon
			response.'''
		print("updating game list now")
		def response(games):
			self.parentmenu.gameList = games
			self.l_games.clear()
			for g in games:
				self.l_games.addOption(g['String'])
		self.parentmenu.clientconnection.getGameList(response)
		
	def createGame(self, button, key, mouse):
		print('create game')
		createGameDialog = None
		
		def createResponse(resp):
			print('Game created, updating list')
			if (resp):
				createGameDialog.l_status.setText('Game created.')
				# Make ok button exit dialog
				createGameDialog.setOkFunc(onCancel)
				self.updateGameList()
			else:
				print('Game was not created')
				
		def onOk(button, key, mouse):
			print('Ok')
			name = createGameDialog.i_name.getText()
			map  = createGameDialog.d_map.getOption()
			maxplayers = createGameDialog.i_maxplayers.getText()
			self.parentmenu.clientconnection.newGame(name, map, maxplayers, createResponse)
			
		def onCancel(button, key, mouse):
			print('Cancel')
			createGameDialog.toggle()
			gui.remove(createGameDialog)
		
		if self.parentmenu.clientconnection.isConnected():
			createGameDialog = CreateGameDialog(self.parentmenu, okFunc=onOk, cancelFunc=onCancel)
			gui.add(createGameDialog)
		else:
			createGameDialog = Alert('Oops!', text='Can not create game, we are not connected', pos=Vec2(250,20))
			gui.add(createGameDialog)
		
	def connect(self, button, key, mouse):
		''' Connect to a server using the info filled in on this form.'''
		connectDialog = None
		connected     = False
		authenticated = False
		
		
		def connectionResponse(resp):
			if resp:
				connectDialog.setText('Connected to the server, authenticating...')
				self.parentmenu.clientconnection.authenticate(username, password, authResponse)
			else:
				connectDialog.setText('Connection failed.')
				
		def authResponse(resp):
			if resp:
				connectDialog.setText('Authenticated. You are connected.')
				self.updateGameList()
			else:
				connectDialog.setText('Authentication failed.')
				
		def cancel():
			print('cancel')
			self.parentmenu.clientconnection.disconnect()
			gui.remove(connectDialog)
			del(connectDialog)
			
		print('connecting...')
		
		# Get the values from the form
		server   = self.i_server.getText()
		username = self.i_username.getText()
		password = self.i_password.getText()
		port     = self.i_port.getText()
		
		# If everything is ok attempt to connect and use connectDialog to show the status
		if (server!='' and username!='' and password!='' and port!=''):
			self.parentmenu.clientconnection.setAddress(server)
			connectDialog = Dialog('Connecting', text='connecting to server %s'%server, pos=Vec2(250,20))
			gui.add(connectDialog)
			self.parentmenu.clientconnection.connect(server, int(port), 3000, connectionResponse)
		else:
			print('You did not fill in the all the values')
			
	def joinGame(self, button=None, key=None, mouse=None):
		
		def joinResponse(resp):
			if resp < 2:
				print("Couldn't join game")
			else:
				self.parentmenu.startGame(game)
				
		# Get the selected game
		if len(self.l_games.selected) > 0:
			selectedGame = self.l_games.selected[0]
		else:
			print("No game selected") # Make this an Alert
			return
		
		# Find the selected game in the gameList and try to join it
		for g in self.parentmenu.gameList:
			if g['String'] == selectedGame:
				# Check if we have the map for the game
				print("mapList = %s"%str(self.parentmenu.mapList))
				print("Map = %s"%g['Map'])
				if g['Map'] not in self.parentmenu.mapList:
					print('We dont have the map %s, trying to download it'%g['Map'])
					# TODO - Finish this!
					return
				game = g
				self.parentmenu.clientconnection.joinGame(g['Id'], joinResponse)
		
class CreateGameDialog(Dialog):
	''' Create server dialog.'''
	def __init__(self, parentmenu, okFunc=None, cancelFunc=None):
		Dialog.__init__(self, title='Create Game', text='', pos=Vec2(250,20), size=Vec2(270,200), okFunc=okFunc, cancelFunc=cancelFunc)
		
		self.parentmenu = parentmenu
		
		self.l_status = Lable('', pos=Vec2(10,80))
		self.add(self.l_status)
		self.add(Lable('Max Players:',pos=Vec2(10,60)))
		self.i_maxplayers = Input('3', pos=Vec2(90,60), size=Vec2(20,20))
		self.add(self.i_maxplayers)
		self.add(Lable('Map',pos=Vec2(10,40)))
		self.d_map = DropDown(self.parentmenu.mapList, self.parentmenu.mapList[0], pos=Vec2(90,40), size=Vec2(100,20))
		self.add(self.d_map)
		self.add(Lable('Game Name:',pos=Vec2(10,20)))
		self.i_name = Input('New Game', pos=Vec2(90,20))
		self.add(self.i_name)
		
		
		
		
class DisplayForm(Form):
	''' Display settings menu.'''
	def __init__(self,  menu):
		Form.__init__(self,'Settings',pos=Vec2(250,200),size=Vec2(300,350))
		self.menu = menu
		
		# Dont show close or sizer button and disable drag.
		self.x.node.hide()
		self.sizer.node.hide()
		self.things[0].onClick=lambda b,k,m : None
			
		self.fullscreen = Check('Fullscreen',pos=Vec2(10,50))
		if GameSettings().getSetting('FULLSCREEN') == 'True':
			self.fullscreen.onClick(None, None, None)
		self.add(self.fullscreen);
		
		self.fpsmeter = Check('FPS Meter',pos=Vec2(10,75))
		if GameSettings().getSetting('SHOWFPS') == 'True':
			self.fpsmeter.onClick(None, None, None)
		self.add(self.fpsmeter);
		
		self.aaInput = Input(GameSettings().getSetting('ANTIALIAS'),pos=Vec2(10,100),size=Vec2(20,20))
		self.add(self.aaInput);
		self.add(Lable('AA (1,2,4,8,16)',pos=Vec2(40,100)))
		
		self.alphaInput = Input(GameSettings().getSetting('ALPHABITS'),pos=Vec2(10,125),size=Vec2(20,20))
		self.add(self.alphaInput);
		self.add(Lable('Alphabits (4,8,16,32)',pos=Vec2(40,125)))
		
		self.colorInput = Input(GameSettings().getSetting('COLORDEPTH'),pos=Vec2(10,150),size=Vec2(20,20))
		self.add(self.colorInput);
		self.add(Lable('Colordepth (4,8,16,32)',pos=Vec2(40,150)))
		
		self.bloom = Check('Bloom',pos=Vec2(10,175))
		if GameSettings().getSetting('USEBLOOM') == 'True':
			self.bloom.onClick(None, None, None)
		self.add(self.bloom);
		
		self.fog = Check('Fog',pos=Vec2(10,200))
		if GameSettings().getSetting('USEFOG') == 'True':
			self.fog.onClick(None, None, None)
		self.add(self.fog);
		
		self.add(Button('OK',pos=Vec2(40,280), onClick=self.ok))
		self.add(Button('Cancel',pos=Vec2(150,280), onClick=self.menu.showMainFromDisplay))
		
		# This needs to be done last so the dropdowns show over other widgets
		self.add(Lable('Resolution:',pos=Vec2(10,25)))
		options = ['640x480 (4:3)',
			'800x600 (4:3)',
			'1024x768 (4:3)', 
			'1280x960 (4:3)', 
			'1400x1050 (4:3)', 
			'1600x1200 (4:3)', 
			'1280x1024 (5:4)', 
			'1280x800 (8:5)', 
			'1440x900 (8:5)', 
			'1680x1050 (8:5)', 
			'1920x1200 (8:5)', 
			'854x480 (16:9)', 
			'1280x720 (16:9)', 
			'1920x1080 (16:9)']
		self.resolution = DropDown(options, GameSettings().getSetting('RESOLUTION'), pos=Vec2(75,25), size=Vec2(100,20))
		self.add(self.resolution)
		
	def ok(self,button,key,mouse):
		# save settings
		GameSettings().setSetting('RESOLUTION',  self.resolution.getOption())
		if self.fullscreen.value:
			GameSettings().setSetting('FULLSCREEN',  'True')
		else:
			GameSettings().setSetting('FULLSCREEN',  'False')
		if self.fpsmeter.value:
			GameSettings().setSetting('SHOWFPS',  'True')
		else:
			GameSettings().setSetting('SHOWFPS',  'False')
		GameSettings().setSetting('ANTIALIAS',  self.aaInput.getText())
		GameSettings().setSetting('ALPHABITS',  self.alphaInput.getText())
		GameSettings().setSetting('COLORDEPTH',  self.colorInput.getText())
		if self.bloom.value:
			GameSettings().setSetting('USEBLOOM',  'True')
		else:
			GameSettings().setSetting('USEBLOOM',  'False')
		if self.fog.value:
			GameSettings().setSetting('USEFOG',  'True')
		else:
			GameSettings().setSetting('USEFOG',  'False')
		GameSettings().saveSettings()
		self.menu.showMainFromDisplay()
		
class AudioForm(Form):
	def __init__(self, menu):
		Form.__init__(self,'AudioSettings',pos=Vec2(250,200),size=Vec2(300,300))
		self.menu = menu
		self.x.node.hide()
		self.sizer.node.hide()
		self.things[0].onClick=lambda b,k,m : None
		
		self.add(Lable('Nothing here yet. Click OK or Cancel to go',pos=Vec2(60,50)))
		self.add(Lable('back to the main menu',pos=Vec2(60,70)))
		self.add(Button('OK',pos=Vec2(40,280), onClick=self.menu.showMainFromLoad))
		self.add(Button('Cancel',pos=Vec2(150,280), onClick=self.menu.showMainFromLoad))

class CreditsForm(Form):
	def __init__(self, menu):
		Form.__init__(self,'Credits',pos=Vec2(250,200),size=Vec2(300,300))
		self.menu = menu
		self.x.node.hide()
		self.sizer.node.hide()
		self.things[0].onClick=lambda b,k,m : None
		
		self.add(Lable('Nothing here yet. Click OK or Cancel to go',pos=Vec2(60,50)))
		self.add(Lable('back to the main menu',pos=Vec2(60,70)))
		self.add(Button('OK',pos=Vec2(40,280), onClick=self.menu.showMainFromLoad))
		self.add(Button('Cancel',pos=Vec2(150,280), onClick=self.menu.showMainFromLoad))
