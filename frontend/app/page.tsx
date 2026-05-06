"use client";

import { motion } from "framer-motion";
import { FlaskConical, Search } from "lucide-react";
import { useState } from "react";
import ReactMarkdown from "react-markdown";

import { AgentBrain } from "@/components/AgentBrain";
import { CitationsAccordion } from "@/components/CitationsAccordion";
import { runResearch, type ResearchResponse } from "@/lib/api";

export default function Page() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<ResearchResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const hasResults = result !== null;

  const onSubmit = async () => {
    if (!query.trim()) {
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await runResearch(query);
      setResult(data);
    } catch (submitError) {
      setError(submitError instanceof Error ? submitError.message : "Unexpected error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="mx-auto flex min-h-screen w-full max-w-6xl flex-col px-6 py-10">
      <motion.section
        layout
        className={hasResults ? "mb-8" : "my-auto"}
        transition={{ type: "spring", stiffness: 120, damping: 22 }}
      >
        <motion.div layoutId="omnibar" className="glass rounded-3xl p-5 shadow-glow">
          <div className="mb-4 flex items-center gap-2 text-slate-300">
            <FlaskConical className="h-5 w-5 text-sky-300" />
            <h1 className="text-xl font-semibold tracking-tight">Biomedical Research Intelligence</h1>
          </div>
          <div className="flex gap-3">
            <input
              className="w-full rounded-2xl border border-white/10 bg-slate-900/60 px-4 py-3 text-slate-100 outline-none transition focus:border-sky-300/70 focus:shadow-glow"
              placeholder="Analyze CRISPR for sickle cell..."
              value={query}
              onChange={(event) => setQuery(event.target.value)}
            />
            <button
              className="rounded-2xl bg-sky-400 px-5 text-slate-950 transition hover:bg-sky-300 disabled:opacity-50"
              onClick={() => {
                void onSubmit();
              }}
              type="button"
              disabled={loading}
            >
              <Search className="h-5 w-5" />
            </button>
          </div>
        </motion.div>
      </motion.section>

      {loading && <AgentBrain />}
      {error && <p className="mt-4 text-sm text-rose-300">{error}</p>}

      {result && !loading && (
        <motion.section
          className="space-y-6"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <div className="glass rounded-3xl p-6">
            <h2 className="mb-2 text-sm uppercase tracking-[0.2em] text-slate-400">Clinical Consensus</h2>
            <p className="text-lg font-semibold text-slate-100">
              {result.synthesis?.clinical_consensus || "Consensus unavailable"}
            </p>
            <p className="mt-3 text-sm text-slate-300">
              Recommendation: {result.synthesis?.clinical_recommendation || "Not provided"}
            </p>
          </div>

          <article className="glass prose prose-invert max-w-none rounded-3xl p-6 prose-p:text-slate-200">
            <ReactMarkdown>{result.content}</ReactMarkdown>
          </article>

          <section>
            <h3 className="mb-3 text-sm uppercase tracking-[0.2em] text-slate-400">Source Citations</h3>
            <CitationsAccordion citations={result.citations} />
          </section>
        </motion.section>
      )}
    </main>
  );
}
