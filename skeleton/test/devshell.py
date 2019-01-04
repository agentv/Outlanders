'''
Created on Jan 3, 2019

@author: VincentLowe
'''
import cmd
import json

import gb
import cc
import gu

DieRoll = gu.VariableDie

class GameShell(cmd.Cmd):
   ''' we have a global Gameboard structure called g, estabalished in preloop() 
   this whole class is a giant hack
   its purpose is simply to provide a test bed for game functions
   
   TODO - This shell should be moved from the current file into a test/devshell.py file
   '''
   
   # overrides
   prompt = '\nPODS command: $ '
   
   # globals for easy shell control
   activePlayer = gb.Player()
   activeShip = cc.Ship(gb.Player())
   activeColony = cc.Colony(gb.Player())
   activeSector = gb.Sector()
   
   def preloop(self):
      cmd.Cmd.preloop(self)
      self.g = gb.GameBoard()
      
   def postloop(self):
      print 'Thanks for playing!\n'
   
   def do_moveship(self, line):
      choice = gu.get_tty_input('x location? ')
      xspot = int(choice)
      choice = gu.get_tty_input('Y location? ')
      yspot = int(choice)
      rslt = self.g.moveShip(self.activeShip, gu.Location(xspot, yspot))
      if rslt:
         print 'that worked!'
      else:
         print 'that did not work'
      
   def help_dumpplayers(self):
      print 'show details for all players'

   def do_dumpplayers(self, line):
      print 'Details for all Players: '
      for plyr in self.g.playerTable:
         print plyr.playerName
         plyr.dump()
   
   def help_showplayers(self):
      print 'display a list of all players'

   def do_showplayers(self, line):
      print 'These are the Players:'
      ndx = 1
      for plyr in self.g.playerTable:
         print '[%d] %s' % (ndx, plyr.playerName)
         ndx += 1   

   def help_selectplayer(self):
      print 'choose active player from a numbered list'

   def do_selectplayer (self, line):
      self.do_showplayers(line)
      choice = gu.get_tty_input('Which one? ')
      print 'You chose: [%s]' % choice
      self.activePlayer = self.g.playerTable[int(choice) - 1]    
   
   def help_selectship(self):
      print 'select active ship from a numbered list'

   def do_showships(self, line):
      ndx = 1
      print 'These are the ships for %s' % self.activePlayer.playerName
      for ship in self.activePlayer.shipmaster:
         print '[%d] %s' % (ndx, ship.name)
         ndx += 1

   def do_selectship(self, line):
      self.do_showships(line)
      choice = gu.get_tty_input('Which one? ')
      print 'You chose [%s]' % choice
      self.activeShip = self.activePlayer.shipmaster[int(choice) - 1]
      loc = self.activeShip.location
      self.activeSector = self.g.locateSector(loc)

   def do_showcolonies(self, line):
      ndx = 1
      print 'These are the colonies for player: %s' % self.activePlayer.playerName
      for colony in self.activePlayer.colonymaster:
         print '[%d] %s' % (ndx, colony.name)
         ndx += 1
          
   def help_selectcolony(self):
      print 'select active colony from a numbered list'

   def do_selectcolony(self, line):
      self.do_showcolonies(line)
      choice = gu.get_tty_input('Which one? ')
      print 'You chose [%s]' % choice
      self.activeColony = self.activePlayer.colonymaster[int(choice) - 1]
      loc = self.activeColony.location
      self.activeSector = self.g.locateSector(loc)
   
   def help_showsectors(self):
      print 'dumps details about all known sectors'

   def do_showsectors(self, line):
      print 'ready to dump known sectors'
      self.g.dump()
  
   def do_status(self, line):
      statusstring = '''Active Player: %s
Active Sector: %s
Active Colony: %s
Active Ship: %s''' % (self.activePlayer.playerName, self.activeSector.location.toString(),
                      self.activeColony.name, self.activeShip.name)
      print statusstring
      
   def help_showgameboard(self):
      print 'shows the gameboard as JSON'

   def do_showgameboard(self, line):
      print 'here is the gameoboard as JSON'
      # do the thing here
      # print json.dumps(self.g,enc=MyEncoder) # currently broken
      print self.g.dump()

   def help_dump(self):
      print 'dumps the gameboard'

   def do_dump(self, line):
      print 'printing the gameboard'
      self.g.dump()
   
   def do_quit(self, line):
      return True

   def do_EOF(self, line):
      return True
   
   ############### test routines ##########################   
   def do_showRegistry(self, line):
      self.g.registry.dump()

   def help_jdumpSectors(self):
      print "dump entire sector table as JSON"

   def do_jdumpSectors(self, line):
      print json.dumps(self.g.sectorTable)
      
   def help_initializeSectors(self):
      print "populate a 14x14 grid of sectors near the origin, then emit the JSON for each sector"

   def do_initializeSectors(self, line):
      for x in range(0, 14):
         if not x in self.g.sectorTable:
            self.g.sectorTable[x] = {}
         for y in range (0, 14):
            # print "x is: |%s| -- and y is: |%s|" % (x,y)
            self.g.sectorTable[x][y] = (gb.Sector(gu.Location(x, y)))
      for x in range(0, 14):
         for y in range(0, 14):
            sect = self.g.sectorTable[x][y]
            print json.dumps(sect)
      
   def help_name(self):
      print 'test name generator'

   def do_name(self, line):
      # test that we can get a unique new name
      t = gu.NameMaker().grantName()
      print t

   def help_sectorfinder(self):
      print 'find a sector matching cartesian input ie: (x,y)'

   def do_sectorfinder(self, line):
      choice = gu.get_tty_input('x location? ')
      xspot = int(choice)
      choice = gu.get_tty_input('Y location? ')
      yspot = int(choice)
      sect = self.g.locateSector(gu.Location(xspot, yspot))
      sect.dump()

   def help_addplayer(self):
      print 'tests the addplayer functionality'

   def do_addplayer(self, line):
      r = gb.MasterRegistry()
      r.addPlayer(gb.Player('Joan Watson'))
      r.dump()

   def help_saveSectorTable(self):
      print "write out the sector table as JSON file"

   def do_saveSectorTable(self, line):
      print 'ready to write sector table to file'
      f = open("resources/sectortable.json", "w")
      tbl = json.dumps(self.g.sectorTable)
      f.write(tbl)
      f.close()
      
   def help_readNamesMemory(self):
      print '''simply read from a resource file into memory'''

   def do_readNamesMemory(self, line):
      localnames = []
      print 'ready to read names in'
      f = open("resources/names", "r")
      for n in f:
         localnames.append(n.rstrip('\n\t '))
      f.close()
      for nm in localnames:
         print "another name is: %s" % nm 
      return localnames
         
   def do_bigTable(self, line):
      ''' 
         This routine makes a file that is 25MB in size
         it's just 140x140 - quite a few sectors, but
         not big data by any means      
       '''
      print 'ready to make giant sector table'
      t = self.g.sectorTable
      for x in range(300, 440):
         if not x in t:
            t[x] = {}
         for y in range(300, 440):
            t[x][y] = (gb.Sector(gu.Location(x, y)))
      print 'giant sector table created, now writing...'
      fstore = open('resources/bigSectorTable.json', 'w')
      tbl = json.dumps(t)
      fstore.write(tbl)
      fstore.close()
      
   def do_selectMapPages(self, line):
      t = self.g.sectorTable
      print 'ready to write out just select pages to a file'
      origins = [[120, 400], [270, 600], [80, 150], [400, 390]]
      for o in origins:
         print 'mapping sectors from origin: %02d,%02d' % (o[0], o[1])
         for x in range(o[0], o[0] + 12):
            if not x in t:
               t[x] = {}
            for y in range(o[1], o[1] + 12):
               t[x][y] = (gb.Sector(gu.Location(x, y)))
         print 'map page created, now to write it to a file...'
         fstore = open('resources/sectorTable.%03d%03d.json' % (o[0], o[1]), 'w')
         tbl = json.dumps(t)
         fstore.write(tbl)
         fstore.close()
      
   def do_noteEditorTest(self, line):
      done = False
      tempPage = gu.NotePage('')
      print '''
This is simply a test to validate the structure and methods of the
NotePage class. It uses a temporary NotePage that will be destroyed
after the test succeeds.

Type lines of input
End by using a line with only "..."

      '''
      while (done != True):
         # something
         nextLine = gu.get_tty_input('line: ')
         if (nextLine == '...'):
            done = True
         else:
            # add it to the page
            tempPage.setContent(tempPage.getContent() + '\n' + nextLine)
      print 'Here is your page'
      tempPage.dumpContent()        
   
   def do_noteHeaderTest(self, line):
      ''' add a note, add a header, emit the note '''
      n = gu.NotePage('This is your sample note page')
      n.addHeader('Content-Type', 'text/plain')
      
      print 'ready to show message content'
      n.dumpContent()
      
      print 'now a list of headers'
      print n.content['headers'].keys()
      
      print 'now, can we find a specific Header (ie. Content-Type)?'
      print n.hasHeader('Content-Type')
      
      print 'also, change the content string, does that propogate to the object?'
      n.setContent('Another message, in case you are listening.')
      n.dumpContent()  # proves that "content" contains a reference to "contentString"
      
      print 'and now, the entire message:'
      n.dumpEntirely()
      
   def do_makeFile(self,line):
      print 'making a new file'
      fhandle = open('RightHereBeeches','w')
      fhandle.write('words on a page')
      fhandle.close()
      
   def do_noteStorageTest(self, line):
      print 'creates a set of notes and stores them into MessageRegistry'
      lines = self.do_readNamesMemory('blah!')
      line_ct = len(lines)
      # generate some number of messages
      for m in xrange(0, 20):
         # select three random names from lines
         manny = lines[DieRoll(line_ct - 1).roll()]
         moe = lines[DieRoll(line_ct - 1).roll()]
         jack = lines[DieRoll(line_ct - 1).roll()]
         missive = '%s%s%s' % (manny, moe, jack)
         # you can tell when I'm getting loopy
         # store message in Message Registry
         np = gu.NotePage(missive)
         self.g.legend.insertNote(np.noteID, np)
      
      # dump Message Registry
      self.g.legend.dump()

def main():
   GameShell().cmdloop()

if __name__ == '__main__':
   main()
