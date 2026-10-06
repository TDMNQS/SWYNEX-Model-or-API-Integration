"""Local scikit-learn library integration; evidence retrieval, not an LLM."""
import json
import re
import time
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_PATH = Path(__file__).parent / 'data' / 'papers.json'


def normalize(text):
    text = text.lower()
    return re.sub(r'\b(?:training|trained|trains)\b', 'train', text)


class PaperAssistant:
    def __init__(self, data_path=DATA_PATH):
        self.papers = json.loads(Path(data_path).read_text(encoding='utf-8'))
        if not self.papers or any(not p.get('text', '').strip() for p in self.papers):
            raise ValueError('Corpus must contain non-empty source notes.')
        self.vectorizer = TfidfVectorizer(preprocessor=normalize, stop_words='english', ngram_range=(1, 2), sublinear_tf=True)
        self.matrix = self.vectorizer.fit_transform([p['text'] for p in self.papers])
        self.analyze = self.vectorizer.build_analyzer()

    def ask(self, question, paper_id=None):
        start = time.perf_counter()
        if not isinstance(question, str) or not question.strip():
            raise ValueError('Please enter a question.')
        question = question.strip()
        if len(question) > 1000:
            raise ValueError('Question must be at most 1,000 characters.')
        if paper_id and paper_id not in {p['id'] for p in self.papers}:
            raise ValueError('Unknown paper identifier.')
        q = self.vectorizer.transform([question])
        scores = cosine_similarity(q, self.matrix).ravel()
        candidates = [i for i, p in enumerate(self.papers) if not paper_id or p['id'] == paper_id]
        candidates.sort(key=lambda i: (-float(scores[i]), self.papers[i]['id']))
        terms = {t for t in self.analyze(question) if ' ' not in t}
        corpus_terms = set(self.vectorizer.get_feature_names_out())
        coverage = len(terms & corpus_terms) / max(1, len(terms))
        best = candidates[0]
        # Development heuristic, not a calibrated confidence estimate.
        abstained = float(scores[best]) < 0.12 or coverage < 0.45
        citations = []
        answer = 'I cannot answer this from the included research notes. Try a question about their methods or limitations.'
        if not abstained:
            paper = self.papers[best]
            sentences = re.split(r'(?<=[.!?])\s+', paper['text'])
            # Remove paper-name terms so topic words drive sentence selection.
            aliases = {'P01':'sentence-bert', 'P02':'dense passage retrieval',
                       'P03':'retrieval-augmented generation', 'P04':'realm', 'P05':'lost in the middle'}
            focused = re.sub(re.escape(aliases[paper['id']]), '', question, flags=re.I)
            sentence_q = self.vectorizer.transform([focused])
            if sentence_q.nnz == 0:
                sentence_q = q
            sentence_matrix = self.vectorizer.transform(sentences)
            sentence_scores = cosine_similarity(sentence_q, sentence_matrix).ravel()
            selected = sorted(sorted(range(len(sentences)), key=lambda i: -float(sentence_scores[i]))[:2])
            answer = ' '.join(sentences[i] for i in selected)
            citations = [{'paper_id':paper['id'], 'title':paper['title'], 'url':paper['url'],
                          'section':paper['section'], 'evidence':answer}]
        return {'question':question, 'answer':answer, 'abstained':abstained,
                'citations':citations, 'retrieval_score':round(float(scores[best]), 4),
                'term_coverage':round(coverage, 4),
                'related_sources':[{'paper_id':self.papers[i]['id'], 'title':self.papers[i]['title'],
                                    'score':round(float(scores[i]), 4)} for i in candidates[:3]],
                'elapsed_ms':round((time.perf_counter()-start)*1000, 2),
                'mode':'TF-IDF retrieval + extractive answer from paraphrased notes'}
