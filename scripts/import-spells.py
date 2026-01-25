#!/usr/bin/env python3
"""
Import spells from the dndsrd5.2_markdown spells file and generate MDX files.
"""

import re
import os
import json
from pathlib import Path

# Read the markdown file
spells_path = Path(__file__).parent.parent / "pdfs" / "spells_markdown.md"
with open(spells_path, 'r') as f:
    content = f.read()

# Find where spell descriptions start (after "## Spell Descriptions")
spell_section_match = re.search(r'## Spell Descriptions\s+### [A-Z] Spells\s+', content)
if not spell_section_match:
    print("Could not find spell descriptions section")
    exit(1)

spell_content = content[spell_section_match.end():]

# Pattern to match spell headers
# #### Spell Name or #### **Spell Name**
# *Level X School (Classes)* or *School Cantrip (Classes)*
spell_pattern = re.compile(
    r'^#### \*?\*?([^\n*]+)\*?\*?\s*\n\n'
    r'\*(?:Level (\d) )?(\w+)(?: Cantrip)? \(([^)]+)\)\*\s*\n\n'
    r'\*\*Casting Time:\*\* ([^\n]+)\s*\n\n'
    r'\*\*Range:\*\* ([^\n]+)\s*\n\n'
    r'\*\*Components:\*\* ([^\n]+)\s*\n\n'
    r'\*\*Duration:\*\* ([^\n]+)\s*\n\n'
    r'(.*?)(?=\n#### |\n### [A-Z] Spells|\Z)',
    re.MULTILINE | re.DOTALL
)

def slugify(name):
    """Convert spell name to slug for filename."""
    return name.lower().replace("'", "").replace("/", "-").replace(" ", "-").replace(":", "")

def parse_components(comp_str):
    """Parse component string like 'V, S, M (a tiny ball)'"""
    result = {'verbal': False, 'somatic': False}
    if 'V' in comp_str:
        result['verbal'] = True
    if 'S' in comp_str:
        result['somatic'] = True
    # Check for material component
    m_match = re.search(r'M \(([^)]+)\)', comp_str)
    if m_match:
        result['material'] = m_match.group(1)
    elif 'M' in comp_str.split(','):
        result['material'] = 'required'
    return result

def escape_yaml_string(s):
    """Escape a string for YAML if needed."""
    if not s:
        return s
    # If contains special chars, quote it
    if any(c in s for c in [':', '#', '{', '}', '[', ']', ',', '&', '*', '?', '|', '-', '<', '>', '=', '!', '%', '@', '`', '"', "'"]):
        # Use double quotes and escape internal quotes
        s = s.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{s}"'
    return s

# Schools mapping for folder names
SCHOOLS = {
    'Abjuration': 'abjuration',
    'Conjuration': 'conjuration',
    'Divination': 'divination',
    'Enchantment': 'enchantment',
    'Evocation': 'evocation',
    'Illusion': 'illusion',
    'Necromancy': 'necromancy',
    'Transmutation': 'transmutation',
}

# Find all spells
spells = []
for match in spell_pattern.finditer(spell_content):
    name = match.group(1).strip()
    level_str = match.group(2)
    level = int(level_str) if level_str else 0  # Cantrip = 0
    school = match.group(3).strip()
    classes_str = match.group(4)
    casting_time = match.group(5).strip()
    range_val = match.group(6).strip()
    components_str = match.group(7).strip()
    duration = match.group(8).strip()
    description = match.group(9).strip()

    # Parse classes
    classes = [c.strip() for c in classes_str.split(',')]

    # Parse components
    components = parse_components(components_str)

    # Check for ritual
    ritual = 'Ritual' in casting_time
    if ritual:
        casting_time = casting_time.replace(' or Ritual', '').strip()

    # Check for concentration
    concentration = 'Concentration' in duration

    # Extract higher level text if present
    higher_level = None
    higher_match = re.search(r'\*\*_?Using a Higher-Level Spell Slot\.?_?\*\*\.?\s*(.+?)(?:\n\n|\Z)', description, re.DOTALL)
    cantrip_match = re.search(r'\*\*_?Cantrip Upgrade\.?_?\*\*\.?\s*(.+?)(?:\n\n|\Z)', description, re.DOTALL)

    if higher_match:
        higher_level = higher_match.group(1).strip()
        description = description[:higher_match.start()].strip()
    elif cantrip_match:
        higher_level = cantrip_match.group(1).strip()
        description = description[:cantrip_match.start()].strip()

    spell = {
        'name': name,
        'level': level,
        'school': school,
        'classes': classes,
        'castingTime': casting_time,
        'range': range_val,
        'components': components,
        'duration': duration,
        'concentration': concentration,
        'ritual': ritual,
        'description': description,
    }
    if higher_level:
        spell['higherLevel'] = higher_level

    spells.append(spell)

print(f"Parsed {len(spells)} spells")

# Group by school
by_school = {}
for spell in spells:
    school_lower = spell['school'].lower()
    if school_lower not in by_school:
        by_school[school_lower] = []
    by_school[school_lower].append(spell)

# Output directory
output_dir = Path(__file__).parent.parent / "spellbook"

# Clear existing spell files (but keep index.mdx and meta.json at root)
for school_dir in output_dir.iterdir():
    if school_dir.is_dir():
        for f in school_dir.glob('*.mdx'):
            f.unlink()
        print(f"Cleared {school_dir.name}/")

# Write MDX files for each school
for school, school_spells in by_school.items():
    school_dir = output_dir / school
    school_dir.mkdir(parents=True, exist_ok=True)

    # Sort spells alphabetically
    school_spells.sort(key=lambda s: s['name'])

    spell_slugs = []

    for spell in school_spells:
        slug = slugify(spell['name'])
        spell_slugs.append(slug)
        filename = slug + '.mdx'
        filepath = school_dir / filename

        # Build YAML frontmatter manually for control
        lines = ['---']
        lines.append(f"title: {escape_yaml_string(spell['name'])}")
        lines.append(f"level: {spell['level']}")
        lines.append(f"school: {spell['school']}")
        lines.append(f"castingTime: {escape_yaml_string(spell['castingTime'])}")
        lines.append(f"range: {escape_yaml_string(spell['range'])}")
        lines.append('components:')
        lines.append(f"  verbal: {str(spell['components']['verbal']).lower()}")
        lines.append(f"  somatic: {str(spell['components']['somatic']).lower()}")
        if 'material' in spell['components']:
            lines.append(f"  material: {escape_yaml_string(spell['components']['material'])}")
        lines.append(f"duration: {escape_yaml_string(spell['duration'])}")
        lines.append(f"concentration: {str(spell['concentration']).lower()}")
        lines.append(f"ritual: {str(spell['ritual']).lower()}")
        lines.append('classes:')
        for cls in spell['classes']:
            lines.append(f"  - {cls}")
        if spell.get('higherLevel'):
            lines.append(f"higherLevel: {escape_yaml_string(spell['higherLevel'])}")
        lines.append('---')
        lines.append('')
        lines.append(spell['description'])
        lines.append('')

        with open(filepath, 'w') as f:
            f.write('\n'.join(lines))

    # Write meta.json for this school
    meta_path = school_dir / 'meta.json'
    meta = {
        'title': school.capitalize(),
        'pages': spell_slugs
    }
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)

    print(f"  {school}: {len(school_spells)} spells")

print(f"\nDone! Wrote {len(spells)} spell files across {len(by_school)} schools.")
