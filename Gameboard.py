#!/usr/local/bin/python

'''
module that contains the Game Board, Sector, Player, 
and MasterRegistry
 
it also contains test yokes for various system functions
including the GameShell that allows console operation
of game functions

The Gameboard hosts all of the actual game functions
such as randomizer (dice) and a sector map
'''

import cmd
import sys
import json
import GameUtilities
from compiler.pyassem import DONE
import CoreClasses 

Ship = CoreClasses.Ship
Colony = CoreClasses.Colony

Location = GameUtilities.Location
NotePage = GameUtilities.NotePage
DieRoll = GameUtilities.VariableDie


# TODO - now that command-line processing is in place, use that to control
# testing as development proceeds

# Overall game elements, game board, players, and game squares (ie. sectors)


# TODO - convert this static dictionary into a routine that reads from a JSON file
'''
This stock setup table sets the Gameboard to a known configuration
as a fixed way to start the game. In the long run, the plan should
be to read this material in from a JSON dataset and to have a way
for players to affect the startup somewhat before the game start
This data structure is referenced in the game setup routine
startPositions()
'''

stockSetup = {
  'Alexander': {
       'loc': Location(545, 250),
       'rssNames': ('Tesla 3', 'Captain Cook', 'Adm. Byrd') 
   },
  'Greg': { 
       'loc': Location(245, 550),
       'rssNames': ('Portsmouth', 'Lindbergh', 'Cousteau')
   },
  'Roosevelt': {
       'loc': Location(525, 310),
       'rssNames': ('Sanders', 'Babbage', 'Nelson')
   },
  'Napolean': {
       'loc': Location(340, 505),
       'rssNames': ('Botany Bay', 'Kennedy', 'Eisenhower')
   }
}

'''
We might not need this custom encoder, but we'll put it here
in case we want to modify it to deal with unusual conditions
'''
class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

class MasterRegistry:
   ''' 
   The Registry holds the Player, Ship, and Colony objects
   Each object stored in the registry has a unique key
   generated by the NameMaker - it's not clear that this name
   will be used later although it's likely.
   
   It's probable that if the GameBoard and the MasterRegistry
   are serialized, that the entire game is preserved.
   '''
   register = {}
   def __init__(self):
      self.register = {} # be sure it's empty upon creation
      self.nameMaker = GameUtilities.NameMaker()
      
   def addColony(self,c):
      # arg c is a fully instantiated colony
      pre = 'c'
      self.registryInsert(pre, c)
   
   def addShip(self,s):
      # arg s is a fully instantiated ship
      pre = 's'
      self.registryInsert(pre, s)

   def addPlayer(self,p):
      # second arg is a fully instantiated Player
      pre = 'p'
      self.registryInsert(pre, p)

   def registryInsert(self,prefix,element):
      # prefix is a type string, element is an object
      nameAppendage = self.nameMaker.grantName()
      nameCandidate = '%s%s' % (prefix,nameAppendage)
      while self.register.has_key(nameCandidate):
         nameAppendage = self.nameMaker.grantName()
         nameCandidate = '%s%s' % (prefix,nameAppendage)
      self.register[nameCandidate] = element
      
   def dump(self):
      dumpstring = 'Master Registry:\n===============\n'
      rstring = ''
      for o in self.register.keys():
          rstring += '%s -> %s\n' % (o,self.register[o])
      # rstring = '\n'.join(self.register.keys())
      print '%s%s' % (dumpstring,rstring)             

class GameBoard:
   ''' defines the characteristic of the full game board'''

   def __init__(self):
      self.sectorTable = {} # we use a dictionary to create a sparse matrix
      self.sectorTable[0] = {}
      self.addSector(Sector(Location(0,0)))
      
      self.playerTable = []
      
      self.registry = MasterRegistry()
      self.startPositions()
  
   def scanNeighbors(self,sect):
      xc = sect.location.xCoord
      yc = sect.location.yCoord
      for row in range(xc-1,xc+2): # check each neighbor and establish sectors where needed
         for col in range(yc-1,yc+2):
            rcstring = '(%d,%d)' % (row,col)
            if not row in self.sectorTable:
               self.sectorTable[row] = {}
            if not col in self.sectorTable[row]:
               self.addSector(Sector(Location(row,col)))
   
   def addPlayer(self,p):
      self.playerTable.append(p)
      self.registry.addPlayer(p)
       
   def moveShip(self,ship,newLocation):
      oldLocation = ship.location
      #get sector for current ship's location
      oldSector = self.locateSector(oldLocation)
      # no failure mode is handled here
      jumpDistance = oldSector.distanceTo(newLocation)
      if jumpDistance > ship.jumpRange:
         return False
      
      # get sector for target location
      newSector = self.locateSector(newLocation)
      oldSector.removeShip(ship)
      newSector.addShip(ship)
      ship.location = newLocation
      return True
      
   def startPositions(self):
      for p in stockSetup.keys():
         plyr = Player(p)
         self.addPlayer(plyr)
         spot = stockSetup[p]['loc']
         
         sect = Sector(spot)
         self.addSector(sect)
         ''' one problem here is the static nature of this setup
             everyone has exactly 1 colony and exactly two ships
             a more progressive approach would be to allow an
             object-driven startup - for now, we're going to implement
             that with a "turn 0" that allows them to roll up a bunch 
             of surplus resources into whatever they wish
         '''

         co = Colony(plyr, stockSetup[p]['rssNames'][0], spot)
         plyr.addColony(co)
         self.registry.addColony(co)
         sect.hasColony = True
         
         sh = Ship(plyr, stockSetup[p]['rssNames'][1], spot)
         plyr.addShip(sh)
         self.registry.addShip(sh)
         sect.addShip(sh)
         
         sh = Ship(plyr, stockSetup[p]['rssNames'][2], spot)
         plyr.addShip(sh)
         self.registry.addShip(sh)
         sect.addShip(sh)
         
         homeColony = plyr.colonymaster[0]
         homeColony.goodsSurplus = 30
         homeColony.foodSurplus = 90
         homeColony.energySurplus = 200

   def addSector(self, s):
      xcoord = s.location.xCoord
      ycoord = s.location.yCoord
      if not xcoord in self.sectorTable:
         self.sectorTable[xcoord] = {}
      if not ycoord in self.sectorTable[xcoord]:
         self.sectorTable[xcoord][ycoord] = s
      else:
         print 'log an error because we tried to overwrite a sector'

   def locateSector(self,loc):
      ''' returns sector at the given location '''
      ndx = loc.xCoord
      ndy = loc.yCoord
      if not (self.sectorTable.has_key(ndx) and self.sectorTable[ndx].has_key(ndy)):
         s = Sector(Location(ndx,ndy))
         self.addSector(s)
         return s
      return self.sectorTable[ndx][ndy]

   
   def dump(self):
      for r in self.sectorTable.keys():
         for c in self.sectorTable[r].keys():
            self.sectorTable[r][c].dump()
            
   def getSector(self,loc=Location(0,0)): # this throws a key error if table not populated
      return (self.sectorTable[loc.xCoord][loc.yCoord])         


class Sector:
   ''' core characteristics of any Sector '''
   
   manufacturingCapacity = 0
   farmingCapacity = 0
   energyCapacity = 0
   
   manufacturingDeveloped = 0
   farmingDeveloped = 0
   energyDeveloped = 0
   
   portAuthority = []  # list of ships in sector
   
   hasColony = False  # flag used now to prevent multiple colonies in one sector
   
   ''' add/remove quotes at end of line to enable or disable 
   colonyCommission = [] # list of colonies in sector - future development
   recreationalResources = 0 # future development (maybe)
   researchResources = 0 # future development (maybe)
   # end of future development section '''
   
   def dump(self):
      dumpstring = '''====================================
Sector at: %2d, %2d
Food (production/capacity): %d / %d
Energy (production/capacity): %d / %d
Goods (production/capacity): %d / %d
Colony Present: %s
====================================''' % (self.location.xCoord, self.location.yCoord,
                                          self.farmingDeveloped, self.farmingCapacity,
                                          self.energyDeveloped, self.energyCapacity,
                                          self.manufacturingDeveloped, self.manufacturingCapacity,
                                          self.hasColony)
      print dumpstring
   
   def addShip(self, s):
      self.portAuthority.append(s)
      
   def removeShip(self, s):
      self.portAuthority.remove(s)
      
   def __init__(self, l=Location(0, 0)):
      self.location = l
      xc = l.xCoord
      yc = l.yCoord
      
      boost = 0  # added to resource calc when we know where
      if xc < 400 or yc < 400: 
         boost += 40
      if xc < 200 or yc < 200:
            boost += 40
         
      self.manufacturingCapacity = 20 + DieRoll(30).roll() + boost
      self.farmingCapacity = 50 + DieRoll(30).roll() + boost
      self.energyCapacity = 70 + DieRoll(20).roll() + boost
               
   def distanceTo (self, loc=Location(0, 0)):
      xDelta = abs(self.location.xCoord - loc.xCoord)
      yDelta = abs(self.location.yCoord - loc.yCoord)
      distance = xDelta + yDelta
      return distance


class Player:
   '''core characteristics of a single game player'''
   totalCropProduction = 0
   totalManufacturing = 0
   totalEnergyProduction = 0
   totalPopulation = 0
   generalMorale = 0
   playerName = ''
      
   def addColony(self,co):
      self.colonymaster.append(co)
      self.totalPopulation += co.population
      
   def addShip(self,sh):
      self.shipmaster.append(sh)
      self.totalPopulation += sh.population
        
   def __init__ (self, nm='Caligula'):

      '''grant starting resources and update globals'''
      self.playerName = nm
      self.generalMorale = 0
      
      self.colonymaster = []
      self.shipmaster = []
      
      self.dumpstring = '''
Player Name:             %s
Total Population:        %d
Population Morale:       %d
Total Crop Production:   %d
Total Energy Production: %d
Total Goods Production:  %d
      ''' % (self.playerName, self.totalPopulation, self.generalMorale, 
             self.totalCropProduction, self.totalEnergyProduction, self.totalManufacturing)
      
   ''' end of Player constructor '''

   def publish(self,note=NotePage()):
      note.setContent(self.dumpstring)
      return note
           
   def dump(self):
      print '%s' % self.dumpstring      
      for i in self.colonymaster:
         i.dump()
      for i in self.shipmaster:
         i.dump()

class GameShell(cmd.Cmd):
   ''' we have a global Gameboard structure called g, estabalished in preloop() 
   this whole class is a giant hack
   its purpose is simply to provide a test bed for game functions
   '''
   
   # overrides
   prompt = 'PODS command: '
   
   #globals for easy shell control
   activePlayer = Player()
   activeShip = Ship(Player())
   activeColony = Colony(Player())
   activeSector = Sector()
   
   def preloop(self):
      cmd.Cmd.preloop(self)
      self.g = GameBoard()
      
   def postloop(self):
      print 'Thanks for playing!\n'
   
   def do_moveship(self,line):
      choice = GameUtilities.get_tty_input('x location? ')
      xspot = int(choice)
      choice = GameUtilities.get_tty_input('Y location? ')
      yspot = int(choice)
      rslt = self.g.moveShip(self.activeShip, Location(xspot,yspot))
      if rslt:
         print 'that worked!'
      else:
         print 'that did not work'
      
   def help_dumpplayers(self):
       print 'show details for all players'
   def do_dumpplayers(self,line):
       print 'Details for all Players: '
       ndx = 1
       for plyr in self.g.playerTable:
           print plyr.playerName
           plyr.dump()
    
   
   def help_showplayers(self):
      print 'display a list of all players'
   def do_showplayers(self,line):
      print 'These are the Players:'
      ndx = 1
      for plyr in self.g.playerTable:
         print '[%d] %s' % (ndx, plyr.playerName)
         ndx += 1   
   def help_selectplayer(self):
      print 'choose active player from a numbered list'
   def do_selectplayer (self,line):
      self.do_showplayers(line)
      choice = GameUtilities.get_tty_input('Which one? ')
      print 'You chose: [%s]' % choice
      self.activePlayer = self.g.playerTable[int(choice)-1]    
   
   def help_selectship(self):
      print 'select active ship from a numbered list'
   def do_showships(self,line):
      ndx = 1
      print 'These are the ships for %s' % self.activePlayer.playerName
      for ship in self.activePlayer.shipmaster:
         print '[%d] %s' % (ndx, ship.name)
         ndx += 1
   def do_selectship(self,line):
      self.do_showships(line)
      choice = GameUtilities.get_tty_input('Which one? ')
      print 'You chose [%s]' % choice
      self.activeShip = self.activePlayer.shipmaster[int(choice)-1]
      loc = self.activeShip.location
      self.activeSector = self.g.locateSector(loc)
       
   
   def help_selectcolony(self):
      print 'select active colony from a numbered list'
   def do_showcolonies(self,line):
      ndx = 1
      print 'These are the colonies for player: %s' % self.activePlayer.playerName
      for colony in self.activePlayer.colonymaster:
         print '[%d] %s' % (ndx, colony.name)
         ndx += 1
   def do_selectcolony(self,line):
      self.do_showcolonies(line)
      choice = GameUtilities.get_tty_input('Which one? ')
      print 'You chose [%s]' % choice
      self.activeColony = self.activePlayer.colonymaster[int(choice)-1]
      loc = self.activeColony.location
      self.activeSector = self.g.locateSector(loc)
   
   def help_showsectors(self):
      print 'dumps details about all known sectors'
   def do_showsectors(self,line):
      print 'ready to dump known sectors'
      self.g.dump()
  
   def do_status(self,line):
      statusstring = '''Active Player: %s
Active Sector: %s
Active Colony: %s
Active Ship: %s''' % (self.activePlayer.playerName, self.activeSector.location.toString(), 
                      self.activeColony.name, self.activeShip.name)
      print statusstring
      
   def help_showgameboard(self):
       print 'shows the gameboard as JSON'
   def do_showgameboard(self,line):
       print 'here is the gameoboard as JSON'
       # do the thing here
       json.dumps(g,enc=MyEncoder)

   def help_dump(self):
      print 'dumps the gameboard'
   def do_dump(self,line):
      print 'printing the gameboard'
      self.g.dump()
   
   def do_quit(self,line):
      return True
   def do_EOF(self,line):
      return True
   
   ############### test routines ##########################   
   def do_makePage(self,line):
      done = False
      tempPage = NotePage('')
      print '''
This is simply a test to validate the structure and methods of the
NotePage class. It uses a temporary NotePage that will be destroyed
after the test succeeds.

Type lines of input
End by using a line with only "..."

      '''
      while (done != True):
         #something
         nextLine = GameUtilities.get_tty_input('line: ')
         if (nextLine == '...'):
            done = True
         else:
            # add it to the page
            tempPage.setContent(tempPage.getContent() + '\n' + nextLine)
      print 'Here is your page\n\n'
      tempPage.dumpContent()        
   
   def do_showRegistry(self,line):
      self.g.registry.dump()
   def do_sectorsjson(self,line):
      gm = self.g
      sect = gm.sectorTable[0][0] # TODO - okay, let's make this more generalized now...
      print json.dumps(sect,cls=MyEncoder)
   
   def help_spillmap(self):
       print "emitting a 14x14 grid of sectors"
   def do_spillmap(self,s):
        print "populating a 14x14 region"
        gm = self.g
        m = [15][15]
        for x in range(0,14):
            for y in range (0,14):
                m[x][y] = Sector(Location(x,y))
        for x in range(0,14):
            for y in range(0,14):
                sect = gm.sectorTable[x][y]
                print json.dumps(sect,cls=MyEncoder)
      
   def help_name(self):
      print 'test name generator'
   def do_name(self,line):
      # test that we can get a unique new name
      t = GameUtilities.NameMaker().grantName()
      print t
   def help_sectorfinder(self):
      print 'find a sector matching cartesian input ie: (x,y)'
   def do_sectorfinder(self,line):
      choice = GameUtilities.get_tty_input('x location? ')
      xspot = int(choice)
      choice = GameUtilities.get_tty_input('Y location? ')
      yspot = int(choice)
      sect = self.g.locateSector(Location(xspot,yspot))
      sect.dump()
   def help_addplayer(self):
      print 'tests the addplayer functionality'
   def do_addplayer(self,line):
      r = MasterRegistry()
      r.addPlayer(Player('Joan Watson'))
      r.dump()

