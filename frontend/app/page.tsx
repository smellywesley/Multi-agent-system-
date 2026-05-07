"use client";
import { motion, AnimatePresence } from "framer-motion";
import { useState } from "react";
import ReactMarkdown from "react-markdown";
import { Search, BrainCircuit, FlaskConical, ChevronDown, Download } from "lucide-react";

export default function Page() {
  const [query, setQuery] = useState("");
  const [isSearching, setIsSearching] = useState(false);
  const [result, setResult] = useState(null);

  const handleSearch = async () => {
    if (!query) return;
    setIsSearching(true);
    setResult(null);
    try {
      const res = await fetch("/api/research", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task: query }),
      });
      const data = await res.json();
      setResult(data);
    } catch (e) { console.error(e); }
    finally { setIsSearching(false); }
  };

  return (
    <main className="min-h-screen bg-[#04060e] text-slate-100 p-8">
      <div className="max-w-4xl mx-auto">
        <motion.div layout className={`flex flex-col ${result || isSearching ? 'items-start' : 'items-center justify-center min-h-[60vh]'}`}>
          <div className="flex items-center gap-3 mb-8">
            <FlaskConical className="text-sky-400" />
            <h1 className="text-xl font-bold">Biomedical Intelligence</h1>
          </div>
          <div className="w-full max-w-2xl flex gap-2 bg-white/5 p-2 rounded-2xl border border-white/10">
            <input 
              className="flex-1 bg-transparent outline-none px-4" 
              placeholder="What research are you looking for?"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSearch()}
            />
            <button onClick={handleSearch} className="bg-sky-500 text-black px-4 py-2 rounded-xl font-bold">Search</button>
          </div>
        </motion.div>

        {isSearching && (
          <motion.div initial={{opacity:0}} animate={{opacity:1}} className="mt-20 text-center">
            <BrainCircuit className="w-12 h-12 text-sky-400 mx-auto animate-pulse" />
            <p className="mt-4 text-sky-400">Agents are synthesizing consensus...</p>
          </motion.div>
        )}

        {result && !isSearching && (
          <motion.div initial={{opacity:0, y:20}} animate={{opacity:1, y:0}} className="mt-12 p-8 bg-white/5 border border-white/10 rounded-3xl">
             <div className="prose prose-invert max-w-none">
                <ReactMarkdown>{result.content || result.synthesis?.clinical_consensus}</ReactMarkdown>
             </div>
          </motion.div>
        )}
      </div>
    </main>
  );
}
