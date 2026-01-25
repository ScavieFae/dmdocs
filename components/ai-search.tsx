"use client";

import { useChat } from "@ai-sdk/react";
import { useState, FormEvent, useEffect } from "react";
import { createPortal } from "react-dom";
import { Sparkles, X, Send, Loader2 } from "lucide-react";

export function AISearchTrigger() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className="flex items-center gap-1.5 px-3 py-1.5 text-sm rounded-md bg-fd-primary/10 text-fd-primary hover:bg-fd-primary/20 transition-colors"
      >
        <Sparkles className="h-4 w-4" />
        Ask AI
      </button>
      {open && <AISearchDialog onClose={() => setOpen(false)} />}
    </>
  );
}

function AISearchDialog({ onClose }: { onClose: () => void }) {
  const { messages, sendMessage, status } = useChat();
  const [input, setInput] = useState("");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const isLoading = status === "streaming" || status === "submitted";

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;
    sendMessage({ content: input, role: "user" });
    setInput("");
  };

  // Extract text content from message parts
  const getMessageContent = (msg: typeof messages[0]) => {
    if (typeof msg.content === "string") return msg.content;
    // Handle parts array format
    const parts = msg.parts;
    if (!parts) return "";
    return parts
      .filter((p): p is { type: "text"; text: string } => p.type === "text")
      .map((p) => p.text)
      .join("");
  };

  const dialog = (
    <div className="fixed inset-0 z-[100] flex items-center justify-center">
      {/* Backdrop */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={onClose}
      />

      {/* Dialog */}
      <div className="relative w-full max-w-2xl max-h-[80vh] mx-4 bg-fd-background border border-fd-border rounded-xl shadow-2xl flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3 border-b border-fd-border">
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-fd-primary" />
            <span className="font-medium">Ask AI about D&D 5e</span>
          </div>
          <button
            onClick={onClose}
            className="p-1 rounded hover:bg-fd-muted transition-colors"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-[300px]">
          {messages.length === 0 && (
            <div className="text-center text-fd-muted-foreground py-8">
              <p className="mb-2">Ask me anything about D&D 5e rules!</p>
              <p className="text-sm">Try: &quot;How does grappling work?&quot; or &quot;What does a Fireball spell do?&quot;</p>
            </div>
          )}
          {messages.map((m) => (
            <div
              key={m.id}
              className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}
            >
              <div
                className={`max-w-[85%] rounded-lg px-4 py-2 ${
                  m.role === "user"
                    ? "bg-fd-primary text-fd-primary-foreground"
                    : "bg-fd-muted"
                }`}
              >
                <div className="text-sm whitespace-pre-wrap">{getMessageContent(m)}</div>
              </div>
            </div>
          ))}
          {isLoading && messages[messages.length - 1]?.role === "user" && (
            <div className="flex justify-start">
              <div className="bg-fd-muted rounded-lg px-4 py-2">
                <Loader2 className="h-4 w-4 animate-spin" />
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <form onSubmit={handleSubmit} className="p-4 border-t border-fd-border">
          <div className="flex gap-2">
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about spells, monsters, rules..."
              className="flex-1 px-4 py-2 bg-fd-muted border border-fd-border rounded-lg focus:outline-none focus:ring-2 focus:ring-fd-primary text-sm"
              autoFocus
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="px-4 py-2 bg-fd-primary text-fd-primary-foreground rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              <Send className="h-4 w-4" />
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  // Use portal to render at document body level
  if (!mounted) return null;
  return createPortal(dialog, document.body);
}
