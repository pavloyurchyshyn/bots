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
  - use skill functionality
    - ~~send request to server~~
    - ~~create validators system~~
    - ~~validate on server side~~
    - ~~add card to used cards deck~~
    - change actions order
    - highlight slot for current card use 
    - ~~skip~~
    - ~~cancel skip~~
    - ~~cancel_action~~
    - ~~check is action valid after move~~
    - card use trace predict

    - damage class
    - skill use class
    - validation cache
    - detail wearing
    - ready logic
    - ~~ready warning if bad steps~~
  - rounds and steps GLOBAL clock
  - events react system:
    - unified functions call args 
    - on_damage_event
    - on_deal_damage_event
    - pre_move_event
    - post_move_event

    - pre_skill_use_event
    - on_skill_use_event
    - post_skill_use_event

    - on_stun_event
    - on_silence_event

    - on_death_event

    - on_mech_kill_event
    - on_mech_damage_event
    - on_npc_kill_event
    - on_npc_damage_event

    - on_equip_detail
    - on_effect_apply_event
    - on_effects_end_event
    
  - attrs system
    - cast range attr
    - effects duration
  - create skill, effects etc configs
  
  - mech effects:
    - effects manager
    - stun, 
    - silence, 
    - damage de/increase
    - range de/increase
    - effects triggers
  - mech respawn
  - other entities:
    - missiles
    - smoke
    - clouds
    
  - mech luck
  - pathfinder
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
    
  - world:
    - fragmentation for sectors to speedup logic 
    - areas
    - weather
    - fire
    - fog of war
    - карта висот

  - ~~nickname edit~~
  - ~~player obj~~
  
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
[//]: # (    - draw meches)
    - start details selection
    - sync time

### GAME:
- mech AI
- saves

### Features:
  - check for PICKLE serializing of pools
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
      - rotation
      - different hp stages for tile
      - animations
  - tiles textures system
      - different hp stages for tile

----------------------

## Server
  - ping pong
----------------------

## BUGS:


### OTHER
 - switch target tiles demonstration types
 - custom font
 - render dots in text