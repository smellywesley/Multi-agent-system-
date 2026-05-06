"""PubMed E-utilities client."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from dataclasses import dataclass

import httpx

from multi_agent_system.schemas.messages import Citation


@dataclass
class PubMedClient:
    """Client for PubMed ESearch + EFetch operations."""

    base_url: str = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    timeout_seconds: float = 20.0

    def search(self, query: str, max_results: int = 20) -> list[Citation]:
        pmids = self._esearch(query=query, max_results=max_results)
        if not pmids:
            return []
        return self._efetch(pmids)

    def _esearch(self, query: str, max_results: int) -> list[str]:
        with httpx.Client(timeout=self.timeout_seconds) as client:
            response = client.get(
                f"{self.base_url}/esearch.fcgi",
                params={"db": "pubmed", "retmode": "json", "retmax": max_results, "term": query},
            )
            response.raise_for_status()
        payload = response.json()
        return payload.get("esearchresult", {}).get("idlist", [])

    def _efetch(self, pmids: list[str]) -> list[Citation]:
        with httpx.Client(timeout=self.timeout_seconds) as client:
            response = client.get(
                f"{self.base_url}/efetch.fcgi",
                params={"db": "pubmed", "retmode": "xml", "id": ",".join(pmids)},
            )
            response.raise_for_status()

        root = ET.fromstring(response.text)
        citations: list[Citation] = []

        for article in root.findall(".//PubmedArticle"):
            pmid = self._text(article.find(".//PMID"))
            title = self._text(article.find(".//ArticleTitle"))
            abstract_segments = [
                self._text(node)
                for node in article.findall(".//Abstract/AbstractText")
                if self._text(node)
            ]
            abstract = " ".join(abstract_segments).strip()
            authors = self._authors(article)
            doi = self._doi(article)
            citations.append(
                Citation(
                    source="PubMed",
                    pmid=pmid or None,
                    title=title,
                    abstract=abstract,
                    authors=authors,
                    doi=doi,
                )
            )

        return citations

    @staticmethod
    def _text(node: ET.Element | None) -> str:
        if node is None:
            return ""
        return "".join(node.itertext()).strip()

    def _authors(self, article: ET.Element) -> list[str]:
        names: list[str] = []
        for author in article.findall(".//AuthorList/Author"):
            last_name = self._text(author.find("LastName"))
            initials = self._text(author.find("Initials"))
            collective = self._text(author.find("CollectiveName"))
            if collective:
                names.append(collective)
            elif last_name:
                names.append(f"{last_name} {initials}".strip())
        return names

    def _doi(self, article: ET.Element) -> str | None:
        for id_node in article.findall(".//ArticleIdList/ArticleId"):
            if id_node.attrib.get("IdType") == "doi":
                doi_value = self._text(id_node)
                if doi_value:
                    return doi_value
        return None
