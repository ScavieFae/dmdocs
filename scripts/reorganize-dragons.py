#!/usr/bin/env python3
"""
Reorganize dragon files into grouped folders by dragon type.
"""

import os
import json
import re
from pathlib import Path

dragon_dir = Path(__file__).parent.parent / "bestiary" / "dragon"

# Dragon colors that have age variants
DRAGON_COLORS = ['black', 'blue', 'brass', 'bronze', 'copper', 'gold', 'green', 'red', 'silver', 'white']

# Chromatic vs Metallic for descriptions
CHROMATIC = ['black', 'blue', 'green', 'red', 'white']
METALLIC = ['brass', 'bronze', 'copper', 'gold', 'silver']

# Standalone dragons (no variants)
STANDALONE = ['dragon-turtle', 'half-dragon', 'kobold-warrior', 'pseudodragon', 'wyvern']

def read_frontmatter(filepath):
    """Read frontmatter from MDX file."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract frontmatter between --- markers
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if not match:
        return {}, content

    frontmatter_str = match.group(1)
    body = match.group(2)

    # Parse YAML-ish frontmatter
    data = {}
    current_key = None
    current_list = None

    for line in frontmatter_str.split('\n'):
        if line.startswith('  ') and current_key:
            # Nested content
            if current_list is not None:
                current_list.append(line.strip().lstrip('- '))
            continue

        match = re.match(r'^(\w+):\s*(.*)$', line)
        if match:
            key = match.group(1)
            value = match.group(2).strip()

            if value == '':
                # Could be start of nested object or list
                current_key = key
                current_list = None
            elif value.startswith('"') and value.endswith('"'):
                data[key] = value[1:-1]
                current_key = None
                current_list = None
            elif value.isdigit():
                data[key] = int(value)
                current_key = None
                current_list = None
            else:
                data[key] = value
                current_key = None
                current_list = None

    return data, body

def get_dragon_stats(color):
    """Get stats for all ages of a dragon color."""
    stats = {}
    for age in ['wyrmling', 'young', 'adult', 'ancient']:
        if age == 'wyrmling':
            filename = f"{color}-dragon-wyrmling.mdx"
        else:
            filename = f"{age}-{color}-dragon.mdx"

        filepath = dragon_dir / filename
        if filepath.exists():
            data, _ = read_frontmatter(filepath)
            stats[age] = {
                'ac': data.get('ac', '?'),
                'hp': data.get('hp', {}).get('average', '?') if isinstance(data.get('hp'), dict) else '?',
                'cr': data.get('cr', '?'),
            }
    return stats

def create_dragon_index(color, stats):
    """Create an index page for a dragon type."""
    color_cap = color.capitalize()
    dragon_type = "Chromatic" if color in CHROMATIC else "Metallic"

    # Dragon descriptions
    descriptions = {
        'black': "Black dragons are cruel, cunning predators that lurk in swamps and marshes. Their acid breath and ambush tactics make them feared throughout the land.",
        'blue': "Blue dragons are vain, territorial creatures that claim vast stretches of desert as their domain. They are master manipulators who prefer to talk before fighting.",
        'green': "Green dragons are manipulative schemers who dwell in ancient forests. They delight in corrupting and controlling other creatures.",
        'red': "Red dragons are the most covetous and arrogant of all chromatic dragons. They dwell in mountainous lairs filled with treasure.",
        'white': "White dragons are the most bestial and least intelligent of the chromatic dragons. They hunt in arctic regions with savage ferocity.",
        'brass': "Brass dragons are talkative, friendly creatures who dwell in desert regions. They love conversation and collecting stories.",
        'bronze': "Bronze dragons are coastal dwellers who love to watch ships and sometimes take humanoid form to interact with sailors.",
        'copper': "Copper dragons are pranksters and jokesters who love riddles and games. They make their homes in rocky hills.",
        'gold': "Gold dragons are the wisest and most powerful of the metallic dragons. They dedicate themselves to fighting evil.",
        'silver': "Silver dragons are the most social of metallic dragons, often taking humanoid form to live among people they protect.",
    }

    content = f'''---
title: {color_cap} Dragon
description: {dragon_type} dragon - all life stages from wyrmling to ancient
---

# {color_cap} Dragon

{descriptions.get(color, f"{color_cap} dragons are formidable creatures.")}

## Life Stages

| Age | AC | HP | CR |
|-----|----|----|-----|
'''

    age_labels = {'wyrmling': 'Wyrmling', 'young': 'Young', 'adult': 'Adult', 'ancient': 'Ancient'}
    for age in ['wyrmling', 'young', 'adult', 'ancient']:
        if age in stats:
            s = stats[age]
            content += f"| [{age_labels[age]}]({age}) | {s['ac']} | {s['hp']} | {s['cr']} |\n"

    content += f'''
## Ecology

{color_cap} dragons are {dragon_type.lower()} dragons, known for their distinctive appearance and behavior. Like all true dragons, they grow more powerful with age, progressing through four distinct life stages.
'''

    return content

def move_and_rename_dragon(color, age):
    """Move a dragon file to its new location."""
    if age == 'wyrmling':
        old_name = f"{color}-dragon-wyrmling.mdx"
    else:
        old_name = f"{age}-{color}-dragon.mdx"

    old_path = dragon_dir / old_name
    new_dir = dragon_dir / f"{color}-dragon"
    new_path = new_dir / f"{age}.mdx"

    if old_path.exists():
        new_dir.mkdir(exist_ok=True)

        # Read content and update title
        with open(old_path, 'r') as f:
            content = f.read()

        # Update title to shorter form
        age_cap = age.capitalize()
        content = re.sub(
            r'title: .+\n',
            f'title: {age_cap}\n',
            content
        )

        # Write to new location
        with open(new_path, 'w') as f:
            f.write(content)

        # Remove old file
        old_path.unlink()

        return True
    return False

# Main execution
print("Reorganizing dragons...")

for color in DRAGON_COLORS:
    print(f"\n{color.capitalize()} Dragon:")

    # Get stats before moving
    stats = get_dragon_stats(color)

    # Create folder and move files
    folder = dragon_dir / f"{color}-dragon"
    folder.mkdir(exist_ok=True)

    for age in ['wyrmling', 'young', 'adult', 'ancient']:
        if move_and_rename_dragon(color, age):
            print(f"  Moved {age}")

    # Create index
    index_content = create_dragon_index(color, stats)
    with open(folder / "index.mdx", 'w') as f:
        f.write(index_content)
    print(f"  Created index.mdx")

    # Create meta.json for the folder
    meta = {
        "title": f"{color.capitalize()} Dragon",
        "pages": ["index", "wyrmling", "young", "adult", "ancient"],
        "defaultOpen": False
    }
    with open(folder / "meta.json", 'w') as f:
        json.dump(meta, f, indent=2)

# Update root dragon meta.json
root_meta = {
    "title": "Dragon",
    "pages": (
        [f"{color}-dragon" for color in DRAGON_COLORS] +
        STANDALONE
    ),
    "defaultOpen": False
}
with open(dragon_dir / "meta.json", 'w') as f:
    json.dump(root_meta, f, indent=2)

print("\nDone!")
