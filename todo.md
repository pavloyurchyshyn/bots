python -m cProfile -s tottime launch.py

# **TODO**
First priority:
  - ~~CREATE COMPILER SCRIPTS~~
  - ~~CREATE DETAILS POOL~~
  - ~~create detail pool settings~~
  - ~~mech build~~
  - ~~skills cards~~
  - ~~MAKE USED CARDS POSITIONS~~
  - ~~make cards factory~~
  - ~~REFACTOR separate game logic to a module~~
  - ~~make bridge for online and offline play~~ not complete but anyway
  - use skill functionality
    - send request to server
    - create validators system
    - validate on server side
    - add card to used cards deck
    - skill chain if needed to choose few things
  - detail wearing
  - game stages
----------------------
- Basic
  - ~~run/stop server~~
  - host menu
  - game UI
    - main menu
    - settings
    - map editor
    - game
    
  - nickname edit
  - player obj
  
  - #### SETUP STAGE
    - block game start if no slots selected 
    - ~~map selection~~
    - ~~connected players~~
    - add settings edit
    - edit players number
    - ~~kick players~~
    - ban players
    - lock connections
    - set password
    - ~~edit nickname~~
    - game settings
      - timer
      - details pool
    
  - #### JOIN MENU
    - add nickname edit
  
  - #### GAME stage
    - draw meches
    - start details selection
    - sync time

### GAME:
- mech effects
- mech AI

### Features:
  - custom details
  - custom skills

- Multiplayer
  - ~~connecting~~
  - ~~join~~
  - Setup stage:
    - connection
    - reconnection
  - Game stage:
    - connection
    - reconnection


- Visual 
  - Tile
    - images
      - different hp stages for tile
      - animations
  - tiles textures system
      - different hp stages for tile

----------------------

## Server
  - ping pong
----------------------

## BUGS:
 - map scale

### OTHER
 - switch target tiles demonstration types
 - custom font
 - render dots in text