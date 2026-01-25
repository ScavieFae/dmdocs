import { anthropic } from '@ai-sdk/anthropic';
import { streamText, createUIMessageStreamResponse } from 'ai';

export const maxDuration = 30;

export async function POST(req: Request) {
  const { messages } = await req.json();

  // System prompt with D&D context
  const systemPrompt = `You are a helpful D&D 5th Edition rules assistant for DMDocs, a site containing the System Reference Document (SRD) 5.2.1.

You help answer questions about:
- Game rules and mechanics
- Spells and their effects
- Monsters and their stat blocks
- Magic items and their properties
- Character classes and abilities

Be concise and accurate. Reference specific rules when relevant. If you're unsure about something, say so rather than guessing.

Keep responses focused and practical for players and DMs at the table.`;

  const result = streamText({
    model: anthropic('claude-3-5-haiku-latest'),
    system: systemPrompt,
    messages,
  });

  return createUIMessageStreamResponse({
    stream: result.toUIMessageStream(),
  });
}
