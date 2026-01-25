#!/usr/bin/env python3
"""
Import magic items from SRD 5.2.1 markdown.
Source: https://github.com/springbov/dndsrd5.2_markdown
"""

import re
import os
import urllib.request

# Category mapping to folder names
CATEGORY_MAP = {
    'armor': 'armor',
    'potion': 'potions',
    'ring': 'rings',
    'rod': 'rods',
    'scroll': 'scrolls',
    'staff': 'staffs',
    'wand': 'wands',
    'weapon': 'weapons',
    'wondrous item': 'wondrous-items',
}

def clean_name(name):
    """Remove markdown formatting from item name."""
    # Remove bold/italic markers
    name = re.sub(r'\*+', '', name)
    return name.strip()

def slugify(name):
    """Convert item name to kebab-case slug."""
    slug = clean_name(name).lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')

def parse_rarity(info_line):
    """Extract rarity from the info line."""
    rarities = ['Common', 'Uncommon', 'Rare', 'Very Rare', 'Legendary', 'Artifact']
    for rarity in rarities:
        if rarity.lower() in info_line.lower():
            return rarity
    return None

def parse_category(info_line):
    """Extract category from the info line."""
    info_lower = info_line.lower()
    for key, folder in CATEGORY_MAP.items():
        if key in info_lower:
            return folder
    return 'wondrous-items'  # Default

def parse_attunement(info_line):
    """Extract attunement requirement."""
    if 'requires attunement' in info_line.lower():
        # Check for specific requirements
        match = re.search(r'requires attunement by (.+?)\)', info_line, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return True
    return False

def parse_item_type(info_line):
    """Extract the specific item type (e.g., 'Any Medium or Heavy Armor')."""
    # Match content in parentheses after category
    match = re.match(r'\*(\w+)\s*\(([^)]+)\)', info_line)
    if match:
        return match.group(2).strip()
    return None

def parse_items(content):
    """Parse all magic items from markdown content."""
    items = []

    # Split on #### headers (item names)
    parts = re.split(r'\n####\s+', content)

    for part in parts[1:]:  # Skip content before first item
        lines = part.strip().split('\n')
        if not lines:
            continue

        name = clean_name(lines[0].strip())

        # Skip section headers that aren't items
        if name in ['Magic Item Rules', 'Spells Cast from Items']:
            continue

        # Find the info line (starts with *)
        info_line = ''
        content_start = 1
        for i, line in enumerate(lines[1:], 1):
            if line.strip().startswith('*') and line.strip().endswith('*'):
                info_line = line.strip().strip('*')
                content_start = i + 1
                break

        if not info_line:
            continue

        # Parse metadata
        rarity = parse_rarity(info_line)
        category = parse_category(info_line)
        attunement = parse_attunement(info_line)
        item_type = parse_item_type('*' + info_line + '*')

        # Get description (everything after info line)
        description = '\n'.join(lines[content_start:]).strip()

        if not description:
            continue

        items.append({
            'name': name,
            'rarity': rarity,
            'category': category,
            'attunement': attunement,
            'item_type': item_type,
            'description': description,
        })

    return items

def generate_mdx(item):
    """Generate MDX content for an item."""
    # Map folder name to display category
    category_display = {
        'armor': 'Armor',
        'potions': 'Potion',
        'rings': 'Ring',
        'rods': 'Rod',
        'scrolls': 'Scroll',
        'staffs': 'Staff',
        'wands': 'Wand',
        'weapons': 'Weapon',
        'wondrous-items': 'Wondrous Item',
    }

    frontmatter = [
        '---',
        f'title: {item["name"]}',
    ]

    # Add category
    category = category_display.get(item['category'], 'Wondrous Item')
    frontmatter.append(f'category: {category}')

    if item['rarity']:
        frontmatter.append(f'rarity: {item["rarity"]}')

    if item['item_type']:
        frontmatter.append(f'itemType: "{item["item_type"]}"')

    if item['attunement']:
        if item['attunement'] is True:
            frontmatter.append('attunement: true')
        else:
            frontmatter.append(f'attunement: "{item["attunement"]}"')

    frontmatter.append('---')
    frontmatter.append('')
    frontmatter.append(item['description'])

    return '\n'.join(frontmatter)

def main():
    # Read from local file (download with curl first if needed)
    local_path = "/tmp/magic-items.md"
    print(f"Reading from {local_path}...")

    with open(local_path, 'r') as f:
        content = f.read()

    # Parse items
    items = parse_items(content)
    print(f"Found {len(items)} magic items")

    # Count by category
    categories = {}
    for item in items:
        cat = item['category']
        categories[cat] = categories.get(cat, 0) + 1

    print("\nItems by category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

    # Write items to files
    base_dir = os.path.join(os.path.dirname(__file__), '..', 'magicitems')

    for item in items:
        category_dir = os.path.join(base_dir, item['category'])
        os.makedirs(category_dir, exist_ok=True)

        slug = slugify(item['name'])
        filepath = os.path.join(category_dir, f'{slug}.mdx')

        mdx_content = generate_mdx(item)

        with open(filepath, 'w') as f:
            f.write(mdx_content)

    print(f"\nWrote {len(items)} magic item files")

    # Update meta.json files for each category
    for category in categories:
        category_dir = os.path.join(base_dir, category)
        meta_path = os.path.join(category_dir, 'meta.json')

        # Get all item slugs in this category
        item_slugs = sorted([
            slugify(item['name'])
            for item in items
            if item['category'] == category
        ])

        # Read existing meta.json to preserve title
        import json
        existing_title = category.replace('-', ' ').title()
        if os.path.exists(meta_path):
            with open(meta_path) as f:
                existing = json.load(f)
                existing_title = existing.get('title', existing_title)

        meta = {
            'title': existing_title,
            'pages': item_slugs,
            'defaultOpen': False
        }

        with open(meta_path, 'w') as f:
            json.dump(meta, f, indent=2)
            f.write('\n')

    print("Updated meta.json files")

if __name__ == '__main__':
    main()
