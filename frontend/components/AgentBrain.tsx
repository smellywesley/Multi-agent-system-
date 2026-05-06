"use client";

import { motion } from "framer-motion";
import { BrainCircuit } from "lucide-react";

const steps = [
  "Formulating PICO query...",
  "Scouring PubMed & Semantic Scholar...",
  "Reading and structuring clinical abstracts...",
  "Synthesizing consensus..."
];

export function AgentBrain() {
  return (
    <motion.div
      className="glass mx-auto w-full max-w-3xl rounded-3xl p-6"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      <div className="mb-6 flex items-center gap-3 text-sky-300">
        <BrainCircuit className="h-5 w-5" />
        <p className="text-sm font-medium">Agent Brain Active</p>
      </div>
      <motion.ul
        className="space-y-4"
        initial="hidden"
        animate="show"
        variants={{
          hidden: {},
          show: {
            transition: { staggerChildren: 0.5 }
          }
        }}
      >
        {steps.map((step) => (
          <motion.li
            key={step}
            className="flex items-center gap-3"
            variants={{
              hidden: { opacity: 0.2, x: -8 },
              show: { opacity: 1, x: 0 }
            }}
          >
            <motion.span
              className="h-3 w-3 rounded-full bg-sky-400"
              animate={{ scale: [1, 1.3, 1], opacity: [0.5, 1, 0.5] }}
              transition={{ repeat: Number.POSITIVE_INFINITY, duration: 1.4 }}
            />
            <span className="text-sm text-slate-200">{step}</span>
          </motion.li>
        ))}
      </motion.ul>
    </motion.div>
  );
}
