# Chunking strategy

Extraction first creates sections from headings, CSV rows, or JSON records. Each non-empty section becomes a semantic chunk; FAQ question/answer sections and table rows remain intact. No fixed character slicing or overlap is used because these prototype sections are already short and splitting policy meaning would be unsafe. Longer approved documents should split only at paragraph boundaries while retaining the parent heading and page.
