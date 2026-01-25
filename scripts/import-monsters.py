#!/usr/bin/env python3
"""
Import monsters from the dndsrd5.2_markdown files and generate MDX files.
"""

import re
import json
from pathlib import Path

# Creature type to folder mapping
CREATURE_TYPES = {
    'aberration': 'aberration',
    'beast': 'beast',
    'celestial': 'celestial',
    'construct': 'construct',
    'dragon': 'dragon',
    'elemental': 'elemental',
    'fey': 'fey',
    'fiend': 'fiend',
    'giant': 'giant',
    'humanoid': 'humanoid',
    'monstrosity': 'monstrosity',
    'ooze': 'ooze',
    'plant': 'plant',
    'undead': 'undead',
}

def slugify(name):
    """Convert monster name to slug for filename."""
    return name.lower().replace("'", "").replace("/", "-").replace(" ", "-").replace(",", "").replace("(", "").replace(")", "")

def parse_speed(speed_line):
    """Parse speed string like '10 ft., Swim 40 ft.'"""
    result = {}
    # Walk speed (first number without prefix)
    walk_match = re.match(r'(\d+)\s*ft\.', speed_line)
    if walk_match:
        result['walk'] = int(walk_match.group(1))
    # Other speeds
    for speed_type in ['Fly', 'Swim', 'Burrow', 'Climb']:
        match = re.search(rf'{speed_type}\s+(\d+)\s*ft\.', speed_line, re.IGNORECASE)
        if match:
            result[speed_type.lower()] = int(match.group(1))
    return result

def parse_hp(hp_line):
    """Parse HP like '150 (20d10 + 40)'"""
    match = re.match(r'(\d+)\s*\(([^)]+)\)', hp_line)
    if match:
        return {
            'average': int(match.group(1)),
            'formula': match.group(2).strip()
        }
    return None

def parse_cr(cr_line):
    """Parse CR like '10 (XP 5,900, or 7,200 in lair)'"""
    cr_match = re.match(r'([\d/]+)', cr_line)
    xp_match = re.search(r'XP\s*([\d,]+)', cr_line)
    cr = cr_match.group(1) if cr_match else None
    xp = int(xp_match.group(1).replace(',', '')) if xp_match else None
    return cr, xp

def parse_abilities(stat_table):
    """Parse the ability score table."""
    abilities = {}
    saves = {}
    # Pattern: | STR | 21 | +5 | +5 |
    for row in stat_table.split('\n'):
        match = re.match(r'\|\s*(STR|DEX|CON|INT|WIS|CHA)\s*\|\s*(\d+)\s*\|\s*([+-]?\d+)\s*\|\s*([+-]?\d+)\s*\|', row)
        if match:
            stat = match.group(1).lower()
            score = int(match.group(2))
            save = int(match.group(4))
            abilities[stat] = score
            # Only include save if it's different from the modifier (has proficiency)
            expected_mod = (score - 10) // 2
            if save != expected_mod:
                saves[stat] = save
    return abilities, saves

def get_creature_type_folder(type_str):
    """Map creature type string to folder name."""
    type_lower = type_str.lower()
    for key in CREATURE_TYPES:
        if key in type_lower:
            return CREATURE_TYPES[key]
    return 'monstrosity'  # Default fallback

def escape_yaml(s):
    """Escape a string for YAML."""
    if not s:
        return s
    if any(c in s for c in [':', '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`', '"', "'"]):
        s = s.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{s}"'
    return s

def parse_monster(text):
    """Parse a single monster text block."""
    lines = text.strip().split('\n')
    if len(lines) < 10:
        return None

    # First line is ## Name
    name_match = re.match(r'^##\s+(.+)$', lines[0])
    if not name_match:
        return None
    name = name_match.group(1).strip()

    # Find the type line (may have blank line after name)
    type_line = None
    for line in lines[1:5]:
        if line.startswith('*') and ',' in line:
            type_line = line
            break

    if not type_line:
        return None

    type_match = re.match(r'^\*(\w+)\s+([^,]+),\s*(.+)\*$', type_line)
    if not type_match:
        return None

    size = type_match.group(1)
    creature_type = type_match.group(2).strip()
    alignment = type_match.group(3).strip()

    monster = {
        'name': name,
        'size': size,
        'creatureType': creature_type,
        'alignment': alignment,
    }

    # Parse the bullet points
    for line in lines:
        if line.startswith('- **Armor Class:**'):
            ac_match = re.search(r'\*\*Armor Class:\*\*\s*(\d+)', line)
            if ac_match:
                monster['ac'] = int(ac_match.group(1))
        elif line.startswith('- **Hit Points:**'):
            hp_match = re.search(r'\*\*Hit Points:\*\*\s*(.+)$', line)
            if hp_match:
                monster['hp'] = parse_hp(hp_match.group(1))
        elif line.startswith('- **Speed:**'):
            speed_match = re.search(r'\*\*Speed:\*\*\s*(.+)$', line)
            if speed_match:
                monster['speed'] = parse_speed(speed_match.group(1))
        elif line.startswith('- **Skills**'):
            skills_match = re.search(r'\*\*Skills\*\*:?\s*(.+)$', line)
            if skills_match:
                monster['skills'] = [s.strip() for s in skills_match.group(1).split(',')]
        elif line.startswith('- **Senses**'):
            senses_match = re.search(r'\*\*Senses\*\*:?\s*(.+)$', line)
            if senses_match:
                monster['senses'] = [s.strip() for s in senses_match.group(1).split(';')]
        elif line.startswith('- **Languages**'):
            lang_match = re.search(r'\*\*Languages\*\*:?\s*(.+)$', line)
            if lang_match:
                langs = lang_match.group(1).strip()
                if langs and langs != '—':
                    monster['languages'] = [l.strip() for l in langs.split(',')]
        elif line.startswith('- **CR**'):
            cr_match = re.search(r'\*\*CR\*\*\s*(.+)$', line)
            if cr_match:
                cr, xp = parse_cr(cr_match.group(1))
                monster['cr'] = cr
                monster['xp'] = xp
        elif line.startswith('- **Immunities**'):
            imm_match = re.search(r'\*\*Immunities\*\*:?\s*(.+)$', line)
            if imm_match:
                monster['immunities'] = [i.strip() for i in imm_match.group(1).split(',')]
        elif line.startswith('- **Resistances**'):
            res_match = re.search(r'\*\*Resistances\*\*:?\s*(.+)$', line)
            if res_match:
                monster['resistances'] = [r.strip() for r in res_match.group(1).split(',')]

    # Parse stat table
    stat_block = '\n'.join(lines)
    table_match = re.search(r'\|STAT\|SCORE\|MOD\|SAVE\|.*?(?=\n\n|\n-|\n###)', stat_block, re.DOTALL)
    if table_match:
        abilities, saves = parse_abilities(table_match.group(0))
        if abilities:
            monster['abilities'] = abilities
        if saves:
            monster['saves'] = saves

    # Extract traits, actions, etc. as the body content
    body_parts = []
    current_section = None

    for line in lines:
        if line.startswith('### Traits'):
            current_section = 'Traits'
            body_parts.append('\n## Traits\n')
        elif line.startswith('### Actions'):
            current_section = 'Actions'
            body_parts.append('\n## Actions\n')
        elif line.startswith('### Bonus Actions'):
            current_section = 'Bonus Actions'
            body_parts.append('\n## Bonus Actions\n')
        elif line.startswith('### Reactions'):
            current_section = 'Reactions'
            body_parts.append('\n## Reactions\n')
        elif line.startswith('### Legendary Actions'):
            current_section = 'Legendary Actions'
            body_parts.append('\n## Legendary Actions\n')
        elif current_section and line.startswith('***'):
            # Trait/action name
            body_parts.append(line)
        elif current_section and line.strip():
            body_parts.append(line)

    monster['body'] = '\n'.join(body_parts).strip()

    return monster

def write_monster_mdx(monster, output_dir, limit_monsters=None):
    """Write a monster to an MDX file."""
    folder = get_creature_type_folder(monster['creatureType'])
    folder_path = output_dir / folder
    folder_path.mkdir(parents=True, exist_ok=True)

    slug = slugify(monster['name'])
    filepath = folder_path / f"{slug}.mdx"

    # Build frontmatter
    lines = ['---']
    lines.append(f"title: {escape_yaml(monster['name'])}")
    lines.append(f"size: {monster['size']}")
    lines.append(f"creatureType: {escape_yaml(monster['creatureType'])}")
    lines.append(f"alignment: {escape_yaml(monster['alignment'])}")

    if monster.get('ac'):
        lines.append(f"ac: {monster['ac']}")

    if monster.get('hp'):
        lines.append('hp:')
        lines.append(f"  average: {monster['hp']['average']}")
        lines.append(f"  formula: {escape_yaml(monster['hp']['formula'])}")

    if monster.get('speed'):
        lines.append('speed:')
        for k, v in monster['speed'].items():
            lines.append(f"  {k}: {v}")

    if monster.get('abilities'):
        lines.append('abilities:')
        for stat in ['str', 'dex', 'con', 'int', 'wis', 'cha']:
            if stat in monster['abilities']:
                lines.append(f"  {stat}: {monster['abilities'][stat]}")

    if monster.get('saves'):
        lines.append('saves:')
        for stat, val in monster['saves'].items():
            lines.append(f"  {stat}: {val}")

    if monster.get('skills'):
        lines.append('skills:')
        for skill in monster['skills']:
            lines.append(f"  - {escape_yaml(skill)}")

    if monster.get('immunities'):
        lines.append('immunities:')
        for imm in monster['immunities']:
            lines.append(f"  - {escape_yaml(imm)}")

    if monster.get('resistances'):
        lines.append('resistances:')
        for res in monster['resistances']:
            lines.append(f"  - {escape_yaml(res)}")

    if monster.get('senses'):
        lines.append('senses:')
        for sense in monster['senses']:
            lines.append(f"  - {escape_yaml(sense)}")

    if monster.get('languages'):
        lines.append('languages:')
        for lang in monster['languages']:
            lines.append(f"  - {escape_yaml(lang)}")

    if monster.get('cr'):
        lines.append(f'cr: "{monster["cr"]}"')

    if monster.get('xp'):
        lines.append(f"xp: {monster['xp']}")

    lines.append('---')
    lines.append('')
    lines.append(monster.get('body', ''))
    lines.append('')

    with open(filepath, 'w') as f:
        f.write('\n'.join(lines))

    return folder, slug

# Main execution
if __name__ == '__main__':
    import sys

    # Parse command line args
    limit = 10  # Default to 10 monsters for testing
    if len(sys.argv) > 1:
        if sys.argv[1] == '--all':
            limit = None
        else:
            limit = int(sys.argv[1])

    # Read monster files
    base_dir = Path(__file__).parent.parent
    monsters_path = base_dir / "pdfs" / "monsters_markdown.md"
    animals_path = base_dir / "pdfs" / "animals_markdown.md"
    output_dir = base_dir / "bestiary"

    with open(monsters_path, 'r') as f:
        monsters_content = f.read()

    with open(animals_path, 'r') as f:
        animals_content = f.read()

    # Split into individual monster blocks
    monster_blocks = re.split(r'\n(?=## [A-Z])', monsters_content)
    animal_blocks = re.split(r'\n(?=## [A-Z])', animals_content)

    all_blocks = monster_blocks + animal_blocks

    # If limiting, pick a diverse set
    if limit:
        # Pick specific monsters for variety
        target_names = [
            'Aboleth',           # Aberration
            'Adult Red Dragon',  # Dragon
            'Beholder',          # Aberration
            'Gelatinous Cube',   # Ooze
            'Ghost',             # Undead
            'Goblin',            # Humanoid/Fey
            'Hill Giant',        # Giant
            'Owlbear',           # Monstrosity
            'Vampire',           # Undead
            'Wolf',              # Beast (animal)
        ]
        selected_blocks = []
        for block in all_blocks:
            first_line = block.strip().split('\n')[0]
            for name in target_names:
                if first_line == f'## {name}':
                    selected_blocks.append(block)
                    print(f"Found: {name}")
                    break
        all_blocks = selected_blocks

    # Clear existing monster files (keep index.mdx)
    for folder in CREATURE_TYPES.values():
        folder_path = output_dir / folder
        if folder_path.exists():
            for f in folder_path.glob('*.mdx'):
                f.unlink()

    # Also remove old placeholder files at root
    for f in output_dir.glob('*.mdx'):
        if f.name != 'index.mdx':
            f.unlink()

    # Parse and write monsters
    by_folder = {}
    count = 0

    for block in all_blocks:
        if limit and count >= limit:
            break

        monster = parse_monster(block)
        if monster:
            folder, slug = write_monster_mdx(monster, output_dir)
            if folder not in by_folder:
                by_folder[folder] = []
            by_folder[folder].append(slug)
            count += 1
            print(f"  {monster['name']} -> {folder}/{slug}.mdx")

    # Write meta.json for each folder
    for folder, slugs in by_folder.items():
        folder_path = output_dir / folder
        meta = {
            'title': folder.capitalize(),
            'pages': sorted(slugs),
            'defaultOpen': False
        }
        with open(folder_path / 'meta.json', 'w') as f:
            json.dump(meta, f, indent=2)

    # Update root meta.json
    root_meta = {
        'title': 'Bestiary',
        'pages': ['index'] + sorted(by_folder.keys())
    }
    with open(output_dir / 'meta.json', 'w') as f:
        json.dump(root_meta, f, indent=2)

    print(f"\nDone! Wrote {count} monsters across {len(by_folder)} creature types.")
