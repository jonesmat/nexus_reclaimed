# Title ideas
- Project codename: **Nexus Reclaimed**

# Concepts

- An action-rpg where the map moves around the character sitting in the center.
- The world should be built from tiles.
	- Tiles are defined by bmp resource files.
	- Simple tiles with colors that indicate terrain type and connection points.
- The player perform a basic melee skill on start.
- The player can level up and pick from a few basic skills.
- The player has a paper doll with a few slots.
- Enemies of a few basic types should spawn on the tiles.
	- Melee
	- Ranged
- Enemies grant XP when killed.
- Enemies drop basic loot when killed.
- Loot can be equipped to the character's paper doll.
- One tile is generated as the boss tile with a bigger enemy that grants more XP and loot.
- A portal appears that starts a new level.

# Theme

Keywords: Ancient, Mechanical, Fractured, Aether, Veils, Restoration, Nexus

**The Legacy of the Ancients Mechanic:** In this world, the ancient civilization had harnessed a unique power source, let's call it "Aether." However, their overuse and mismanagement of Aether led to a catastrophic event known as the "Aetherial Collapse." This event fractured the world's reality and life force.

1. **Fractured World:** The Aetherial Collapse caused the world to split into various realms or "Veils." These Veils are layers of reality that overlap and interact with each other, creating a world that's physically intact but dimensionally shattered.

2. **Player's Unique Connection:** The player character has a rare ability to perceive and interact with these different Veils. This could be due to a genetic anomaly, a unique bond with Aether, or a mysterious ritual performed at birth.

3. **Death and Resurgence:** Upon death, the player is pulled back to a central Veil or a "Nexus." This Nexus acts as a safe haven and is the only stable part of the world. The reason for the player's return to the Nexus could be a protective spell, a piece of ancient technology, or a mysterious guardian entity. Each death also causes slight alterations in the Veils, as the Aether tries to balance the disrupted energy.

4. **Restoring the Aether:** The player's goal is to understand the Aetherial Collapse and find a way to mend the fractured Veils. This involves collecting fragments of Aether, understanding the ancient technology or magic, and facing the consequences of the ancient civilization's actions.

5. **Power Growth:** As the player gathers Aether fragments and learns more about the ancient civilization, they gradually unlock new abilities and powers. These powers are manifestations of mastering the Aether and learning to navigate the fractured Veils.

6. **Knowledge Retention:** Despite the world shifting with each death, the player retains their knowledge and skills. This represents the growing understanding and mastery of the Aether, and the ability to adapt to the ever-changing world.

**End-game Objective Concept**

The player's ultimate goal is to collect Aether fragments scattered across the fractured Veils to power a device at the Nexus, the world's stable core. These fragments not only enhance the player's abilities but also gradually stabilize the Veils. The culmination of the player's journey is a final confrontation that tests their mastery of the Aether. Overcoming this challenge allows the player to activate the Nexus device, initiating the Aetherial Restoration to realign and merge the fractured Veils, thus healing the world. The game concludes with an epilogue that showcases the restored world and hints at future adventures.

# Tools
- Use ai to generate pixel art.

# Plan

## Milestone - Basic map and movement
- [ ] Build a World from a single Tile.
- [x] Place a Character in the center of the World.
- [x] When a Player clicks in the World, move the Character to the clicked location.
	- [x] The camera should track the player's position.
- [ ] Stop the movement if the Character is at the Tile border.
- [ ] Build the World from multiple Tiles.
	- Tiles connect via connection pixels.
- [ ] Add grass and rock pixels to Tiles.

## Milestone - Single enemy and simple combat
- [ ] Create an Enemy and spawn it it randomly on each Tile.
- [ ] The Enemy should approach the character and stop at arm's reach.
- [ ] Clicking on an Enemy close to the Player's Character will attack it.
- [ ] A Enemy dies after a few hits.
- [ ] The Player's Character is invincible for now.

## Milestone - Looting and equipping
- [ ] When an Enemy dies it should have a high-chance of dropping loot.
	- A simple Enemy-specific loot table should be used.
	- LootItem's have a slot type (head, chest, legs, or boots)
	- LootItem's have a loot class (a-z).
- [ ] If a LootItem drops, render it in the World.
	- [ ] Render as a treasure icon.
	- [ ] On hover, show the type and loot class.
- [ ] Clicking a LootItem near the Player's Character moves it to the Character's inventory.
	- Inventory's are a fixed size (6x10).
	- LootItem's have a fixed size of 1x1 for now.
	- If a LootItem won't fit, drop it.
- [ ] Add a UI button that opens an Inventory UI that show's the Character's inventory.
	- [ ] Render the LootItem with it's type and loot class (i.e. "head-a" for a Top slot with a loot class of "a").
	- For now, LootItem's can't be moved in the Inventory.
	- [ ] Render a Character paper doll.
		- 4 slots; top, left, right, bottom. 
	- [ ] Left-clicking drops the LootItem on the ground.
	- [ ] Right-clicking on a LootItem swaps it with the Character's equipped LootItem in that slot.


## Milestone - Death and restart
- [ ] The Enemy's should now attack the Character when it is in melee range.
- [ ] Add a UI element that shows the Character health.
- [ ] Add a UI element that shows Enemy health.
- [ ] If the Character reaches 0 health, it dies.
- [ ] Show a UI element indicating the character died and a Restart button that creates a fresh character.

## Milestone - Character progression
- [ ] Killing an Enemy grants XP to the Character that killed it.
- [ ] At an XP threshold, the Character levels up.
- [ ] Add a UI button that levels up the character.
	- Reset health to 100%
	- Add more total health.
	- Add more attack damage.
- [ ] Base the Enemy loot table on the Character's level.
	- Higher level, better loot class.

## Milestone - More enemy types
- [ ] Add ranged Enemy.
- [ ] Add weak swarming Enemy.
- [ ] Add slow, big Enemy.

## Milestone - Character skills
- [ ] Grant a basic melee skill as the left-click for new Characters.
	- With a cooldown.
- [ ] At level up, give an option to pick one of two new skills.
- [ ] If a skill has already been selected, level it up.
	- More damage, lower cooldown, more projectiles, etc.

## Milestone - Boss room
- [ ] Use a special boss tile and replace a generated tile away from the Player's Character.
- [ ] Spawn a Boss as a base Enemy type and scale it up.
- [ ] Use a scaled up loot table and drop multiple items (multiple rolls).
- [ ] Grant a large chunk of experience.
- [ ] On boss kill, add a UI button for Goto Next Level.
	- Generate a new World and base the map generation on the Character level (higher level, more tiles and Enemies).

## Milestone - Win condition
- [ ] When the player >= level 10, the next World spawn is the final level.
- [ ] Final level should spawn some special tiles.
- [ ] The final level Boss should be scaled higher or have a new ability.
- [ ] Upon winning, show a congratulation view with the following info:
	- Time played
	- Levels played
- [ ] After the congratulations screen, send the player to a Title screen.
	- Two buttons; Start and Quit.

## Milestone - Improved loot and weapons
- [ ] Add Left arm and right arm slot types to Enemy loot tables.
- [ ] Add Left arm and right arm to Character paper doll.
- [ ] LootItem's can now drop with a suffixes and prefixes that change the character's stats.
	- Health
	- Movement speed
	- Increase Skill damage
	- Increase projectiles.
	- etc.
- [ ] Add on-hover inspection of LootItem's in inventory that list prefix and suffix values.