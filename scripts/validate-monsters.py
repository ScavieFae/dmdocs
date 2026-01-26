#!/usr/bin/env python3
"""Validate monster frontmatter against SRD extracted text."""

import os
import re
import yaml
from pathlib import Path

# Load SRD monster data
SRD_FILE = "pdfs/DND-SRD-5.2.1-CC - updated.docx.txt"

def parse_srd_monsters():
    """Extract monster data from SRD text."""
    monsters = {}

    with open(SRD_FILE, 'r') as f:
        content = f.read()

    # Find monster entries (starting at line ~18678)
    # Pattern: "      N. Monster Name" followed by stat block
    pattern = r'      \d+\. ([A-Z][^\n]+)\n([^\n]+(?:Beast|Dragon|Fiend|Celestial|Undead|Construct|Elemental|Fey|Giant|Humanoid|Monstrosity|Ooze|Plant|Aberration)[^\n]*)\nArmor Class: (\d+)[^\n]*\nHit Points:(\d+)[^\n]*\nSpeed: ([^\n]+)'

    matches = re.findall(pattern, content, re.IGNORECASE)

    for match in matches:
        name, type_line, ac, hp, speed = match
        name = name.strip()

        # Parse size and type
        size_match = re.match(r'(Tiny|Small|Medium|Large|Huge|Gargantuan)', type_line)
        size = size_match.group(1) if size_match else None

        # Parse CR (appears later in block)
        cr_pattern = rf'{re.escape(name)}.*?CR: ([0-9/]+)'
        cr_match = re.search(cr_pattern, content[content.find(name):content.find(name)+2000], re.DOTALL)
        cr = cr_match.group(1) if cr_match else None

        monsters[name] = {
            'size': size,
            'ac': int(ac),
            'hp': int(hp),
            'cr': cr
        }

    return monsters

def parse_mdx_monster(filepath):
    """Extract frontmatter from monster MDX file."""
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract YAML frontmatter
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            yaml_content = content[3:end]
            try:
                data = yaml.safe_load(yaml_content)
                return data
            except:
                return None
    return None

def get_monster_name_from_path(filepath):
    """Convert filepath to SRD monster name."""
    # This mirrors the logic in list-bestiary.py
    rel = str(filepath).replace('bestiary/', '').replace('.mdx', '')
    parts = rel.split('/')

    if len(parts) == 2:
        name = parts[1].replace('-', ' ').title()
    elif len(parts) == 3:
        creature_type, subfolder, filename = parts

        if creature_type == 'dragon' and subfolder.endswith('-dragon'):
            color = subfolder.replace('-dragon', '').replace('-', ' ').title()
            age = filename.replace('-', ' ').title()
            if age == 'Wyrmling':
                name = f"{color} Dragon Wyrmling"
            else:
                name = f"{age} {color} Dragon"
        elif subfolder == 'devils':
            if filename in ['pit-fiend', 'erinyes', 'lemure', 'imp']:
                name = filename.replace('-', ' ').title()
            else:
                name = f"{filename.replace('-', ' ').title()} Devil"
        elif subfolder == 'goblins':
            name = f"Goblin {filename.replace('-', ' ').title()}"
        elif subfolder == 'hobgoblins':
            name = f"Hobgoblin {filename.replace('-', ' ').title()}"
        elif subfolder == 'bugbears':
            name = f"Bugbear {filename.replace('-', ' ').title()}"
        elif subfolder == 'sphinxes':
            name = f"Sphinx of {filename.replace('-', ' ').title()}"
        else:
            name = filename.replace('-', ' ').title()
    else:
        name = parts[-1].replace('-', ' ').title()

    # Handle special cases
    special = {
        'Saber Toothed Tiger': 'Saber-Toothed Tiger',
        'Will O Wisp': "Will-o'-Wisp",
        'Half Dragon': 'Half-Dragon',
    }
    return special.get(name, name)

def main():
    # Sample a subset of monsters for validation
    sample_monsters = [
        'bestiary/aberration/aboleth.mdx',
        'bestiary/beast/wolf.mdx',
        'bestiary/dragon/red-dragon/adult.mdx',
        'bestiary/fiend/devils/pit-fiend.mdx',
        'bestiary/undead/vampire.mdx',
        'bestiary/giant/frost-giant.mdx',
        'bestiary/construct/iron-golem.mdx',
        'bestiary/celestial/solar.mdx',
        'bestiary/elemental/elementals/fire-elemental.mdx',
        'bestiary/monstrosity/tarrasque.mdx',
    ]

    print("Sampling 10 monsters for metadata validation...\n")

    issues = []
    for filepath in sample_monsters:
        if not os.path.exists(filepath):
            print(f"  SKIP: {filepath} (not found)")
            continue

        mdx_data = parse_mdx_monster(filepath)
        if not mdx_data:
            print(f"  SKIP: {filepath} (parse error)")
            continue

        name = get_monster_name_from_path(filepath)
        print(f"  {name}:")
        print(f"    Size: {mdx_data.get('size')}")
        print(f"    AC: {mdx_data.get('ac')}")
        print(f"    HP: {mdx_data.get('hp', {}).get('average') if isinstance(mdx_data.get('hp'), dict) else mdx_data.get('hp')}")
        print(f"    CR: {mdx_data.get('cr')}")
        print()

    print("Manual spot-check against SRD recommended for these samples.")

if __name__ == '__main__':
    main()
