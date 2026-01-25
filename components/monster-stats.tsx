interface MonsterStatsProps {
  data: {
    title: string;
    size?: string;
    creatureType?: string;
    alignment?: string;
    ac?: number;
    hp?: { average: number; formula: string };
    speed?: {
      walk?: number;
      fly?: number;
      swim?: number;
      burrow?: number;
      climb?: number;
    };
    abilities?: {
      str: number;
      dex: number;
      con: number;
      int: number;
      wis: number;
      cha: number;
    };
    saves?: {
      str?: number;
      dex?: number;
      con?: number;
      int?: number;
      wis?: number;
      cha?: number;
    };
    skills?: string[];
    immunities?: string[];
    resistances?: string[];
    vulnerabilities?: string[];
    conditionImmunities?: string[];
    senses?: string[];
    languages?: string[];
    cr?: string;
    xp?: number;
  };
}

function modifier(score: number): string {
  const mod = Math.floor((score - 10) / 2);
  return mod >= 0 ? `+${mod}` : `${mod}`;
}

function AbilityScore({ label, score }: { label: string; score: number }) {
  return (
    <div className="text-center">
      <div className="text-xs font-bold text-fd-muted-foreground uppercase tracking-wide">
        {label}
      </div>
      <div className="text-lg font-semibold">{score}</div>
      <div className="text-sm text-fd-muted-foreground">({modifier(score)})</div>
    </div>
  );
}

export function MonsterStats({ data }: MonsterStatsProps) {
  if (!data.creatureType) return null;

  const speedParts: string[] = [];
  if (data.speed?.walk) speedParts.push(`${data.speed.walk} ft.`);
  if (data.speed?.fly) speedParts.push(`Fly ${data.speed.fly} ft.`);
  if (data.speed?.swim) speedParts.push(`Swim ${data.speed.swim} ft.`);
  if (data.speed?.burrow) speedParts.push(`Burrow ${data.speed.burrow} ft.`);
  if (data.speed?.climb) speedParts.push(`Climb ${data.speed.climb} ft.`);
  const speedStr = speedParts.join(', ') || '30 ft.';

  const saveParts: string[] = [];
  if (data.saves) {
    if (data.saves.str !== undefined) saveParts.push(`Str ${data.saves.str >= 0 ? '+' : ''}${data.saves.str}`);
    if (data.saves.dex !== undefined) saveParts.push(`Dex ${data.saves.dex >= 0 ? '+' : ''}${data.saves.dex}`);
    if (data.saves.con !== undefined) saveParts.push(`Con ${data.saves.con >= 0 ? '+' : ''}${data.saves.con}`);
    if (data.saves.int !== undefined) saveParts.push(`Int ${data.saves.int >= 0 ? '+' : ''}${data.saves.int}`);
    if (data.saves.wis !== undefined) saveParts.push(`Wis ${data.saves.wis >= 0 ? '+' : ''}${data.saves.wis}`);
    if (data.saves.cha !== undefined) saveParts.push(`Cha ${data.saves.cha >= 0 ? '+' : ''}${data.saves.cha}`);
  }

  return (
    <div className="monster-stats mb-8 rounded-lg border border-[hsl(var(--primary))] overflow-hidden">
      {/* Header */}
      <div className="bg-[hsl(var(--primary))] px-4 py-3">
        <h2 className="text-xl font-bold text-[hsl(var(--primary-foreground))] m-0">
          {data.title}
        </h2>
        <p className="text-sm text-[hsl(var(--primary-foreground))]/80 m-0 italic">
          {data.size} {data.creatureType}, {data.alignment}
        </p>
      </div>

      {/* Combat Stats */}
      <div className="px-4 py-3 border-b border-fd-border">
        <div className="grid grid-cols-3 gap-4 text-sm">
          <div>
            <span className="font-bold text-[hsl(var(--primary))]">Armor Class</span>{' '}
            <span>{data.ac}</span>
          </div>
          <div>
            <span className="font-bold text-[hsl(var(--primary))]">Hit Points</span>{' '}
            <span>{data.hp?.average} ({data.hp?.formula})</span>
          </div>
          <div>
            <span className="font-bold text-[hsl(var(--primary))]">Speed</span>{' '}
            <span>{speedStr}</span>
          </div>
        </div>
      </div>

      {/* Ability Scores */}
      {data.abilities && (
        <div className="px-4 py-4 border-b border-fd-border bg-fd-muted/30">
          <div className="grid grid-cols-6 gap-3">
            <AbilityScore label="STR" score={data.abilities.str} />
            <AbilityScore label="DEX" score={data.abilities.dex} />
            <AbilityScore label="CON" score={data.abilities.con} />
            <AbilityScore label="INT" score={data.abilities.int} />
            <AbilityScore label="WIS" score={data.abilities.wis} />
            <AbilityScore label="CHA" score={data.abilities.cha} />
          </div>
        </div>
      )}

      {/* Secondary Stats */}
      <div className="px-4 py-3 text-sm space-y-1">
        {saveParts.length > 0 && (
          <div>
            <span className="font-bold text-[hsl(var(--primary))]">Saving Throws</span>{' '}
            {saveParts.join(', ')}
          </div>
        )}
        {data.skills && data.skills.length > 0 && (
          <div>
            <span className="font-bold text-[hsl(var(--primary))]">Skills</span>{' '}
            {data.skills.join(', ')}
          </div>
        )}
        {data.vulnerabilities && data.vulnerabilities.length > 0 && (
          <div>
            <span className="font-bold text-[hsl(var(--primary))]">Vulnerabilities</span>{' '}
            {data.vulnerabilities.join(', ')}
          </div>
        )}
        {data.resistances && data.resistances.length > 0 && (
          <div>
            <span className="font-bold text-[hsl(var(--primary))]">Resistances</span>{' '}
            {data.resistances.join(', ')}
          </div>
        )}
        {data.immunities && data.immunities.length > 0 && (
          <div>
            <span className="font-bold text-[hsl(var(--primary))]">Immunities</span>{' '}
            {data.immunities.join(', ')}
          </div>
        )}
        {data.conditionImmunities && data.conditionImmunities.length > 0 && (
          <div>
            <span className="font-bold text-[hsl(var(--primary))]">Condition Immunities</span>{' '}
            {data.conditionImmunities.join(', ')}
          </div>
        )}
        {data.senses && data.senses.length > 0 && (
          <div>
            <span className="font-bold text-[hsl(var(--primary))]">Senses</span>{' '}
            {data.senses.join(', ')}
          </div>
        )}
        {data.languages && data.languages.length > 0 && (
          <div>
            <span className="font-bold text-[hsl(var(--primary))]">Languages</span>{' '}
            {data.languages.join(', ')}
          </div>
        )}
        {data.cr && (
          <div>
            <span className="font-bold text-[hsl(var(--primary))]">Challenge</span>{' '}
            {data.cr} ({data.xp?.toLocaleString()} XP)
          </div>
        )}
      </div>
    </div>
  );
}
