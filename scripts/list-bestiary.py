#!/usr/bin/env python3
"""Extract proper monster names from bestiary folder structure."""

import os
import re
from pathlib import Path

# Special name mappings for monsters with unusual naming
SPECIAL_NAMES = {
    'saber-toothed-tiger': 'Saber-Toothed Tiger',
    'will-o-wisp': "Will-o'-Wisp",
    'half-dragon': 'Half-Dragon',
    'pit-fiend': 'Pit Fiend',
}

def kebab_to_title(s: str) -> str:
    """Convert kebab-case to Title Case, keeping prepositions lowercase."""
    prepositions = {'of', 'the', 'and', 'or', 'a', 'an'}
    words = s.split('-')
    result = []
    for i, word in enumerate(words):
        if i == 0 or word not in prepositions:
            result.append(word.capitalize())
        else:
            result.append(word.lower())
    return ' '.join(result)

def get_monster_name(filepath: str) -> str | None:
    """Convert a bestiary filepath to proper monster name."""
    # Skip index files
    if filepath.endswith('index.mdx'):
        return None

    rel = filepath.replace('bestiary/', '').replace('.mdx', '')
    parts = rel.split('/')

    # Check for special name mapping first
    filename = parts[-1]
    if filename in SPECIAL_NAMES:
        return SPECIAL_NAMES[filename]

    # Handle based on folder structure
    if len(parts) == 2:
        # Simple: creature_type/monster-name -> Monster Name
        return kebab_to_title(parts[1])

    elif len(parts) == 3:
        creature_type, subfolder, filename = parts

        # Dragons: dragon/red-dragon/adult -> Adult Red Dragon
        # But wyrmlings are: dragon/red-dragon/wyrmling -> Red Dragon Wyrmling
        if creature_type == 'dragon' and subfolder.endswith('-dragon'):
            color = subfolder.replace('-dragon', '')
            age = filename
            if age == 'wyrmling':
                return f"{kebab_to_title(color)} Dragon Wyrmling"
            else:
                return f"{kebab_to_title(age)} {kebab_to_title(color)} Dragon"

        # Devils: fiend/devils/chain -> Chain Devil
        # But some already have full names (pit-fiend, erinyes, lemure, imp)
        if subfolder == 'devils':
            if filename in ['pit-fiend', 'erinyes', 'lemure', 'imp']:
                return kebab_to_title(filename)
            else:
                return f"{kebab_to_title(filename)} Devil"

        # Demons have full names already
        if subfolder == 'demons':
            return kebab_to_title(filename)

        # Goblins/Hobgoblins/Bugbears: fey/goblins/boss -> Goblin Boss
        if subfolder == 'goblins':
            return f"Goblin {kebab_to_title(filename)}"
        if subfolder == 'hobgoblins':
            return f"Hobgoblin {kebab_to_title(filename)}"
        if subfolder == 'bugbears':
            return f"Bugbear {kebab_to_title(filename)}"

        # Hags have full names already
        if subfolder == 'hags':
            return kebab_to_title(filename)

        # Mephits have full names already
        if subfolder == 'mephits':
            return kebab_to_title(filename)

        # Elementals have full names already
        if subfolder == 'elementals':
            return kebab_to_title(filename)

        # Sphinxes: celestial/sphinxes/lore -> Sphinx of Lore
        if subfolder == 'sphinxes':
            return f"Sphinx of {kebab_to_title(filename)}"

        # Golems have full names already
        if subfolder == 'golems':
            return kebab_to_title(filename)

        # Default: just use filename
        return kebab_to_title(filename)

    # Unexpected structure - just use filename
    return kebab_to_title(parts[-1])

def is_redirect_file(filepath: str) -> bool:
    """Check if a file is a redirect stub, not a real monster entry."""
    try:
        with open(filepath, 'r') as f:
            content = f.read(500)  # Just read the beginning
            return 'httpEquiv="refresh"' in content or 'redirect(' in content
    except:
        return False

def main():
    bestiary_dir = Path('bestiary')
    monsters = []

    for filepath in bestiary_dir.rglob('*.mdx'):
        # Skip redirect stubs
        if is_redirect_file(str(filepath)):
            continue
        name = get_monster_name(str(filepath))
        if name:
            monsters.append(name)

    for name in sorted(monsters):
        print(name)

if __name__ == '__main__':
    main()
