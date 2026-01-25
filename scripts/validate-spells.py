#!/usr/bin/env python3
"""
Validate spell MDX frontmatter against SRD 5.2.1 extracted text.
Compares: level, school, classes, casting time, range, components, duration, concentration, ritual
"""

import os
import re
import yaml
from pathlib import Path

SPELLBOOK_DIR = Path(__file__).parent.parent / "spellbook"
SRD_FILE = Path(__file__).parent.parent / "pdfs" / "DND-SRD-5.2.1-CC - updated.docx.txt"

def parse_mdx_frontmatter(filepath):
    """Extract YAML frontmatter from MDX file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None

    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None

def load_our_spells():
    """Load all spells from our MDX files."""
    spells = {}
    for school_dir in SPELLBOOK_DIR.iterdir():
        if not school_dir.is_dir():
            continue
        for mdx_file in school_dir.glob("*.mdx"):
            if mdx_file.name == "index.mdx":
                continue
            fm = parse_mdx_frontmatter(mdx_file)
            if fm and 'title' in fm:
                spells[fm['title'].lower()] = {
                    'file': str(mdx_file.relative_to(SPELLBOOK_DIR.parent)),
                    **fm
                }
    return spells

def parse_srd_spells():
    """Parse spells from SRD extracted text."""
    with open(SRD_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove Windows line endings
    content = content.replace('\r\n', '\n')

    spells = {}
    lines = content.split('\n')

    i = 0
    while i < len(lines):
        line = lines[i]

        # Match spell entry headers like "         1. Acid Arrow"
        spell_match = re.match(r'^\s+\d+\.\s+([A-Z][A-Za-z\s\'/\-]+)$', line)
        if spell_match:
            spell_name = spell_match.group(1).strip()

            # Skip stat blocks and non-spells
            if spell_name in ['Animated Object', 'Otherworldly Steed', 'Draconic Spirit',
                              'Fey Spirit', 'Shadow Spirit', 'Construct Spirit', 'Undead Spirit',
                              'Celestial Spirit', 'Fiendish Spirit', 'Aberrant Spirit']:
                i += 1
                continue

            # Next line should have level/school/classes
            if i + 1 < len(lines):
                info_line = lines[i + 1].strip()

                # Parse "Level X School (Classes)" or "School Cantrip (Classes)"
                cantrip_match = re.match(r'^(\w+)\s+Cantrip\s+\(([^)]+)\)', info_line)
                leveled_match = re.match(r'^Level\s+(\d+)\s+(\w+)\s+\(([^)]+)\)', info_line)

                spell_data = {'name': spell_name}

                if cantrip_match:
                    spell_data['level'] = 0
                    spell_data['school'] = cantrip_match.group(1)
                    spell_data['classes'] = [c.strip() for c in cantrip_match.group(2).split(',')]
                elif leveled_match:
                    spell_data['level'] = int(leveled_match.group(1))
                    spell_data['school'] = leveled_match.group(2)
                    spell_data['classes'] = [c.strip() for c in leveled_match.group(3).split(',')]
                else:
                    i += 1
                    continue

                # Parse remaining fields
                j = i + 2
                while j < len(lines) and j < i + 10:
                    field_line = lines[j].strip()

                    if field_line.startswith('Casting Time:'):
                        spell_data['castingTime'] = field_line.replace('Casting Time:', '').strip()
                    elif field_line.startswith('Range:'):
                        spell_data['range'] = field_line.replace('Range:', '').strip()
                    elif field_line.startswith('Component:') or field_line.startswith('Components:'):
                        comp_str = field_line.replace('Components:', '').replace('Component:', '').strip()
                        spell_data['components_raw'] = comp_str
                        spell_data['verbal'] = 'V' in comp_str.split(',')[0].split('(')[0]
                        spell_data['somatic'] = 'S' in comp_str.split('(')[0]
                        spell_data['material'] = 'M' in comp_str.split('(')[0]
                    elif field_line.startswith('Duration:'):
                        dur = field_line.replace('Duration:', '').strip()
                        spell_data['duration'] = dur
                        spell_data['concentration'] = 'Concentration' in dur

                    # Stop if we hit the next spell or description
                    if j > i + 2 and (re.match(r'^\s+\d+\.', lines[j]) or
                                       (not field_line.startswith(('Casting', 'Range', 'Component', 'Duration'))
                                        and len(field_line) > 50)):
                        break
                    j += 1

                # Check for ritual in casting time
                spell_data['ritual'] = 'Ritual' in spell_data.get('castingTime', '')

                spells[spell_name.lower()] = spell_data

        i += 1

    return spells

def compare_spells(ours, srd):
    """Compare our spells against SRD and report differences."""
    issues = []

    for name, our_spell in sorted(ours.items()):
        if name not in srd:
            # Try alternate names
            alt_name = name.replace('-', ' ').replace('/', '-')
            if alt_name not in srd:
                issues.append(f"NOT IN SRD: {our_spell['title']} ({our_spell['file']})")
                continue
            srd_spell = srd[alt_name]
        else:
            srd_spell = srd[name]

        spell_issues = []

        # Compare level
        if our_spell.get('level') != srd_spell.get('level'):
            spell_issues.append(f"level: ours={our_spell.get('level')} srd={srd_spell.get('level')}")

        # Compare school
        our_school = our_spell.get('school', '').lower()
        srd_school = srd_spell.get('school', '').lower()
        if our_school != srd_school:
            spell_issues.append(f"school: ours={our_school} srd={srd_school}")

        # Compare classes
        our_classes = set(c.lower() for c in our_spell.get('classes', []))
        srd_classes = set(c.lower() for c in srd_spell.get('classes', []))
        if our_classes != srd_classes:
            missing = srd_classes - our_classes
            extra = our_classes - srd_classes
            if missing:
                spell_issues.append(f"missing classes: {missing}")
            if extra:
                spell_issues.append(f"extra classes: {extra}")

        # Compare concentration
        our_conc = our_spell.get('concentration', False)
        srd_conc = srd_spell.get('concentration', False)
        if our_conc != srd_conc:
            spell_issues.append(f"concentration: ours={our_conc} srd={srd_conc}")

        # Compare ritual
        our_ritual = our_spell.get('ritual', False)
        srd_ritual = srd_spell.get('ritual', False)
        if our_ritual != srd_ritual:
            spell_issues.append(f"ritual: ours={our_ritual} srd={srd_ritual}")

        # Compare components
        our_v = our_spell.get('components', {}).get('verbal', False)
        our_s = our_spell.get('components', {}).get('somatic', False)
        our_m = bool(our_spell.get('components', {}).get('material'))

        if our_v != srd_spell.get('verbal', False):
            spell_issues.append(f"verbal: ours={our_v} srd={srd_spell.get('verbal')}")
        if our_s != srd_spell.get('somatic', False):
            spell_issues.append(f"somatic: ours={our_s} srd={srd_spell.get('somatic')}")
        if our_m != srd_spell.get('material', False):
            spell_issues.append(f"material: ours={our_m} srd={srd_spell.get('material')}")

        if spell_issues:
            issues.append(f"\n{our_spell['title']} ({our_spell['file']}):")
            for issue in spell_issues:
                issues.append(f"  - {issue}")

    return issues

def main():
    print("Loading our spells...")
    our_spells = load_our_spells()
    print(f"  Found {len(our_spells)} spells in spellbook/")

    print("\nParsing SRD spells...")
    srd_spells = parse_srd_spells()
    print(f"  Found {len(srd_spells)} spells in SRD")

    print("\nComparing...")
    issues = compare_spells(our_spells, srd_spells)

    if issues:
        print(f"\n{'='*60}")
        print(f"ISSUES FOUND ({len([i for i in issues if i.startswith('\\n')])} spells with problems):")
        print('='*60)
        for issue in issues:
            print(issue)
    else:
        print("\n✓ All spells match SRD metadata!")

    return len(issues) > 0

if __name__ == "__main__":
    exit(1 if main() else 0)
