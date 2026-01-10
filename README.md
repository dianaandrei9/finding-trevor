# Finding Trevor

## Game Description

**Finding Trevor** is a 2D platformer game created using **Python** and **Pygame**.  
The player controls **Tabitha**, who must go through different levels, avoid enemies, collect items, and solve simple challenges in order to rescue her familiar, **Trevor**.

The game focuses on movement mechanics, basic combat, exploration, and storytelling through cutscenes.

---

## Repository link
	
	https://github.com/dianaandrei9/finding-trevor.git

---

## Main Features

- Character movement: walking, jumping, wall jumping, wall sliding
- Combat system with basic attacks
- Enemies with simple AI behavior
- Keys, gates, and collectible items
- Inventory system shared across levels
- Health system with death and restart
- Cutscenes for story progression
- Parallax background and animated sprites

---

## Technologies Used

- Python 3
- Pygame
- pytmx for loading Tiled (TMX) maps
- Sprite animations using PNG image sequences

---

## How to Run the Game

### Install required libraries

    pip/pip3 install -r requirements.txt

### Run the game

    python3 -m src.main

---

## Controls

- A / D or Left / Right Arrow – Move left / right
- Space – Jump / Wall jump
- Space when in cutscene skips it
- X – Attack
- ESC – Exit game

---

## Gameplay Notes

- Keys are required to open gates
- Enemies can be avoided or defeated
- Falling into dangerous areas reduces health
- Cutscenes play automatically and can be skipped using player input

---

## Team Members & Contributions

| Name | Contribution |
|------|--------------|
| Andrei Diana | Player movement mechanics, collision handling, level, inventory system, Game Over menu,  End Credits |
| Fasui Catalina-Andreea | Sprite design, animations, parallax backgrounds, cutscenes, UI elements, design, player attack |

---

## Challenges Faced

### Collision Handling
Implementing correct collisions for jumping, falling, wall sliding, and standing on moving platforms required careful separation of horizontal and vertical movement. Special attention was needed to ensure the player remained correctly positioned when interacting with platforms that move, without causing jittering, clipping, or other weird movement behavior.

### Enemy Damage & Group Interaction
Initially, enemies could damage the player every frame they were in contact, which resulted in the player losing too much health instantly. To solve this, we implemented an invincibility timer. After taking damage, the player becomes temporarily invulnerable, preventing repeated damage from enemies.  Visual feedback was also added to indicate when damage is taken. Also beacuse of a mixup between groups, at a point some enemies delt damage and some didnt.

### Player Animations
Managing player animations required correctly switching between different states such as jumping, attacking, falling, and wall sliding. Transitions between these states had to feel smooth ensuring the correct animation played at the right moment based on the player’s actions and movement.

### Cutscenes and Text Timing
Cutscenes required text to appear gradually while staying synchronized with character animations. Timing had to be carefully adjusted so the dialogue would be readable, without advancing too quickly or becoming desynchronized from the visual elements.

### UI Scaling
Parallax background movement needed to be adjusted to support different screen resolutions. Without proper scaling, interactions and visual alignment would not match the player, especially when the window size changed.

### Inventory and Health Between Levels
Inventory items and health information needed to persist when switching between levels. This was handled using a level manager that stores and transfers player data, ensuring continuity in gameplay and preventing progress from being lost during level transitions.