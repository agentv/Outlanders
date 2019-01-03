import random
import math
import time
import datetime

''' game utility section begins '''
      
def get_tty_input(prompt):
   print prompt
   return raw_input(" ")

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
      self.tstring = '%s.%03d' % (candidate,VariableDie(1000).roll()) # added salt here... probably okay
      
   def newTS(self):
      ts = time.time()
      candidate = datetime.datetime.fromtimestamp(ts).strftime('%y%m%d.%H%M%S')
      return '%s.%03d' % (candidate,VariableDie(1000).roll()) # added salt here... probably okay
      

class NameMaker():
   def grantName(self):
      # get an alpha identifier - TODO this needs to be much better - use a time stamp at least
      alphaSet = 'abcdefghijklm9876543210nopqrstuvwxyz'
      ltr = VariableDie(len(alphaSet)-1).roll()
      id1 = alphaSet[ltr]
      id2 = VariableDie(999).roll()
      id3 = VariableDie(255).roll()
      idt = IDTimestamp().newTS()
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
      #return random number between where n is  1 <= n >= upperLimit
      return random.randint(1,self.sides)
   
   def testme(self):
      # test harness for just this class
      upperBound = self.sides      
      result = []
      lowest = 0
      highest = 0
   
      for i in range(0,upperBound):
         result.append(0)
      for d in range(1,200000):
         r = VariableDie(upperBound).roll()
         # print 'r is %d' % r
         result[r-1] += 1
      
      lowest = 0
      highest = 0
      for o in range(0,len(result)):
         dieroll = o+1
         repeats = result[o]
         if dieroll == 1: lowest = repeats     
         if repeats < lowest: lowest = repeats
         if repeats > highest: highest = repeats
         print 'result for %d is %d' % (dieroll, repeats)
         
      print '\nhighest is %d' % highest
      print 'lowest is %d' % lowest

      ''' main test harness of VariableDie ends '''

class NotePage():
   ''' this is a message that can be displayed in a variety of contexts '''
   contentString = ''
   content = {"headers" : {"dummy":1}, "payload" : contentString}
   noteID = ''
   
   def __init__(self,msg='uninitialized'):
      self.contentString = msg
   def setContent(self,msg):
      self.contentString = msg
   def getContent(self):
      return self.contentString
   def dumpContent(self):
      print self.contentString
   def dumpEntirely(self):
      for h in self.content['headers'].keys():
         print '%s: %s' % (h,self.content['headers'][h])
      self.dumpContent()
   def addHeader(self,h,c):
      self.content['headers'][h] = c
   def hasHeader(self,h):
      return h in self.content['headers']

class NoteBook():
   ''' this is a collection of note pages - one is assigned to each colony and ship as player scratchpad and log '''
   pageList = []
   def __init__(self,c=NotePage('Cover Page')):
      self.pageList.append(c)
   def addPage(self,note=NotePage()):
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
    
    def __init__(self,x,y,z):
        self.xCoord = x
        self.yCoord = y 
        self.zCoord = z 
        
    def distanceTo(self,p):
        '''
          staged for our move to 3D space
          public double distanceTo(Point3d p) {
            return Math.sqrt(Math.pow(x - p.getxCoord(), 2) + Math.pow(y - p.getyCoord(), 2) + 
                Math.pow(z - p.getzCoord(), 2));
        '''                
        deltaX = xCoord - p.xCoord
        deltaY = yCoord - p.yCoord
        deltaZ = zCoord - p.zCoord
        return math.sqrt(deltaX**2 + deltaY**2 + deltaZ**2)

class Location():
   ''' contains one 2-dimensional cartesian coord '''
   xCoord = 0
   yCoord = 0
   def __init__(self,x,y):
      self.xCoord = x
      self.yCoord = y
      
   def toString(self):
    return '(%d, %d)' % (self.xCoord,self.yCoord)
 
   def distanceTo(self,loc):
      deltaX = xCoord - loc.xCoord
      deltaY = yCoord - loc.yCoord 
      return math.sqrt(deltaX**2 + deltaY**2)
   
   

