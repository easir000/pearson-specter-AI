def generate_memo(query: str, evidence: list) -> dict:
    facts_set = set()
    citations = []

    for e in evidence:
        if e["metadata"]["plaintiff"] != "UNKNOWN":
            facts_set.add(f"Plaintiff: {e['metadata']['plaintiff']}")
        if e["metadata"]["defendant"] != "UNKNOWN":
            facts_set.add(f"Defendant: {e['metadata']['defendant']}")
        if "v." in e["text"]:
            citations.append(e["text"].split("v.")[0].strip()[-20:] + " v. ...")
    
    facts = sorted(facts_set)  # deterministic order

    return {
        "query": query,
        "facts": facts,
        "citations": citations,
        "draft": (
            f"RE: {query}\n\n"
            f"FACTS:\n" + "\n".join(f"- {f}" for f in facts) + "\n\n"
            f"CITATIONS:\n" + "\n".join(f"- {c}" for c in citations)
        ),
        "evidence_used": [e["doc_id"] for e in evidence]
    }