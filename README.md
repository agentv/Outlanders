# Outlanders
Python Model for exploration and industry game

## Usage
When this is finished, it will be deployed as a web application implemented as Python core code (server) and delivered as NoteBook objects as implemented in the game. Maps, unit status, game communications, all can be encapsulated in a NoteBook.

## Backstory
Mankind has at last inherited the stars. With the invention of reliable FTL drive, and long-range scout ships, it is 
finally possible for humanity to move into the vastness of space and colonize the worlds that are suitable for living.

Using modular components (Pods) a society can expand using ships and founding colonies in newly scouted sectors of
outer space.

Unmanned scout ships roam the spaceways looking for habitable new worlds, and groups of humans travel in colony ships to claim and shape the worlds that turn up.

Each player in this game controls one society in a shared universe. Ships can move to promising locations, or sit
still and conduct operations in its current sector. They can harvest energy, produce food or goods, or make more
people and Pods. Ships can be converted into colonies which sacrifices their ability to move, but increases their
ability to produce.

Each Pod represents a group of people and resources (including equipment) to accomplish a specific goal. Most Pods
consume food resources. Most of them consume energy resources.

A player’s team can focus on expansion, industry, trade or militarization.

## Game Structure

The primary components in the design of the game are Pods, Ships, Colonies, and Players.

There is a Gameboard component that encapsulates most of the administrative functions of the game. 
For instance, the logic for processing "end-of-turn" calculations is a part of the Gameboard.
The timers are part of the Gameboard as are the random result artifacts (ie. dice)
Sectors are the cells of the Gameboard and they contain information about activities within their
boundaries. Each Sector contains a registry of ships in the sector, colonies established in the
sector, and statistics about maximum production for energy, food, and goods.

## Game Elements

The primary elements of the game give rise to its structure, and for that matter, its tone and
promising strategies.

### Pods

This is the fundamental element of the game universe. Pods represent the abstraction of a group of
people, their equipment, and the resources they need to conduct their assigned mission. These are the
types of Pods defined in the game:

* Crew Pod - Just people and general purpose tools. These can be assigned to a variety of missions. They are
less productive than specialized Pods, but the flexibility of their deployment commends them as valuable to
have in abundance.
* Farm Pods - Produce food in quantities greater than general purpose pods. They consume energy, but not food.
They are presumed to simply skim their own wares!
* Energy Pods - These produce energy for use by other Pods. A society needs a bunch of these, and no ship
should set out without enough of them
* Factory Pods - These produce goods. They consume energy and food. When a society wants to build new Pods or
convert a ship to a Colony they will need available goods to be on hand. They can also be traded in advanced
versions of the game
* Cargo Pods - These pods can store goods, energy, and food. They do not consume energy, but they do consume
food for their inherent crews.
* Defense Pods - These Pods can absorb damage from attackers. They consume energy and food.
* Attack Pods - These Pods can be used to attack other ships and colonies. The consume energy and food.
During attacks, the Attack Pods double their energy consumption.
* Ship Pods - This is the basic Pod that represents a ship central hull. For the most part, the function of
a ship is defined by the collection of Pods that comprise it. But every ship must have a central hull. Advanced
versions of the game may grant additional abilities through the hull

### Ships
Ships are comprised of a Ship Pod and a collection of other Pods. The difference between a scout ship and
a colony ship is primarily the constituency of its pods. In the prototype for the game, all ships can jump
the same distance. Later refinements might allow for variance between hulls that give greater or lesser
jump distance in return for other abilities. Ships are a subclass of the Organization class, which contains
logic applicable to both Ships and Colonies.

### Colonies
Colonies are non-mobile resources. Except for the colony established at the game start, all colonies are
a result of ships that have been converted. Once a ship has been converted to a colony, it cannot be changed
back. On the other hand, a colony has an increased ability to produce. So the energy, goods, and crew that it
produces can be used to build new ships. Colonies are a subclass of the Organization class, which contains
logic applicable to both Ships and Colonies.

### Sectors
These represent regions of space in the abstract. Each Sector is comprised of stars, planets, and planetary
systems that have varying ability to develop energy, food, and manufacturing activities. In the prototype,
only one player can have a colony in a given sector. Advanced versions of the game allow for multiple
colonies to be established by any player. That is the same threshold at which the combat system will be
enabled.

Sectors contain a registry of all ships in the area. There is also a registry of colonies. The sum of activities
conducted by all ships and colonies is held against the sector maximum capacity.

### Gameboard
This represents the administrative structures that govern the game. At its core, it is comprised of Sectors.
Initially it is a two-dimensional grid of unlimited size. Sectors are only instantiated when a player interacts
with them, so the data model is that of a sparsely populated grid.

The coordinate system places the origin (0,0) at the upper left. The game premise is that an energy barrier
surrounds the playable area such at all positive Y coordinates, all negative X coordinates are inaccessible.
The "richness" of the sectors increases toward the center and the origin Sector is extraordinarily rich. 
(this concept is under review as possibly being too predictable.)

As sectors are "discovered" their capacity is calculated. A random value for energy, food, and goods production
is determined with higher general values toward the center. The origin sector has hard-coded capacities (although
this is not necessarily known to the players).

All functions that govern the game overall are a part of the Gameboard. That includes the player roster,
the game clock, the end-of-turn logic, and more.

#### Gameboard Components

- Player
- Sector
- SectorMap
- Timer
- MasterRegistry
- MessageRegistry

#### Project Status

190209 - clearly, the UX needs some help to invigorate this project. adding a tangent that includes D3 examples that will find their way into the code base is the next step here. Sector display, and Organization display seem to be the next most useful things to develop.

190208 - add project status section. check README management in git repo. 
