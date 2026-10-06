# SWYNEX — Model or API Integration

**Task 2 · Numan Qureshi · Research-paper Q&A prototype**

A runnable local prototype that integrates **scikit-learn** to retrieve evidence and return extractive answers from research notes associated with the five papers selected in Task 1. No API key is required.

## What is implemented

- `TfidfVectorizer` converts source notes and questions into sparse vectors.
- `cosine_similarity` ranks evidence by lexical relevance.
- Sentence ranking selects up to two sentences from the best note as an extractive response.
- Each response links its evidence to the original paper and labels it as a paraphrased abstract note.
- A relevance/term-coverage heuristic declines weak matches.
- A local browser interface supports paper filtering, example questions, source inspection, and request validation.

**Scope:** This is a library-integration baseline, not the complete generative RAG system proposed in Task 1. It indexes five short, human-prepared paraphrased notes, not five full PDFs. No pretrained language model, dense embeddings, LLM API, full-document extraction, or automatic citation-entailment verifier is included. Scores are not confidence probabilities. Abstention is a heuristic and can fail on misleading questions with overlapping words.

## Run on Windows (PowerShell)

Install Python 3.10 or newer, open the extracted project folder, then run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Open **http://127.0.0.1:8000** in your browser. No activation command is needed. The first installation requires internet; after dependencies are installed, the prototype runs offline. Opening original paper links requires internet.

For macOS/Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

If port 8000 is occupied, run `app.py --port 8001` and open port 8001 instead. Ctrl+C stops the server. The server binds only to localhost; it is a local demo, not a hardened public hosting service.

## Example inputs and actual outputs

Run these commands from the project folder:

```powershell
.\.venv\Scripts\python.exe demo.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

`examples/actual_outputs.json` contains actual outputs captured during development, library/runtime versions, source citations, scores, and timing. Re-running `demo.py` regenerates it; timing depends on the machine. Demo questions were used in development and are **not** a held-out accuracy benchmark. The Task 1 evaluation targets have not been demonstrated.

Try “What similarity measure does Sentence-BERT use?” and inspect the cosine-similarity sentence and source link. Then try “What is the latest 2026 benchmark score for this assistant?” to demonstrate an unsupported query.

## API

`GET /health` — status and corpus size.  
`GET /api/papers` — available source metadata.  
`POST /api/ask` — JSON object with `question` and optional `paper_id` (P01–P05).

```json
{"question":"What similarity measure does Sentence-BERT use?","paper_id":"P01"}
```

Returns `answer`, `abstained`, `citations`, `retrieval_score`, `term_coverage`, `related_sources`, `elapsed_ms`, and the integration mode. Invalid/empty questions return HTTP 400. Source text and responses are rendered as text in the UI, not inserted as HTML.

## Sources and provenance

`data/papers.json` contains original paraphrases of abstracts, prepared on 6 October 2026. These notes are human-authored inputs, not model-generated outputs. They preserve only a small portion of each paper's content; source links resolve to the original work. PDF page numbers are not claimed because PDFs are not indexed.

1. Sentence-BERT — https://arxiv.org/abs/1908.10084
2. Dense Passage Retrieval — https://arxiv.org/abs/2004.04906
3. Retrieval-Augmented Generation — https://arxiv.org/abs/2005.11401
4. REALM — https://arxiv.org/abs/2002.08909
5. Lost in the Middle — https://arxiv.org/abs/2307.03172

Library documentation: https://scikit-learn.org/stable/modules/feature_extraction.html

## Validation and limitations

Unit checks cover relevant answers, source selection, an unsupported query, scope filtering, and invalid inputs. An HTTP smoke check covers health, query submission, and HTTP 400 validation. This is verification of prototype behavior, not proof of reliability on unseen research questions.

TF-IDF primarily matches vocabulary, so paraphrases, comparisons, negation, and questions outside the notes can fail. The prototype returns evidence extracts, not a synthesized multi-paper answer. A sensible next step is indexing permitted full PDFs, testing BM25/dense retrieval on separate development and held-out questions, then adding and evaluating an evidence-bound generator.

## Security and submission

No credentials are included or required. `.env`, virtual environments, and caches are ignored by Git. Upload the repository files, not `.venv`.

Create a public repository named `SWYNEX-Model-or-API-Integration`, upload these files, and verify the README is accessible while signed out. Publish a LinkedIn explanation mentioning the official SWYNEX Technologies page. Attach a screenshot or short video of the **running prototype** showing a question, answer, and source. Submit the actual repository URL and LinkedIn post URL to the task portal. Publishing and portal submission must be completed from your accounts.
