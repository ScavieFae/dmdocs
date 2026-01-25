#!/usr/bin/env python3
"""
Reorganize Goblins, Hobgoblins, Bugbears, Elementals, Mephits, and Golems.
"""

import json
import re
import yaml
from pathlib import Path

bestiary_dir = Path(__file__).parent.parent / "bestiary"

def get_stats(filepath):
    """Get AC, HP, CR from a monster file."""
    with open(filepath) as f:
        content = f.read()
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        data = yaml.safe_load(match.group(1))
        return {
            'ac': data.get('ac', '?'),
            'hp': data.get('hp', {}).get('average', '?'),
            'cr': data.get('cr', '?'),
        }
    return {'ac': '?', 'hp': '?', 'cr': '?'}

def move_file(src_path, dest_path):
    """Move a file, creating parent dirs if needed."""
    dest_path.parent.mkdir(exist_ok=True)
    if src_path.exists():
        with open(src_path) as f:
            content = f.read()
        with open(dest_path, 'w') as f:
            f.write(content)
        src_path.unlink()
        return True
    return False

def create_group(base_dir, group_name, title, description, monsters, simplify_prefix=None):
    """Create a grouped folder with index and meta.json."""
    group_dir = base_dir / group_name
    group_dir.mkdir(exist_ok=True)

    slugs = []
    stats_list = []

    for old_slug, display_name in monsters:
        old_path = base_dir / f"{old_slug}.mdx"
        # Simplify slug by removing prefix
        if simplify_prefix and old_slug.startswith(simplify_prefix):
            new_slug = old_slug[len(simplify_prefix):]
        else:
            new_slug = old_slug
        new_path = group_dir / f"{new_slug}.mdx"

        if move_file(old_path, new_path):
            slugs.append(new_slug)
            stats_list.append((display_name, new_slug, get_stats(new_path)))
            print(f"  Moved {old_slug} -> {group_name}/{new_slug}")

    # Create index
    index_content = f'''---
title: {title}
description: {description}
---

# {title}

{description}

## Variants

| Name | CR | AC | HP |
|------|-----|----|----|
'''
    for name, slug, stats in stats_list:
        index_content += f"| [{name}]({slug}) | {stats['cr']} | {stats['ac']} | {stats['hp']} |\n"

    with open(group_dir / "index.mdx", 'w') as f:
        f.write(index_content)

    # Create meta.json (without index to avoid duplication)
    meta = {
        "title": title,
        "pages": slugs,
        "defaultOpen": False
    }
    with open(group_dir / "meta.json", 'w') as f:
        json.dump(meta, f, indent=2)

    print(f"  Created index.mdx and meta.json")
    return group_name

# ============ FEY ============
print("=== Reorganizing Fey ===\n")
fey_dir = bestiary_dir / "fey"

print("Goblins:")
create_group(fey_dir, "goblins", "Goblins",
    "Small, cunning fey creatures that live in caves and ruins",
    [
        ("goblin-minion", "Minion"),
        ("goblin-warrior", "Warrior"),
        ("goblin-boss", "Boss"),
    ],
    simplify_prefix="goblin-"
)

print("\nHobgoblins:")
create_group(fey_dir, "hobgoblins", "Hobgoblins",
    "Disciplined, militaristic fey that organize in legions",
    [
        ("hobgoblin-warrior", "Warrior"),
        ("hobgoblin-captain", "Captain"),
    ],
    simplify_prefix="hobgoblin-"
)

print("\nBugbears:")
create_group(fey_dir, "bugbears", "Bugbears",
    "Large, stealthy fey that delight in ambush and intimidation",
    [
        ("bugbear-warrior", "Warrior"),
        ("bugbear-stalker", "Stalker"),
    ],
    simplify_prefix="bugbear-"
)

# Update fey meta.json
fey_standalone = ["blink-dog", "centaur-trooper", "dryad", "green-hag", "satyr", "sea-hag", "sprite", "worg"]
fey_meta = {
    "title": "Fey",
    "pages": ["index", "goblins", "hobgoblins", "bugbears"] + fey_standalone,
    "defaultOpen": False
}
with open(fey_dir / "meta.json", 'w') as f:
    json.dump(fey_meta, f, indent=2)

# Create fey index
fey_index = '''---
title: Fey Creatures
description: Magical beings tied to nature and the Feywild
---

# Fey

Fey are magical creatures tied to the forces of nature and the Feywild. They range from mischievous sprites to organized goblinoid armies.

## Goblinoids

In the 2024 rules, goblins, hobgoblins, and bugbears are fey creatures with ties to the Feywild.

| Type | Description |
|------|-------------|
| [Goblins](goblins) | Small, cunning raiders |
| [Hobgoblins](hobgoblins) | Disciplined military forces |
| [Bugbears](bugbears) | Stealthy brutes |

## Other Fey

| Creature | CR | Description |
|----------|-----|-------------|
| [Blink Dog](blink-dog) | 1/4 | Teleporting canines |
| [Centaur Trooper](centaur-trooper) | 2 | Horse-bodied warriors |
| [Dryad](dryad) | 1 | Tree-bound nature spirits |
| [Green Hag](green-hag) | 3 | Swamp-dwelling trickster |
| [Sea Hag](sea-hag) | 2 | Ocean-dwelling hag |
| [Satyr](satyr) | 1/2 | Hedonistic goat-legged fey |
| [Sprite](sprite) | 1/4 | Tiny woodland defenders |
| [Worg](worg) | 1/2 | Evil wolf mounts |
'''
with open(fey_dir / "index.mdx", 'w') as f:
    f.write(fey_index)

# ============ ELEMENTAL ============
print("\n=== Reorganizing Elemental ===\n")
elem_dir = bestiary_dir / "elemental"

print("Elementals:")
create_group(elem_dir, "elementals", "Elementals",
    "Pure manifestations of the four elemental forces",
    [
        ("air-elemental", "Air Elemental"),
        ("earth-elemental", "Earth Elemental"),
        ("fire-elemental", "Fire Elemental"),
        ("water-elemental", "Water Elemental"),
    ],
    simplify_prefix=None  # Keep full names
)

print("\nMephits:")
create_group(elem_dir, "mephits", "Mephits",
    "Small, impish elementals that embody mixed elemental forces",
    [
        ("dust-mephit", "Dust Mephit"),
        ("ice-mephit", "Ice Mephit"),
        ("magma-mephit", "Magma Mephit"),
        ("steam-mephit", "Steam Mephit"),
    ],
    simplify_prefix=None
)

# Update elemental meta.json
elem_standalone = ["azer-sentinel", "djinni", "efreeti", "gargoyle", "invisible-stalker", "magmin", "merfolk-skirmisher", "salamander", "xorn"]
elem_meta = {
    "title": "Elemental",
    "pages": ["index", "elementals", "mephits"] + elem_standalone,
    "defaultOpen": False
}
with open(elem_dir / "meta.json", 'w') as f:
    json.dump(elem_meta, f, indent=2)

# Create elemental index
elem_index = '''---
title: Elemental Creatures
description: Beings of pure elemental essence from the Inner Planes
---

# Elementals

Elemental creatures hail from the Inner Planes, embodying the raw forces of air, earth, fire, and water.

## Pure Elementals

| Type | Description |
|------|-------------|
| [Elementals](elementals) | The four classic elemental forms |
| [Mephits](mephits) | Small, impish elemental creatures |

## Genies

| Creature | CR | Element |
|----------|-----|---------|
| [Djinni](djinni) | 11 | Air |
| [Efreeti](efreeti) | 11 | Fire |

## Other Elementals

| Creature | CR | Description |
|----------|-----|-------------|
| [Azer Sentinel](azer-sentinel) | 2 | Fire-forged dwarves |
| [Gargoyle](gargoyle) | 2 | Stone guardians |
| [Invisible Stalker](invisible-stalker) | 6 | Summoned air hunters |
| [Magmin](magmin) | 1/2 | Small fire creatures |
| [Merfolk Skirmisher](merfolk-skirmisher) | 1/8 | Aquatic humanoids |
| [Salamander](salamander) | 5 | Serpentine fire beings |
| [Xorn](xorn) | 5 | Three-armed earth eaters |
'''
with open(elem_dir / "index.mdx", 'w') as f:
    f.write(elem_index)

# ============ CONSTRUCT ============
print("\n=== Reorganizing Construct ===\n")
const_dir = bestiary_dir / "construct"

print("Golems:")
create_group(const_dir, "golems", "Golems",
    "Magically animated constructs built to serve their creators",
    [
        ("clay-golem", "Clay Golem"),
        ("flesh-golem", "Flesh Golem"),
        ("stone-golem", "Stone Golem"),
        ("iron-golem", "Iron Golem"),
    ],
    simplify_prefix=None
)

# Update construct meta.json
const_standalone = ["animated-armor", "animated-flying-sword", "animated-rug-of-smothering", "gorgon", "homunculus", "shield-guardian"]
const_meta = {
    "title": "Construct",
    "pages": ["index", "golems"] + const_standalone,
    "defaultOpen": False
}
with open(const_dir / "meta.json", 'w') as f:
    json.dump(const_meta, f, indent=2)

# Create construct index
const_index = '''---
title: Constructs
description: Magically created creatures and automatons
---

# Constructs

Constructs are magically created creatures, from simple animated objects to powerful golems.

## Golems

[Golems](golems) are powerful constructs crafted from specific materials, each with unique properties.

| Golem | CR | Special Properties |
|-------|-----|-------------------|
| Clay | 9 | Haste, acid/fire immunity |
| Flesh | 5 | Lightning healing, berserk |
| Stone | 10 | Slow, magic resistance |
| Iron | 16 | Poison breath, fire absorption |

## Animated Objects

| Creature | CR | Description |
|----------|-----|-------------|
| [Animated Armor](animated-armor) | 1 | Suits of armor given motion |
| [Animated Flying Sword](animated-flying-sword) | 1/4 | Blades that fight on their own |
| [Animated Rug of Smothering](animated-rug-of-smothering) | 2 | Carpets that engulf prey |

## Other Constructs

| Creature | CR | Description |
|----------|-----|-------------|
| [Gorgon](gorgon) | 5 | Iron bull with petrifying breath |
| [Homunculus](homunculus) | 0 | Tiny servant created by wizards |
| [Shield Guardian](shield-guardian) | 7 | Protective construct bound to an amulet |
'''
with open(const_dir / "index.mdx", 'w') as f:
    f.write(const_index)

print("\nDone!")
