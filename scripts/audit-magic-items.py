#!/usr/bin/env python3
"""
Audit magic item metadata against 5.2.1 SRD.
Checks rarity and attunement for all magic items.
"""

import os
import re
import yaml
from pathlib import Path

# Read SRD extracted text
srd_path = Path("pdfs/DND-SRD-5.2.1-CC - updated.docx.txt")
with open(srd_path, 'r') as f:
    srd_text = f.read()

# Parse SRD items - look for patterns like:
# "123. Item Name"
# "Category, Rarity (Requires Attunement...)"
item_pattern = re.compile(
    r'^\s*\d+\.\s+(.+?)\n'
    r'([A-Za-z].*?),\s*(Common|Uncommon|Rare|Very Rare|Legendary|Artifact|Rarity Varies)'
    r'(?:\s*\(([^)]+)\))?',
    re.MULTILINE
)

srd_items = {}
for match in item_pattern.finditer(srd_text):
    name = match.group(1).strip()
    category = match.group(2).strip()
    rarity = match.group(3).strip()
    attunement_text = match.group(4) if match.group(4) else ""

    # Parse attunement
    attunement = None
    if "Requires Attunement" in attunement_text:
        if "by a " in attunement_text or "by an " in attunement_text:
            # Extract the class/type requirement
            req_match = re.search(r'by (?:a |an )?(.+)', attunement_text)
            if req_match:
                attunement = req_match.group(1).strip()
        else:
            attunement = True

    srd_items[name] = {
        'rarity': rarity,
        'attunement': attunement,
        'category': category
    }

print(f"Found {len(srd_items)} items in SRD\n")

# Now audit our items
magicitems_path = Path("magicitems")
issues = []
fixed_count = 0

def get_item_files():
    """Get all MDX files in magicitems folder."""
    for mdx_file in magicitems_path.rglob("*.mdx"):
        if mdx_file.name == "index.mdx":
            continue
        yield mdx_file

def parse_frontmatter(content):
    """Extract YAML frontmatter from MDX file."""
    if not content.startswith('---'):
        return None, content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return None, content
    try:
        fm = yaml.safe_load(parts[1])
        return fm, '---' + parts[1] + '---' + parts[2]
    except:
        return None, content

def update_frontmatter(content, updates):
    """Update frontmatter values."""
    if not content.startswith('---'):
        return content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content

    lines = parts[1].strip().split('\n')
    new_lines = []
    keys_updated = set()

    for line in lines:
        key_match = re.match(r'^(\w+):', line)
        if key_match:
            key = key_match.group(1)
            if key in updates:
                value = updates[key]
                if value is True:
                    new_lines.append(f'{key}: true')
                elif value is False or value is None:
                    # Skip this key (don't include it)
                    pass
                elif isinstance(value, str):
                    if ' ' in value or value in ('true', 'false'):
                        new_lines.append(f'{key}: "{value}"')
                    else:
                        new_lines.append(f'{key}: {value}')
                else:
                    new_lines.append(f'{key}: {value}')
                keys_updated.add(key)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)

    # Add any new keys not in original
    for key, value in updates.items():
        if key not in keys_updated and value is not None and value is not False:
            if value is True:
                new_lines.append(f'{key}: true')
            elif isinstance(value, str):
                if ' ' in value or value in ('true', 'false'):
                    new_lines.append(f'{key}: "{value}"')
                else:
                    new_lines.append(f'{key}: {value}')
            else:
                new_lines.append(f'{key}: {value}')

    return '---\n' + '\n'.join(new_lines) + '\n---' + parts[2]

# Audit each item
for mdx_file in get_item_files():
    with open(mdx_file, 'r') as f:
        content = f.read()

    fm, _ = parse_frontmatter(content)
    if not fm or 'title' not in fm:
        continue

    title = fm['title']
    our_rarity = fm.get('rarity', 'Unknown')
    our_attunement = fm.get('attunement')

    # Find matching SRD item
    srd_item = srd_items.get(title)
    if not srd_item:
        # Try alternate names
        # Handle +1, +2, or +3 variants
        if '+1, +2, or +3' in title or ', +1, +2, or +3' in title:
            continue  # These have variable rarity
        continue

    srd_rarity = srd_item['rarity']
    srd_attunement = srd_item['attunement']

    # Compare
    rarity_matches = our_rarity == srd_rarity

    # Normalize attunement comparison
    our_att_normalized = our_attunement
    if our_attunement == "true" or our_attunement is True:
        our_att_normalized = True
    elif our_attunement in (None, False, "false"):
        our_att_normalized = None

    srd_att_normalized = srd_attunement
    if isinstance(srd_attunement, str):
        srd_att_normalized = srd_attunement

    attunement_matches = our_att_normalized == srd_att_normalized

    if not rarity_matches or not attunement_matches:
        issue = {
            'file': str(mdx_file),
            'title': title,
            'our_rarity': our_rarity,
            'srd_rarity': srd_rarity,
            'our_attunement': our_attunement,
            'srd_attunement': srd_attunement,
            'rarity_wrong': not rarity_matches,
            'attunement_wrong': not attunement_matches
        }
        issues.append(issue)

        # Auto-fix
        updates = {}
        if not rarity_matches:
            updates['rarity'] = srd_rarity
        if not attunement_matches:
            updates['attunement'] = srd_attunement

        new_content = update_frontmatter(content, updates)
        with open(mdx_file, 'w') as f:
            f.write(new_content)
        fixed_count += 1

# Report
print(f"Issues found: {len(issues)}")
print(f"Items fixed: {fixed_count}")
print()

if issues:
    print("=== Rarity Issues ===")
    rarity_issues = [i for i in issues if i['rarity_wrong']]
    for issue in sorted(rarity_issues, key=lambda x: x['title'])[:30]:
        print(f"  {issue['title']}: {issue['our_rarity']} -> {issue['srd_rarity']}")
    if len(rarity_issues) > 30:
        print(f"  ... and {len(rarity_issues) - 30} more")

    print()
    print("=== Attunement Issues ===")
    att_issues = [i for i in issues if i['attunement_wrong']]
    for issue in sorted(att_issues, key=lambda x: x['title'])[:20]:
        print(f"  {issue['title']}: {issue['our_attunement']} -> {issue['srd_attunement']}")
    if len(att_issues) > 20:
        print(f"  ... and {len(att_issues) - 20} more")
