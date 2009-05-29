from pandac.PandaModules import Vec3
from Util import Singleton
import Event
import math

# EntityManager-----------------------------------------------------------------
class EntityManager():
	__metaclass__=Singleton
	_entities = []
	def __init__(self):
			pass
			
	def addEntity(self, entity):
		if not entity in self._entities:
			#print("EntityManager adding " + str(entity))
			self._entities.append(entity)
			Event.Dispatcher().broadcast(Event.Event('E_New_EntityRep', src=self, data=entity))
			
	def delEntity(self,  entity):
		'''TODO - Broadcast a del'''
		try:
			self._entities.remove(entity)
		except:
			pass
			
	def getFromTag(self, tag):
		for e in self._entities:
			if e.getTag() == tag:
				return e
		return None
		
	def getEntitiesWithin(self, pos, radius):
		entityList = []
		px = pos.getX()
		py = pos.getY()
		pz = pos.getZ()
		for e in self._entities:
			ex = e.getPos().getX()
			ey = e.getPos().getY()
			ez = e.getPos().getZ()
			d = math.sqrt((px-ex)**2 + (py-ey)**2 + (pz-ez)**2)
			if (d <= radius):
				entityList.append(e)
		return entityList

# Entity------------------------------------------------------------------------
class Entity:
	"""An abstract class that represents any logical entity in the game."""
	pos = Vec3()
	hpr = Vec3()
	type = ""
	owner = None
	tag  = ""
	representation = None
	
	def __init__(self,  pos=None,  hpr=None,  type="",  owner=None,  tag=""):
		if pos != None:
			self.pos = pos
		if hpr != None:
			self.hpr = hpr
		if type != "":
			self.type = type
		if owner != None:
			self.owner = owner
		if tag != "":
			self.tag = tag
			
	def setOwner(self, owner):
		self.owner = owner
		
	def getTag(self):
		return self.tag
		
	def getPos(self):
		return self.pos
		
	def getHpr(self):
		return self.hpr
		
	def __repr__(self):
		return "<Entity: " + self.tag + ", pos=" + str(self.pos) + ">"
		
# ShipEntity--------------------------------------------------------------------
class EntityShip(Entity):
	"""Represents ship logic"""
	type = "SHIP"
	moveRad   = 0
	attackRad = 0
	sensorRad = 0
	fuel      = 0
	cost      = 0
	weaponList  = []
	abilityList = []
	representation = None
	moved = False
	attacked = False
			
	def __init__(self,  pos=None,  hpr=None,  type="",  owner=None,  tag=""):
		Entity.__init__(self, pos, hpr, type, owner, tag)
		
	def move(self,  newPos):
		self.pos = newPos
		self.representation.move(self.pos)
		
class EntityLightCapture(EntityShip):
	type = "SHIP"
	moveRad   = 1200 /10
	attackRad = 300 /10
	sensorRad = 800 /10
	fuel      = 99
	cost      = 1000
	weaponList  = []
	abilityList = []
	
	def __init__(self,  pos=None,  hpr=None,  type="",  owner=None,  tag=""):
		EntityShip.__init__(self, pos, hpr, type, owner, tag)
	
class EntityHeavyCapture(EntityShip):
	type = "SHIP"
	moveRad   = 1200 /10
	attackRad = 300 /10
	sensorRad = 800 /10
	fuel      = 70
	cost      = 3000
	weaponList  = []
	abilityList = []
	
	def __init__(self,  pos=None,  hpr=None,  type="",  owner=None,  tag=""):
		EntityShip.__init__(self, pos, hpr, type, owner, tag)
	
# PlanetEntity------------------------------------------------------------------
class EntityPlanet(Entity):
	"""Represents ship logic"""
	type = "Planet"
	
	def __init__(self,  pos=None,  hpr=None,  type="",  owner=None,  tag=""):
		Entity.__init__(self, pos, hpr, type, owner, tag)