module_name = 'GameUtilities'
version = '1.1.190108'

import random
import math
import time
import datetime
import json

''' game utility section begins '''
     
def get_tty_input(prompt):
   print prompt
   return raw_input(" ")

def radius(x):
   return range(-x, x + 1)  # helpful for scanning

'''
We might not need this custom encoder, but we'll put it here
in case we want to modify it to deal with unusual conditions
(it probably belongs in utils)
'''

class MyEncoder(json.JSONEncoder):

   def default(self, o):
      return o.__dict__

class IDTimestamp ():
   '''
      default constructor gives back a formatted string in the form:
      yymmdd.hhmmss
      for use in longer identifiers. For instance, a Note ID will probably be:
      oooooooo.yymmdd.hhmmss-salt
      where oooooooo is the note owner identifier.
   '''
   tstring = ''

   def __init__(self):
      ts = time.time()
      candidate = datetime.datetime.fromtimestamp(ts).strftime('%y%m%d.%H%M%S')
      self.tstring = '%s.%03d' % (candidate, VariableDie(1000).roll())  # added salt here... probably okay

class NameMaker():

   def grantName(self):
      # get an alpha identifier - TODO this needs to be much better - use a time stamp at least
      alphaSet = 'abcdefghijklm9876543210nopqrstuvwxyz'
      ltr = VariableDie(len(alphaSet) - 1).roll()
      id1 = alphaSet[ltr]
      id2 = VariableDie(999).roll()
      id3 = VariableDie(255).roll()
      idt = IDTimestamp().tstring
      finalName = '%s%s%03d%03d' % (idt, id1, id2, id3)
      return finalName

class VariableDie ():
   ''' Variable Die
         usage:
            outcome = VariableDie(number_of_sides).roll()
         or:
            twentysides = VariableDie(20)
            twentysides.roll()
         or:
            d = VariableDie()
            d.roll() # give you 1-6
   '''

   def __init__ (self, sides=6):
      self.sides = sides
      
   def roll(self):
      # return random number between where n is  1 <= n >= upperLimit
      return random.randint(1, self.sides)
   
   def testme(self):
      # test harness for just this class
      upperBound = self.sides      
      result = []
   
      for i in xrange(0, upperBound):
         result.append(i)
      for d in xrange(1, 200000):
         r = VariableDie(upperBound).roll()
         print '%d r is %d' % (d,r)
         result[r - 1] += 1
      
      lowest = 0
      highest = 0
      for o in range(0, len(result)):
         dieroll = o + 1
         repeats = result[o]
         if dieroll == 1: lowest = repeats     
         if repeats < lowest: lowest = repeats
         if repeats > highest: highest = repeats
         print 'result for %d is %d' % (dieroll, repeats)
         
      print '\nhighest is %d' % highest
      print 'lowest is %d' % lowest

      ''' main test harness of VariableDie ends '''

class NotePage():
   ''' this is a message that can be displayed in a variety of contexts
      it is a core element of the game. Commands, reminders, communications,
      journals, notebooks, they are all implemented as instances of NotePage
   '''
   contentString = ''
   content = {'headers' : {'modified_date':1}, 'payload' : contentString}
   noteID = ''
   
   def __init__(self, msg='uninitialized'):
      self.contentString = msg
      self.noteID = NameMaker().grantName()
      #self.content.headers{'modified_date'} = time.strftime('%yy%mm%dd%hh%mm%ss', time.gmtime())

   def setContent(self, msg):
      self.contentString = msg

   def getContent(self):
      return self.contentString

   def dumpContent(self):
      print self.contentString

   def dumpEntirely(self):
      for h in self.content['headers'].keys():
         print '%s: %s' % (h, self.content['headers'][h])
      print 'Content:'
      self.dumpContent()

   def addHeader(self, h, c):
      self.content['headers'][h] = c

   def hasHeader(self, h):
      return h in self.content['headers']

class NoteBook():
   ''' this is a collection of note pages - one is assigned to each colony and ship 
   as player scratchpad and log - other notebooks can exist as game elements '''
   pageList = []

   def __init__(self, c=NotePage('Cover Page')):
      self.pageList.append(c)

   def addPage(self, note=NotePage()):
      self.pageList.append(note)

   def getNotebook(self):
      # there is always at least one page, so it's okay to do this
      return self.pageList

   def dumpNotebook(self):
      for p in self.pageList:
         p.dumpContent()

class Location3D():
   ''' contains a 3- dimensional cartesian coord '''
   xCoord = 0
   yCoord = 0
   zCoord = 0
    
   def __init__(self, x, y, z):
      self.xCoord = x
      self.yCoord = y 
      self.zCoord = z 
        
   def distanceTo(self, p):
      '''
          staged for our move to 3D space
          public double distanceTo(Point3d p) {
            return Math.sqrt(Math.pow(x - p.getxCoord(), 2) + Math.pow(y - p.getyCoord(), 2) +                 Math.pow(z - p.getzCoord(), 2));
      '''
      deltaX = self.xCoord - p.xCoord
      deltaY = self.yCoord - p.yCoord
      deltaZ = self.zCoord - p.zCoord
      return math.sqrt(deltaX ** 2 + deltaY ** 2 + deltaZ ** 2)

class Location():
   ''' contains one 2-dimensional cartesian coord -- actually, it should be simply a coordinate
      Using overloading, when a method only knows two dimensions, they will be X and Y - with Z being
      set to zero by default. We will remove the "Location3D" class soon
   '''
   xCoord = 0
   yCoord = 0

   def __init__(self, x, y):
      self.xCoord = x
      self.yCoord = y
      
   def toString(self):
      return '(%d, %d)' % (self.xCoord, self.yCoord)
 
   def distanceTo(self, loc):
      deltaX = self.xCoord - loc.xCoord
      deltaY = self.yCoord - loc.yCoord 
      return math.sqrt(deltaX ** 2 + deltaY ** 2)

