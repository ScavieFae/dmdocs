#!/usr/bin/env python3
"""
Extract spells from SRD 5.2.1 text file and generate MDX files.
"""

import re
import os
import yaml
from pathlib import Path

# Read the SRD text
srd_path = Path(__file__).parent.parent / "pdfs" / "SRD_5.2.1.txt"
with open(srd_path, 'r') as f:
    lines = f.readlines()

# Spell section roughly lines 6468-11238
spell_lines = lines[6467:11240]
spell_text = ''.join(spell_lines)

# Pattern to match spell headers
# "Level X School (Classes)" or "School Cantrip (Classes)"
spell_header_pattern = re.compile(
    r'^      ([A-Z][a-zA-Z\'\-/ ]+)\n\s+(Level (\d) (\w+)|(\w+) Cantrip) \(([^)]+)\)',
    re.MULTILINE
)

# Schools mapping
SCHOOLS = ['Abjuration', 'Conjuration', 'Divination', 'Enchantment',
           'Evocation', 'Illusion', 'Necromancy', 'Transmutation']

def slugify(name):
    """Convert spell name to slug for filename."""
    return name.lower().replace("'", "").replace("/", "-").replace(" ", "-")

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
    elif 'M' in comp_str:
        result['material'] = 'required'
    return result

def extract_spell_data(text_block):
    """Extract spell data from a text block."""
    lines = text_block.strip().split('\n')

    # Find the header line (Level X School or School Cantrip)
    header_idx = None
    for i, line in enumerate(lines):
        if re.match(r'\s*(Level \d \w+|(?:Abjuration|Conjuration|Divination|Enchantment|Evocation|Illusion|Necromancy|Transmutation) Cantrip)', line.strip()):
            header_idx = i
            break

    if header_idx is None:
        return None

    # Parse header
    header = lines[header_idx].strip()

    # Determine if cantrip or leveled spell
    cantrip_match = re.match(r'(\w+) Cantrip \(([^)]+)\)', header)
    level_match = re.match(r'Level (\d) (\w+) \(([^)]+)\)', header)

    if cantrip_match:
        level = 0
        school = cantrip_match.group(1)
        classes = [c.strip() for c in cantrip_match.group(2).split(',')]
    elif level_match:
        level = int(level_match.group(1))
        school = level_match.group(2)
        classes = [c.strip() for c in level_match.group(3).split(',')]
    else:
        return None

    # Parse remaining fields
    data = {
        'level': level,
        'school': school,
        'classes': classes,
        'concentration': False,
        'ritual': False,
    }

    # Extract Casting Time, Range, Components, Duration
    remaining_text = '\n'.join(lines[header_idx+1:])

    casting_match = re.search(r'Casting Time:\s*(.+?)(?=\n|Range:)', remaining_text, re.DOTALL)
    if casting_match:
        casting_time = casting_match.group(1).strip()
        if 'Ritual' in casting_time:
            data['ritual'] = True
            casting_time = casting_time.replace(' or Ritual', '').replace('Ritual', '').strip()
        data['castingTime'] = casting_time

    range_match = re.search(r'Range:\s*(.+?)(?=\n|Components:)', remaining_text, re.DOTALL)
    if range_match:
        data['range'] = range_match.group(1).strip()

    comp_match = re.search(r'Components:\s*(.+?)(?=\n|Duration:)', remaining_text, re.DOTALL)
    if comp_match:
        data['components'] = parse_components(comp_match.group(1).strip())

    duration_match = re.search(r'Duration:\s*(.+?)(?=\n\n|\n[A-Z])', remaining_text, re.DOTALL)
    if duration_match:
        duration = duration_match.group(1).strip()
        if 'Concentration' in duration:
            data['concentration'] = True
        data['duration'] = duration

    return data

# Find all spells by looking for the pattern
print("Scanning for spells...")

# Simpler approach: find spell names followed by their headers
spell_start_pattern = re.compile(
    r'^      ([A-Z][a-zA-Z\'\-/]+(?: [A-Z]?[a-zA-Z\'\-/]+)*)\s*\n\s+'
    r'(Level \d \w+|(?:Abjuration|Conjuration|Divination|Enchantment|Evocation|Illusion|Necromancy|Transmutation) Cantrip) \(([^)]+)\)',
    re.MULTILINE
)

matches = list(spell_start_pattern.finditer(spell_text))
print(f"Found {len(matches)} spell candidates")

# Process each match
spells = []
for i, match in enumerate(matches):
    name = match.group(1).strip()

    # Skip if name contains lowercase-only words (likely not a spell name)
    words = name.split()
    if any(w.islower() and len(w) > 2 for w in words):
        continue

    # Get the text block for this spell (until next spell or end)
    start = match.start()
    end = matches[i+1].start() if i+1 < len(matches) else len(spell_text)
    block = spell_text[start:end]

    # Parse the block
    header_line = match.group(2)
    classes_str = match.group(3)

    # Determine level and school
    cantrip_match = re.match(r'(\w+) Cantrip', header_line)
    level_match = re.match(r'Level (\d) (\w+)', header_line)

    if cantrip_match:
        level = 0
        school = cantrip_match.group(1)
    elif level_match:
        level = int(level_match.group(1))
        school = level_match.group(2)
    else:
        continue

    classes = [c.strip() for c in classes_str.split(',')]

    # Extract other fields from the block
    casting_match = re.search(r'Casting Time:\s*([^\n]+)', block)
    range_match = re.search(r'Range:\s*([^\n]+)', block)
    comp_match = re.search(r'Components:\s*([^\n]+)', block)
    duration_match = re.search(r'Duration:\s*([^\n]+)', block)

    if not all([casting_match, range_match, comp_match, duration_match]):
        print(f"  Skipping {name} - missing fields")
        continue

    casting_time = casting_match.group(1).strip()
    ritual = 'Ritual' in casting_time
    if ritual:
        casting_time = casting_time.replace(' or Ritual', '').strip()

    duration = duration_match.group(1).strip()
    concentration = 'Concentration' in duration

    components = parse_components(comp_match.group(1))

    # Extract description (everything after Duration line)
    desc_match = re.search(r'Duration:[^\n]+\n\s*(.+)', block, re.DOTALL)
    description = ""
    higher_level = None

    if desc_match:
        desc_text = desc_match.group(1).strip()
        # Clean up the description
        # Remove page numbers like "123   System Reference Document 5.2.1"
        desc_text = re.sub(r'\d+\s+System Reference Document \d+\.\d+\.\d+', '', desc_text)
        # Remove extra whitespace
        desc_text = re.sub(r'\n\s+', '\n', desc_text)
        desc_text = re.sub(r'\s{2,}', ' ', desc_text)

        # Check for higher level casting
        higher_match = re.search(r'Using a Higher-Level Spell Slot\.\s*(.+?)(?=\n\n|$)', desc_text, re.DOTALL)
        cantrip_upgrade = re.search(r'Cantrip Upgrade\.\s*(.+?)(?=\n\n|$)', desc_text, re.DOTALL)

        if higher_match:
            higher_level = higher_match.group(1).strip()
            desc_text = desc_text[:higher_match.start()].strip()
        elif cantrip_upgrade:
            # For cantrips, include the upgrade in the description
            pass

        description = desc_text.strip()

    spell = {
        'name': name,
        'level': level,
        'school': school,
        'classes': classes,
        'castingTime': casting_time,
        'range': range_match.group(1).strip(),
        'components': components,
        'duration': duration,
        'concentration': concentration,
        'ritual': ritual,
        'description': description,
    }
    if higher_level:
        spell['higherLevel'] = higher_level

    spells.append(spell)
    print(f"  {name} (Level {level} {school})")

print(f"\nExtracted {len(spells)} spells")

# Create output directory
output_dir = Path(__file__).parent.parent / "spellbook"

# Group by school
by_school = {}
for spell in spells:
    school = spell['school'].lower()
    if school not in by_school:
        by_school[school] = []
    by_school[school].append(spell)

# Write MDX files
for school, school_spells in by_school.items():
    school_dir = output_dir / school
    school_dir.mkdir(parents=True, exist_ok=True)

    for spell in school_spells:
        filename = slugify(spell['name']) + '.mdx'
        filepath = school_dir / filename

        # Build frontmatter
        frontmatter = {
            'title': spell['name'],
            'level': spell['level'],
            'school': spell['school'],
            'castingTime': spell['castingTime'],
            'range': spell['range'],
            'components': spell['components'],
            'duration': spell['duration'],
            'concentration': spell['concentration'],
            'ritual': spell['ritual'],
            'classes': spell['classes'],
        }
        if 'higherLevel' in spell:
            frontmatter['higherLevel'] = spell['higherLevel']

        # Write file
        with open(filepath, 'w') as f:
            f.write('---\n')
            f.write(yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False))
            f.write('---\n\n')
            f.write(spell['description'])
            f.write('\n')

        print(f"  Wrote {filepath.name}")

print(f"\nDone! Wrote {len(spells)} spell files.")
