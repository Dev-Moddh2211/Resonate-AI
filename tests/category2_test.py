import json, unittest
from pathlib import Path
from knowledge_base.pipeline import build_index
from knowledge_base.retrieval import Retriever
from knowledge_base.extraction import extract
from knowledge_base.processing import clean, pii_findings, similarity
from knowledge_base.embeddings import EmbeddingProvider
from knowledge_base.vector_index import VectorIndex

class Category2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        build_index(); cls.r=Retriever.load()
    def test_extraction_and_cleaning(self):
        d=extract("data/raw/synthetic/product.md"); self.assertTrue(d["sections"]); self.assertNotIn("Menu", clean("Menu\nuseful text"))
    def test_duplicates_and_similarity_helpers(self):
        self.assertEqual(similarity("loan amount required", "required loan amount"),1.0)
    def test_pii_is_detected_and_redacted_in_index(self):
        self.assertTrue(pii_findings(Path("data/raw/synthetic/pii_form.md").read_text()))
        self.assertFalse(any("priya.example@example.test" in c["content"] for c in self.r.chunks))
    def test_retrieval_has_contract_metadata(self):
        out=self.r.search("What documents are needed?"); self.assertEqual(out["status"],"results")
        result=out["results"][0]; self.assertIn("source_id",result); self.assertIn("version",result); self.assertIn("metadata",result)
    def test_unknown_returns_no_trusted_result(self):
        self.assertEqual(self.r.search("quantum gardening on Mars")["status"],"no_trusted_result")
    def test_embedding_and_vector_retrieval(self):
        p=EmbeddingProvider(); self.assertEqual(len(p.embed_query("loan")),p.dimensions)
        self.assertTrue(VectorIndex.build(self.r.chunks).search("loan", 1)[0]["chunk_id"])
    def test_evaluation_cases_have_five_required(self):
        cases=json.loads(Path("evaluation/retrieval_tests.json").read_text()); self.assertGreaterEqual(len(cases),5)

if __name__ == "__main__": unittest.main()
