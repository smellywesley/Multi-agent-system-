"use client";

import { motion } from "framer-motion";
import { ChevronDown } from "lucide-react";
import { useState } from "react";

import type { Citation } from "@/lib/api";

export function CitationsAccordion({ citations }: { citations: Citation[] }) {
  return (
    <div className="space-y-3">
      {citations.map((citation) => (
        <CitationItem key={`${citation.title}-${citation.doi ?? "na"}`} citation={citation} />
      ))}
    </div>
  );
}

function CitationItem({ citation }: { citation: Citation }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="glass overflow-hidden rounded-2xl">
      <button
        className="flex w-full items-center justify-between px-4 py-3 text-left"
        onClick={() => setOpen((previous) => !previous)}
        type="button"
      >
        <span className="text-sm text-slate-100">{citation.title}</span>
        <motion.span animate={{ rotate: open ? 180 : 0 }}>
          <ChevronDown className="h-4 w-4 text-slate-400" />
        </motion.span>
      </button>
      <motion.div
        initial={false}
        animate={{ height: open ? "auto" : 0, opacity: open ? 1 : 0 }}
        className="px-4"
      >
        <div className="pb-4 text-xs text-slate-300">
          <p>DOI: {citation.doi || "N/A"}</p>
          <p>Source: {citation.source}</p>
        </div>
      </motion.div>
    </div>
  );
}
