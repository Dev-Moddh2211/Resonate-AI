"""Replaceable local embedding provider.

The default is a deterministic hashed bag-of-words/character-ngram embedding.
It is a real dense vector representation with no network or credential
requirement, suitable for this small prototype; an API or sentence-transformer
provider can implement the same interface later.
"""
import hashlib, math, re

class EmbeddingProvider:
    dimensions = 256
    model = "local-hash-embedding-v1"
    def _embed(self, text):
        v=[0.0]*self.dimensions
        tokens=re.findall(r"[a-z0-9]+", text.casefold())
        tokens += [text.casefold()[i:i+3] for i in range(max(0,len(text)-2))]
        for token in tokens:
            h=int(hashlib.blake2b(token.encode(),digest_size=8).hexdigest(),16)
            v[h % self.dimensions] += 1.0 if h % 2 else -1.0
        norm=math.sqrt(sum(x*x for x in v)) or 1.0
        return [round(x/norm,8) for x in v]
    def embed_documents(self, texts): return [self._embed(x) for x in texts]
    def embed_query(self, text): return self._embed(text)

def cosine(a,b): return sum(x*y for x,y in zip(a,b))
