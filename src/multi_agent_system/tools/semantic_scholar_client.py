"""Semantic Scholar Graph API client."""

from dataclasses import dataclass

import httpx

from multi_agent_system.schemas.messages import Citation


@dataclass
class SemanticScholarClient:
    """Client for Semantic Scholar paper search."""

    base_url: str = "https://api.semanticscholar.org/graph/v1"
    timeout_seconds: float = 20.0

    def search(self, query: str, max_results: int = 20) -> list[Citation]:
        """Search Semantic Scholar and return structured citations."""
        with httpx.Client(timeout=self.timeout_seconds) as client:
            response = client.get(
                f"{self.base_url}/paper/search",
                params={
                    "query": query,
                    "limit": max_results,
                    "fields": "title,abstract,authors,externalIds,url",
                },
            )
            response.raise_for_status()

        data = response.json().get("data", [])
        citations: list[Citation] = []

        for paper in data:
            external_ids = paper.get("externalIds") or {}
            doi = external_ids.get("DOI")
            pmid = external_ids.get("PubMed")
            authors = [
                author.get("name", "")
                for author in paper.get("authors", [])
                if author.get("name")
            ]
            citations.append(
                Citation(
                    source="Semantic Scholar",
                    pmid=str(pmid) if pmid else None,
                    title=paper.get("title", ""),
                    abstract=paper.get("abstract") or "",
                    authors=authors,
                    doi=str(doi) if doi else None,
                )
            )

        return citations
