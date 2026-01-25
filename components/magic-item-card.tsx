interface MagicItemCardProps {
  data: {
    title: string;
    category?: string;
    rarity?: string;
    itemType?: string;
    attunement?: boolean | string;
  };
}

export function MagicItemCard({ data }: MagicItemCardProps) {
  const { category, rarity, itemType, attunement } = data;

  // Don't render if no metadata
  if (!category && !rarity && !itemType && !attunement) return null;

  // Build category/type display: "Armor (Shield)" or just "Potion"
  let typeDisplay = category || '';
  if (itemType) {
    typeDisplay = category ? `${category} (${itemType})` : itemType;
  }

  // Build attunement text
  let attunementText = null;
  if (attunement) {
    attunementText = attunement === true
      ? "Requires Attunement"
      : `Requires Attunement by ${attunement}`;
  }

  return (
    <div className="mb-6 p-4 rounded-lg bg-fd-muted/50 text-sm">
      <div className="font-medium text-fd-muted-foreground">
        {typeDisplay && <span>{typeDisplay}</span>}
        {typeDisplay && rarity && <span> · </span>}
        {rarity && <span>{rarity}</span>}
        {attunementText && <span> · {attunementText}</span>}
      </div>
    </div>
  );
}
