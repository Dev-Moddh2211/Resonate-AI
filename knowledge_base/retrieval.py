import json, math, re, time
from pathlib import Path
from .vector_index import VectorIndex

STOP = {"what","is","are","the","a","an","do","i","for","to","and","of","my","can","how","please","tell","me","about"}
class Retriever:
    def __init__(self, chunks: list[dict], threshold: float = .12):
        self.chunks, self.threshold, self.vector = chunks, threshold, VectorIndex.build(chunks)
    @classmethod
    def load(cls, path="data/processed/chunks.json"):
        return cls(json.loads(Path(path).read_text()))
    def search(self, query: str, top_k=5, category=None):
        started=time.perf_counter(); q=set(re.findall(r"\w+", query.casefold()))-STOP
        scored=[]
        for c in self.chunks:
            if category and c["category"] != category: continue
            words=set(re.findall(r"\w+", (c["title"]+" "+c["section"]+" "+c["content"]).casefold()))-STOP
            overlap=len(q & words)/max(1, len(q | words)); exact=sum(1 for term in q if term in c["content"].casefold())/max(1,len(q))
            score=min(1.0, .55*overlap+.25*exact)
            scored.append((score,c))
        semantic={x["chunk_id"]:x["semantic_score"] for x in self.vector.search(query, max(top_k*3,10), category)}
        lexical={c["chunk_id"]:s for s,c in scored}
        # Hybrid score: lexical 50%, semantic 35%, question/heading match 15%.
        def category_signal(c):
            if q & {"document","documents","paper","papers"} and c["category"] in {"faq","documents"}: return .12
            if q & {"guarantee","guaranteed","approval"} and c["category"] in {"faq","objection"}: return .12
            if q & {"eligible","qualification","review"} and c["category"] == "qualification": return .12
            return 0
        scored=[(min(1.0,.50*s+.35*semantic.get(c["chunk_id"],0)+.15*(1 if any(t in c["section"].casefold() for t in q) else 0)+category_signal(c)),c) for s,c in scored]
        scored=[x for x in scored if x[0] >= self.threshold and (lexical.get(x[1]["chunk_id"],0) >= self.threshold or semantic.get(x[1]["chunk_id"],0) >= .45)]
        scored.sort(key=lambda x:x[0], reverse=True)
        results=[]
        for score,c in scored[:top_k]:
            confidence="high" if score >= .35 and c["authority_level"] in {"official","approved_internal"} else "medium" if score >= .22 else "low"
            results.append({"record_id":c["record_id"],"chunk_id":c["chunk_id"],"content":c["content"],"score":round(score,4),"confidence":confidence,"source":c["source"],"source_id":c["source_id"],"page":c.get("page"),"version":c["version"],"effective_at":c.get("effective_date"),"metadata":c})
        return {"query":query,"status":"results" if results else "no_trusted_result","results":results,"candidate_count":len(scored),"latency_ms":round((time.perf_counter()-started)*1000,2)}
