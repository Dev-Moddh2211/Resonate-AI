import json
from pathlib import Path
from .embeddings import EmbeddingProvider, cosine

class VectorIndex:
    def __init__(self, entries, provider=None): self.entries=entries; self.provider=provider or EmbeddingProvider()
    @classmethod
    def build(cls, chunks):
        p=EmbeddingProvider(); vectors=p.embed_documents([x["title"]+" "+x["section"]+" "+x["content"] for x in chunks])
        return cls([{"embedding":v,"chunk_id":c["chunk_id"],"record_id":c["record_id"],"source_id":c["source_id"],"metadata":c} for v,c in zip(vectors,chunks)],p)
    def search(self, query, top_k=5, category=None):
        q=self.provider.embed_query(query); found=[]
        for e in self.entries:
            if category and e["metadata"]["category"] != category: continue
            found.append((cosine(q,e["embedding"]),e))
        found.sort(key=lambda x:x[0],reverse=True)
        return [{**e["metadata"],"semantic_score":round(max(0.0,score),4)} for score,e in found[:top_k]]
    def save(self,path): Path(path).write_text(json.dumps({"model":self.provider.model,"dimensions":self.provider.dimensions,"entries":self.entries},indent=2))
