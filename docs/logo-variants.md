# Logo Variants

Reference file for hex logo variations we've explored.

## Current: Gold (all segments)

All six triangles use `#E8B923` gold fill.

## Multicolor (warm/cool alternating)

Each triangle uses a different section/palette color, sequenced for warm/cool contrast:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
  <mask id="hex-cuts">
    <polygon points="16,1 28,8 28,24 16,31 4,24 4,8" fill="white"/>
    <line x1="16" y1="0" x2="16" y2="32" stroke="black" stroke-width="2.5"/>
    <line x1="3" y1="7" x2="29" y2="25" stroke="black" stroke-width="2.5"/>
    <line x1="29" y1="7" x2="3" y2="25" stroke="black" stroke-width="2.5"/>
  </mask>
  <g mask="url(#hex-cuts)">
    <!-- Upper-left: Gold -->
    <polygon points="4,8 16,1 16,16" fill="#E8B923"/>
    <!-- Upper-right: Deep Teal -->
    <polygon points="16,1 28,8 16,16" fill="#1b8a8f"/>
    <!-- Middle-right: Bestiary Red -->
    <polygon points="28,8 28,24 16,16" fill="#c23a4a"/>
    <!-- Lower-right: Moss -->
    <polygon points="28,24 16,31 16,16" fill="#6a9a42"/>
    <!-- Lower-left: Burnt Sienna -->
    <polygon points="16,31 4,24 16,16" fill="#c35a1f"/>
    <!-- Middle-left: Dusty Violet -->
    <polygon points="4,24 4,8 16,16" fill="#6b4b9a"/>
  </g>
</svg>
```

### Color mapping

| Position | Color | Hex | Source |
|----------|-------|-----|--------|
| Upper-left | Gold | #E8B923 | Brand / Rules |
| Upper-right | Deep Teal | #1b8a8f | Spellbook |
| Middle-right | Bestiary Red | #c23a4a | Bestiary |
| Lower-right | Moss | #6a9a42 | Artifact palette |
| Lower-left | Burnt Sienna | #c35a1f | Artifact palette |
| Middle-left | Dusty Violet | #6b4b9a | Magic Items |

### Notes
- Warm/cool alternation ensures every adjacent pair has contrast
- Moss was brightened from `#557d36` to `#6a9a42` to match vibrancy of other segments
- Needs more design work — reads well at navbar size but felt off at hero size
