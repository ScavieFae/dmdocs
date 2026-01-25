#!/usr/bin/env python3
"""
Reorganize wondrous items into subcategories.
"""

import os
import json
import shutil

BASE_DIR = os.path.join(os.path.dirname(__file__), '..', 'magicitems', 'wondrous-items')

# Categorization rules based on item name prefixes/keywords
CATEGORIES = {
    'worn': {
        'title': 'Worn Items',
        'keywords': ['boots', 'belt', 'cloak', 'cape', 'robe', 'slippers', 'mantle', 'gloves', 'gauntlets', 'bracers', 'winged-boots', 'wings'],
        'items': []
    },
    'head': {
        'title': 'Head Items',
        'keywords': ['helm', 'hat', 'headband', 'circlet', 'goggles', 'eyes'],
        'items': []
    },
    'jewelry': {
        'title': 'Jewelry',
        'keywords': ['amulet', 'necklace', 'medallion', 'brooch', 'periapt', 'pearl', 'scarab', 'talisman'],
        'items': []
    },
    'containers': {
        'title': 'Containers',
        'keywords': ['bag', 'bottle', 'bowl', 'decanter', 'flask', 'quiver', 'haversack', 'hole', 'well'],
        'items': []
    },
    'figurines': {
        'title': 'Figurines',
        'keywords': ['figurine'],
        'items': []
    },
    'instruments': {
        'title': 'Instruments & Tools',
        'keywords': ['horn', 'pipes', 'chime', 'drum', 'candle', 'lantern', 'mirror', 'crystal', 'gem', 'stone', 'cube', 'sphere', 'orb', 'bead', 'dust', 'rope', 'carpet', 'broom'],
        'items': []
    },
    'tomes': {
        'title': 'Tomes & Manuals',
        'keywords': ['tome', 'manual', 'deck'],
        'items': []
    },
}

def categorize_item(filename):
    """Determine which category an item belongs to."""
    name = filename.replace('.mdx', '').lower()

    for cat_key, cat_info in CATEGORIES.items():
        for keyword in cat_info['keywords']:
            if keyword in name:
                return cat_key

    return 'misc'

def main():
    # Get all mdx files (excluding index)
    files = [f for f in os.listdir(BASE_DIR) if f.endswith('.mdx') and f != 'index.mdx']

    # Categorize each item
    misc_items = []
    for filename in files:
        category = categorize_item(filename)
        if category == 'misc':
            misc_items.append(filename)
        else:
            CATEGORIES[category]['items'].append(filename)

    # Add misc category
    CATEGORIES['misc'] = {
        'title': 'Miscellaneous',
        'keywords': [],
        'items': misc_items
    }

    # Print summary
    print("Categorization summary:")
    for cat_key, cat_info in CATEGORIES.items():
        print(f"  {cat_info['title']}: {len(cat_info['items'])} items")

    # Create subdirectories and move files
    for cat_key, cat_info in CATEGORIES.items():
        if not cat_info['items']:
            continue

        cat_dir = os.path.join(BASE_DIR, cat_key)
        os.makedirs(cat_dir, exist_ok=True)

        # Move files
        for filename in cat_info['items']:
            src = os.path.join(BASE_DIR, filename)
            dst = os.path.join(cat_dir, filename)
            if os.path.exists(src):
                shutil.move(src, dst)

        # Create meta.json
        slugs = sorted([f.replace('.mdx', '') for f in cat_info['items']])
        meta = {
            'title': cat_info['title'],
            'pages': slugs,
            'defaultOpen': False
        }
        meta_path = os.path.join(cat_dir, 'meta.json')
        with open(meta_path, 'w') as f:
            json.dump(meta, f, indent=2)
            f.write('\n')

        # Create index.mdx
        index_content = f"""---
title: {cat_info['title']}
description: {cat_info['title']} - Wondrous Items
---

# {cat_info['title']}

| Item | Rarity |
|------|--------|
"""
        for filename in sorted(cat_info['items']):
            slug = filename.replace('.mdx', '')
            # Read the file to get rarity
            filepath = os.path.join(cat_dir, filename)
            rarity = 'Unknown'
            with open(filepath, 'r') as f:
                for line in f:
                    if line.startswith('rarity:'):
                        rarity = line.split(':')[1].strip()
                        break
            title = slug.replace('-', ' ').title()
            index_content += f"| [{title}]({slug}) | {rarity} |\n"

        index_path = os.path.join(cat_dir, 'index.mdx')
        with open(index_path, 'w') as f:
            f.write(index_content)

    # Update wondrous-items meta.json
    categories_with_items = [k for k, v in CATEGORIES.items() if v['items']]
    meta = {
        'title': 'Wondrous Items',
        'pages': categories_with_items,
        'defaultOpen': False
    }
    meta_path = os.path.join(BASE_DIR, 'meta.json')
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)
        f.write('\n')

    # Update wondrous-items index.mdx
    index_content = """---
title: Wondrous Items
description: Miscellaneous magical objects
---

# Wondrous Items

Wondrous items include wearable items such as boots, belts, capes, and gloves, as well as items that don't fit any other category.

## Categories

| Category | Items |
|----------|-------|
"""
    for cat_key in categories_with_items:
        cat_info = CATEGORIES[cat_key]
        index_content += f"| [{cat_info['title']}]({cat_key}) | {len(cat_info['items'])} |\n"

    index_path = os.path.join(BASE_DIR, 'index.mdx')
    with open(index_path, 'w') as f:
        f.write(index_content)

    print(f"\nReorganized {len(files)} wondrous items into {len(categories_with_items)} categories")

if __name__ == '__main__':
    main()
