#!/usr/bin/env python3
"""
Reorganize fiends into Devils and Demons subfolders.
"""

import os
import json
import re
import yaml
from pathlib import Path

fiend_dir = Path(__file__).parent.parent / "bestiary" / "fiend"

# Devils (from Nine Hells) - ordered roughly by CR
DEVILS = [
    ('lemure', 'Lemure', 0),
    ('imp', 'Imp', 1),
    ('bearded-devil', 'Bearded Devil', 3),
    ('barbed-devil', 'Barbed Devil', 5),
    ('chain-devil', 'Chain Devil', 8),
    ('bone-devil', 'Bone Devil', 9),
    ('horned-devil', 'Horned Devil', 11),
    ('erinyes', 'Erinyes', 12),
    ('ice-devil', 'Ice Devil', 14),
    ('pit-fiend', 'Pit Fiend', 20),
]

# Demons (from the Abyss) - ordered roughly by CR
DEMONS = [
    ('dretch', 'Dretch', 0.25),
    ('quasit', 'Quasit', 1),
    ('vrock', 'Vrock', 6),
    ('hezrou', 'Hezrou', 8),
    ('glabrezu', 'Glabrezu', 9),
    ('nalfeshnee', 'Nalfeshnee', 13),
    ('marilith', 'Marilith', 16),
    ('balor', 'Balor', 19),
]

# Standalone fiends (not devils or demons)
STANDALONE = [
    'gnoll-warrior',
    'hell-hound',
    'incubus',
    'lamia',
    'night-hag',
    'nightmare',
    'oni',
    'rakshasa',
    'sahuagin-warrior',
    'spirit-naga',
    'succubus',
]

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

def move_to_subfolder(slug, subfolder):
    """Move a fiend file to a subfolder, simplifying the name."""
    old_path = fiend_dir / f"{slug}.mdx"
    new_dir = fiend_dir / subfolder
    new_dir.mkdir(exist_ok=True)

    # For devils/demons, simplify the filename
    new_slug = slug.replace('-devil', '').replace('-demon', '')
    new_path = new_dir / f"{new_slug}.mdx"

    if old_path.exists():
        # Read and update title
        with open(old_path) as f:
            content = f.read()

        # Move file
        with open(new_path, 'w') as f:
            f.write(content)

        old_path.unlink()
        return new_slug
    return None

# Create Devils folder
print("Devils:")
devils_dir = fiend_dir / "devils"
devils_dir.mkdir(exist_ok=True)

devil_slugs = []
devil_stats = []
for slug, name, cr in DEVILS:
    old_path = fiend_dir / f"{slug}.mdx"
    if old_path.exists():
        stats = get_stats(old_path)
        # Simplify slug for subfolder
        new_slug = slug.replace('-devil', '') if slug.endswith('-devil') else slug
        new_path = devils_dir / f"{new_slug}.mdx"

        with open(old_path) as f:
            content = f.read()
        with open(new_path, 'w') as f:
            f.write(content)
        old_path.unlink()

        devil_slugs.append(new_slug)
        devil_stats.append((name, stats))
        print(f"  Moved {slug} -> devils/{new_slug}")

# Create Devils index
devils_index = '''---
title: Devils
description: Lawful Evil fiends from the Nine Hells
---

# Devils

Devils are Lawful Evil fiends native to the Nine Hells of Baator. They exist in a strict hierarchy, with lesser devils serving greater ones in an infernal bureaucracy of torment and temptation.

## Devil Hierarchy

Devils range from lowly lemures to the mighty pit fiends who command infernal legions.

| Devil | CR | AC | HP |
|-------|-----|----|----|
'''

for name, stats in devil_stats:
    slug = name.lower().replace(' ', '-').replace('-devil', '') if 'devil' in name.lower() else name.lower()
    devils_index += f"| [{name}]({slug}) | {stats['cr']} | {stats['ac']} | {stats['hp']} |\n"

devils_index += '''
## Nature of Devils

Unlike demons, devils are cunning and calculating. They prefer to corrupt mortals through deals and contracts rather than outright violence, though they are fearsome combatants when needed.
'''

with open(devils_dir / "index.mdx", 'w') as f:
    f.write(devils_index)

# Devils meta.json (without index in pages)
devils_meta = {
    "title": "Devils",
    "pages": devil_slugs,
    "defaultOpen": False
}
with open(devils_dir / "meta.json", 'w') as f:
    json.dump(devils_meta, f, indent=2)

print("  Created index.mdx and meta.json")

# Create Demons folder
print("\nDemons:")
demons_dir = fiend_dir / "demons"
demons_dir.mkdir(exist_ok=True)

demon_slugs = []
demon_stats = []
for slug, name, cr in DEMONS:
    old_path = fiend_dir / f"{slug}.mdx"
    if old_path.exists():
        stats = get_stats(old_path)
        new_path = demons_dir / f"{slug}.mdx"

        with open(old_path) as f:
            content = f.read()
        with open(new_path, 'w') as f:
            f.write(content)
        old_path.unlink()

        demon_slugs.append(slug)
        demon_stats.append((name, stats))
        print(f"  Moved {slug} -> demons/{slug}")

# Create Demons index
demons_index = '''---
title: Demons
description: Chaotic Evil fiends from the Abyss
---

# Demons

Demons are Chaotic Evil fiends born from the infinite layers of the Abyss. Unlike the orderly devils, demons are creatures of pure destruction and chaos.

## Demon Types

From the weakest dretch to the terrifying balor, demons embody chaos and destruction.

| Demon | CR | AC | HP |
|-------|-----|----|----|
'''

for name, stats in demon_stats:
    slug = name.lower()
    demons_index += f"| [{name}]({slug}) | {stats['cr']} | {stats['ac']} | {stats['hp']} |\n"

demons_index += '''
## Nature of Demons

Demons exist only to destroy. They have no society, no loyalty, and no purpose beyond spreading chaos and ruin. Only the strongest demons command others, and only through raw power and fear.
'''

with open(demons_dir / "index.mdx", 'w') as f:
    f.write(demons_index)

# Demons meta.json (without index in pages)
demons_meta = {
    "title": "Demons",
    "pages": demon_slugs,
    "defaultOpen": False
}
with open(demons_dir / "meta.json", 'w') as f:
    json.dump(demons_meta, f, indent=2)

print("  Created index.mdx and meta.json")

# Update root fiend meta.json
print("\nUpdating fiend meta.json...")
root_meta = {
    "title": "Fiend",
    "pages": ["devils", "demons"] + STANDALONE,
    "defaultOpen": False
}
with open(fiend_dir / "meta.json", 'w') as f:
    json.dump(root_meta, f, indent=2)

print("\nDone!")
