import json, hashlib
from pathlib import Path
from .extraction import extract
from .chunking import make_chunks
from .processing import near_duplicate
from .vector_index import VectorIndex

ROOT=Path(__file__).parents[1]
def build_index(raw=ROOT/"data/raw/synthetic", out=ROOT/"data/processed"):
    manifest=json.loads((raw/"manifest.json").read_text()); all_chunks=[]; report={"sources_processed":0,"sources_failed":0,"records_created":0,"chunks_created":0,"pii_records_flagged":0,"duplicates_found":0,"near_duplicates_found":0,"errors":[]}
    seen=[]; near_pairs=[]
    for source in manifest:
        try:
            doc=extract(str(raw/source["filename"])); chunks=make_chunks(doc,source,source["category"],source.get("tags",[])); report["sources_processed"]+=1; report["records_created"]+=len(chunks); report["chunks_created"]+=len(chunks); report["pii_records_flagged"] += sum(c.pii for c in chunks)
            for c in chunks:
                digest=hashlib.sha256(c.content.encode()).hexdigest(); c.tags.append("content_sha256:"+digest[:12]);
                if any(x.content.casefold()==c.content.casefold() for x in seen): report["duplicates_found"]+=1
                elif any(near_duplicate(x.content,c.content) for x in seen): report["near_duplicates_found"]+=1; near_pairs.append({"new_chunk":c.chunk_id,"decision":"REVIEW_REQUIRED"})
                all_chunks.append(c.to_dict()); seen.append(c)
        except Exception as e: report["sources_failed"]+=1; report["errors"].append({"source_id":source["source_id"],"error":str(e)})
    out.mkdir(parents=True,exist_ok=True); (out/"chunks.json").write_text(json.dumps(all_chunks,indent=2),encoding="utf-8"); VectorIndex.build(all_chunks).save(out/"vector_index.json"); report["vectors_indexed"]=len(all_chunks); report["embeddings_generated"]=len(all_chunks); report["near_duplicate_review"] = near_pairs; (out/"processing_report.json").write_text(json.dumps(report,indent=2),encoding="utf-8"); return report
