import Link from "next/link";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-4">DND Axis</h1>
      <p className="text-xl text-gray-600 dark:text-gray-400 mb-8">
        LLM-Optimized D&D 5e System Reference Document
      </p>
      <Link
        href="/docs"
        className="px-6 py-3 bg-red-700 text-white rounded-lg hover:bg-red-800 transition"
      >
        Enter the SRD
      </Link>
      <p className="mt-8 text-sm text-gray-500 max-w-md text-center">
        Based on SRD 5.2.1 by Wizards of the Coast LLC, licensed under CC-BY-4.0
      </p>
    </main>
  );
}
