import json
from pathlib import Path
from .pipeline import build_index
from .retrieval import Retriever

def main():
    build_index(); r=Retriever.load(); cases=json.loads(Path("evaluation/retrieval_tests.json").read_text()); results=[]
    for case in cases:
        out=r.search(case["user_question"]); actual=out["results"][0]["source_id"] if out["results"] else None
        verdict="correct" if actual==case.get("expected_source") else "incorrect" if actual is not None else "partially_correct"
        results.append({**case,"retrieved_source":actual,"retrieved_record":out["results"][0]["record_id"] if out["results"] else None,"score":out["results"][0]["score"] if out["results"] else None,"verdict":verdict,"relevance_explanation":"Top lexical overlap with normalized query; score is not a probability."})
    Path("evaluation/retrieval_results.json").write_text(json.dumps(results,indent=2))
if __name__ == "__main__": main()
