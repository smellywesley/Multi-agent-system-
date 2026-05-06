export type Citation = {
  title: string;
  doi?: string | null;
  source: string;
};

export type SynthesisReport = {
  clinical_consensus: string;
  conflicting_findings: string[];
  overall_evidence_quality: string;
  clinical_recommendation: string;
};

export type ResearchResponse = {
  content: string;
  citations: Citation[];
  synthesis?: SynthesisReport | null;
};

export async function runResearch(task: string): Promise<ResearchResponse> {
  const response = await fetch("/api/research", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-API-KEY": process.env.NEXT_PUBLIC_INTERNAL_API_SECRET ?? ""
    },
    body: JSON.stringify({ task })
  });

  if (!response.ok) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return (await response.json()) as ResearchResponse;
}
