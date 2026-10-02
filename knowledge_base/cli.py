import argparse, json
from .pipeline import build_index
from .retrieval import Retriever
def main():
    p=argparse.ArgumentParser(); p.add_argument("query",nargs="?"); args=p.parse_args()
    if not __import__("pathlib").Path("data/processed/chunks.json").exists(): build_index()
    print(json.dumps(Retriever.load().search(args.query or "What documents are required?"),indent=2))
if __name__ == "__main__": main()
