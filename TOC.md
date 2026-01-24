# SRD 5.2.1 Table of Contents

Extracted from PDF. This defines our site hierarchy.

## Top-Level Sections

1. **Legal Information** (p. 1)

2. **Playing the Game** (p. 5)
   - Rhythm of Play (5)
   - The Six Abilities (5)
   - D20 Tests (6)
     - Ability Checks (6)
     - Saving Throws (7)
     - Attack Rolls (7)
     - Advantage/Disadvantage (7)
   - Proficiency (8)
   - Actions (9)
     - Bonus Actions (10)
     - Reactions (10)
   - Social Interaction (10)
   - Exploration (11)
     - Vision and Light (11)
     - Hiding (11)
     - Interacting with Objects (11)
     - Hazards (12)
     - Travel (12)
   - Combat (13)
     - The Order of Combat (13)
     - Movement and Position (14)
     - Making an Attack (14)
     - Ranged Attacks (15)
     - Melee Attacks (15)
     - Mounted Combat (15)
     - Underwater Combat (16)
   - Damage and Healing (16)
     - Hit Points (16)
     - Damage Rolls (16)
     - Critical Hits (16)
     - Saving Throws and Damage (16)
     - Damage Types (16)
     - Resistance and Vulnerability (17)
     - Immunity (17)
     - Healing (17)
     - Dropping to 0 Hit Points (17)
     - Temporary Hit Points (18)

3. **Character Creation** (p. 19)
   - Choose a Character Sheet (19)
   - Create Your Character (19)
   - Level Advancement (23)
   - Starting at Higher Levels (24)
   - Multiclassing (24)
   - Trinkets (26)

4. **Classes** (p. 28)
   - Barbarian (28)
     - Subclass: Path of the Berserker (30)
   - Bard (31)
     - Bard Spell List (33)
     - Subclass: College of Lore (35)
   - Cleric (36)
     - Cleric Spell List (38)
     - Subclass: Life Domain (40)
   - Druid (41)
     - Druid Spell List (44)
     - Subclass: Circle of the Land (46)
   - Fighter (47)
     - Subclass: Champion (49)
   - Monk (49)
     - Subclass: Warrior of the Open Hand (52)
   - Paladin (53)
     - Paladin Spell List (55)
     - Subclass: Oath of Devotion (56)
   - Ranger (57)
     - Ranger Spell List (60)
     - Subclass: Hunter (61)
   - Rogue (61)
     - Subclass: Thief (64)
   - Sorcerer (64)
     - Metamagic Options (66)
     - Sorcerer Spell List (67)
     - Subclass: Draconic Sorcery (69)
   - Warlock (70)
     - Eldritch Invocation Options (72)
     - Warlock Spell List (74)
     - Subclass: Fiend Patron (76)
   - Wizard (77)
     - Wizard Spell List (79)
     - Subclass: Evoker (82)

5. **Character Origins** (p. 83)
   - Character Backgrounds (83)
     - Acolyte (83)
     - Criminal (83)
     - Sage (83)
     - Soldier (83)
   - Character Species (83)
     - Dragonborn (84)
     - Dwarf (84)
     - Elf (84)
     - Gnome (85)
     - Goliath (85)
     - Halfling (86)
     - Human (86)
     - Orc (86)
     - Tiefling (86)

6. **Feats** (p. 87)
   - Feat Descriptions (87)
     - Origin Feats (87)
     - General Feats (87)
     - Fighting Style Feats (87)
     - Epic Boon Feats (88)

7. **Equipment** (p. 89)
   - Coins (89)
   - Weapons (89)
     - Properties (89)
     - Mastery Properties (90)
   - Armor (92)
   - Tools (93)
   - Adventuring Gear (94)
   - Mounts and Vehicles (100)
   - Lifestyle Expenses (101)
   - Food, Drink, and Lodging (101)
   - Hirelings (102)
   - Spellcasting Services (102)
   - Magic Item Services (102)
   - Crafting Nonmagical Items (103)
   - Brewing Potions of Healing (103)
   - Scribing Spell Scrolls (103)

8. **Spells** (p. 104)
   - Gaining Spells (104)
   - Casting Spells (104)
   - Spell Descriptions (107)
   - [Individual spells A-Z]

9. **Rules Glossary** (p. 176)
   - [Alphabetical rules terms]

10. **Gameplay Toolbox** (p. 192)
    - Travel Pace (192)
    - Creating a Background (192)
    - Curses and Magical Contagions (193)
    - Environmental Effects (195)
    - Fear and Mental Stress (196)
    - Poison (197)
    - Traps (199)
    - Combat Encounters (202)

11. **Magic Items** (p. 204)
    - Magic Item Categories (204)
    - Magic Item Rarity (205)
    - Activating a Magic Item (206)
    - "The Next Dawn" (206)
    - Cursed Items (206)
    - Magic Item Resilience (206)
    - Crafting Magic Items (206)
    - Sentient Magic Items (207)
    - Magic Items A–Z (209)

12. **Monsters** (p. 254)
    - Stat Block Overview (254)
    - Parts of a Stat Block (254)
    - Running a Monster (255)
    - Monsters A–Z (258)

13. **Animals** (p. 344)
    - [Beast stat blocks]

---

## Proposed Site Structure

```
/docs
├── index                    # Welcome + overview
├── legal                    # CC-BY-4.0 attribution
├── playing-the-game/
│   ├── index               # Overview
│   ├── abilities           # The Six Abilities
│   ├── d20-tests           # Checks, saves, attacks
│   ├── proficiency
│   ├── actions
│   ├── exploration
│   ├── combat
│   └── damage-and-healing
├── character-creation/
│   ├── index
│   ├── level-advancement
│   ├── multiclassing
│   └── trinkets
├── classes/
│   ├── index               # Class comparison table
│   ├── barbarian
│   ├── bard
│   ├── cleric
│   ├── druid
│   ├── fighter
│   ├── monk
│   ├── paladin
│   ├── ranger
│   ├── rogue
│   ├── sorcerer
│   ├── warlock
│   └── wizard
├── origins/
│   ├── backgrounds/
│   │   └── [each background]
│   └── species/
│       └── [each species]
├── feats/
│   ├── index               # Feat list with categories
│   └── [individual feats or by category]
├── equipment/
│   ├── index
│   ├── weapons
│   ├── armor
│   ├── tools
│   ├── adventuring-gear
│   └── services
├── spells/
│   ├── index               # Spell list with filters
│   └── [individual spells A-Z]
├── rules-glossary/
│   └── index               # Alphabetical terms
├── toolbox/
│   ├── index
│   ├── travel
│   ├── hazards
│   ├── traps
│   └── encounters
├── magic-items/
│   ├── index               # Item list with filters
│   └── [individual items A-Z]
└── monsters/
    ├── index               # Monster list with filters
    ├── stat-blocks         # How to read stat blocks
    └── [individual monsters A-Z]
```
