'''  Pods and the things we can build out of them '''
import GameUtilities
Location = GameUtilities.Location
NotePage = GameUtilities.NotePage

class Pod:
   ''' defines the base characteristics of the core game unit, the pod'''
   energyConsumed = 0
   energyProduced = 0
   foodConsumed = 0
   foodProduced = 0
   goodsProduced = 0
   cargoCapacity = 0
   
   cargo = 0
   defense = 0
   attack = 0
   damaged = False

class ColonyPod(Pod):
   
   def __init__(self):
      self.energyConsumed = 1
      self.foodConsumed = 1

class ShipPod(Pod):
   '''basic ship's hull pod'''
   def __init__(self):
      self.energyConsumed = 1
      self.foodConsumed = 1

class CrewPod(Pod):
   '''basic crew pod'''
   def __init__(self):
      self.energyConsumed = 1
      self.foodConsumed = 1

class EnergyPod(Pod):
   '''basic energy pod'''
   def __init__(self):
      self.energyProduced = 2
      self.foodConsumed = 1
   
   # future development
   def damage(self):
      self.energyProduced = 0
      self.damaged = True
   def repair(self):
      self.energyProduced = 2
      self.damaged = False

class FarmPod(Pod):
   '''basic food production pod'''
   def __init__(self):
      self.foodProduced = 2
      self.energyConsumed = 1
   
   # future development
   def damage(self):
      self.foodProduced = 0
      self.damaged = True
   def repair(self):
      self.foodProduced = 1
      self.damaged = False

class FactoryPod(Pod):
   def __init__(self):
      self.energyConsumed = 1
      self.foodConsumed = 1
      self.goodsProduced = 1

class CargoPod(Pod):
   '''
   basic cargo pod
   this contains a hint about the future
   of cargo pods - they could be enhanced
   to hold more cargo per unit
   probably best if we subclass to get that effect
   '''
   designCapacity = 1
   inUse = False
   
   def __init__ (self):
      self.cargoCapacity = self.designCapacity
      self.cargo = 0
   
   def loadCargo(self):
      self.inUse = True
   def unloadCargo(self):
      self.inUse = False
   
   # future development
   def damage(self):
      self.cargoCapacity = 0
      damaged = True
   def repair(self):
      self.cargoCapacity = self.designCapacity
      damaged = False
   
class DefensePod(Pod):
   '''basic defense pod'''
   def __init__(self):
      defenseCapacity = 1
      self.energyConsumed = 1
      self.foodConsumed = 1
   
   # future development
   def damage(self):
      self.defenseCapacity = 0
      self.damaged = True
   def repair(self):
      self.defenseCapacity = 1
      self.damaged = False

class WeaponPod(Pod):
   '''basic weapon pod'''
   def __init__(self):
      self.attack = 1
      self.energyConsumed = 1
      self.foodConsumed = 1
   
   #future development
   def damage(self):
      self.attack = 0
      self.energyConsumed = 0
      damaged = True
   def repair(self):
      self.attack = 1
      self.energyConsumed = 1
      damaged = False
   
''' ships and colonies each begin with an Organization '''
  
class Organization:
   ''' abstract superclass for ships and colonies - abstraction not enforced '''
   productionMultiplier = 1
   
   energyProduction = 0
   energyConsumption = 0
   foodProduction = 0
   foodConsumption = 0
   goodsProduction = 0
   crewProduction = 0
   
   availableStorage = 0
   assignedStorage = 0
   energyStored = 0
   foodStored = 0
   goodsStored = 0
   
   energySurplus = 0
   foodSurplus = 0
   goodsSurplus = 0
   
   podList = [] # list of all assigned pods
   population = 0
   
   name = 'Lost City'
   location = Location(0,0)
   
   '''
   these may be good as simply global accumulators instead of lists like this
   if we want to allow variable effects on production and consumption - 
   maybe allow damage, then we might have to include these
   '''
   crewOnEnergy = [] # list of crew assigned to energyProduction
   crewOnFood = [] # list of crew assigned to food production
   crewOnGoods = [] # crew assigned to manufacturing
   crewOnCrew = [] # crew assigned to making more crew
   crewUnassigned = [] # crew available for assignment
   
   def attachPod(self,p):
      self.podList.append(p)
      self.energyConsumption += p.energyConsumed
      self.energyProduction += p.energyProduced
      self.foodConsumption += p.foodConsumed
      self.foodProduction += p.foodProduced
      self.goodsProduction += p.goodsProduced
      self.availableStorage += p.cargoCapacity
      self.assignedStorage += p.cargo
      self.population += 1

   def detachPod(self,p):
      self.podList.remove(p) # I have trust issues with this, but we'll try
      self.energyConsumption -= p.energyConsumed
      self.energyProduction -= p.energyProduced
      self.foodConsumption -= p.foodConsumed
      self.foodProduction -= p.foodProduced
      self.goodsProduction -= p.goodsProduced
      self.availableStorage -= p.cargoCapacity
      self.assignedStorage -= p.cargo
      self.population -= 1

# use this to adjust storage when pods are added or removed
   def adjustStorage(self,a): 
      self.availableStorage += a
      
   def adjustEnergyProduction(self,a):
      self.energyProduction += a
   
   def setName(self,n):
      self.name = n

class Colony(Organization):
   '''
   core characteristics of a colony
   this will probably have to be revised as colonies become more like ships
   the main difference will be that production increases for colonies
   '''
   productionMultiplier = 2 # everything works a little better in the colony
   
   def __init__(self,player,nm='Jonestown',l=Location(0,0)):
      self.owner = player
      self.name = nm
      self.location = l
      self.attachPod(ColonyPod())
      self.assembleColony()
      self.dumpstring = '''
Colony Name: %s
Location: %s
Energy Production:    %d
Energy Consumption:   %d
Food Production:      %d
Food Consumption:     %d
Goods Production:     %d
Crew Production:      %d

Available Storage:    %d
Assigned Storage:     %d
Energy Stored:        %d
Food Stored:          %d
Goods Stored:         %d
      ''' % (self.name, self.location.toString(), self.energyProduction, self.energyConsumption, 
             self.foodProduction, self.foodConsumption, self.goodsProduction, 
             self.crewProduction, self.availableStorage, self.assignedStorage, 
             self.energyStored, self.foodStored, self.goodsStored)
      
   def assembleColony(self):
      ''' create and assign the pods necessary for a basic colony '''
      ''' I acknowledge that this is a blight and should be fixed in refactoring '''
      # give them 30 energy pods
      for r in range(0,30):
         self.attachPod(EnergyPod())
      # give them 30 farm pods
      for r in range(0,30):
         self.attachPod(FarmPod())
      # give them 10 factory pods
      for r in range(0,10):
         self.attachPod(FactoryPod())
      # give them 12 crew pods
      for r in range(0,12):
         self.attachPod(CrewPod())
      # give them 40 cargo pods
      for r in range(0,40):
         self.attachPod(CargoPod())

   def publish(self,note=NotePage()):
      note.addContent(self.dumpstring)
      return note
      
   def dump(self):
      print self.dumpstring

class Ship(Organization):
   ''' core characteristics of a ship '''
      
   def __init__(self,player,nm = 'Titanic',loc=Location(0,0)):
      self.name = nm
      self.owner = player
      self.location = loc
      self.jumpRange = 0
      self.attachPod(ShipPod())
      self.assembleSurveyShip()
      self.dumpstring = '''
Ship Name: %s
Location: %s
Energy Production:    %d
Energy Consumption:   %d
Food Production:      %d
Food Consumption:     %d
Goods Production:     %d
Crew Production:      %d

Available Storage:    %d
Assigned Storage:     %d
Energy Stored:        %d
Food Stored:          %d
Goods Stored:         %d
      ''' % (self.name, self.location.toString(), self.energyProduction, self.energyConsumption, 
             self.foodProduction, self.foodConsumption, self.goodsProduction, 
             self.crewProduction, self.availableStorage, self.assignedStorage, 
             self.energyStored, self.foodStored, self.goodsStored)
      
      def getLocation(self):
         return self.location
      
   def assembleSurveyShip(self):
      ''' this assembles a basic survey ship '''
      self.jumpRange = 10
      for r in range(0,6):
         self.attachPod(CrewPod())
      for r in range(0,6):
         self.attachPod(CargoPod())
      for r in range(0,18):
         self.attachPod(EnergyPod())
      for r in range(0,14):
         self.attachPod(FarmPod())

   def dump(self):      
      print self.dumpstring


