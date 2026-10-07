"""Small development evaluation with expected sources and failure cases."""
import json
import platform
from pathlib import Path
import sklearn
from engine import PaperAssistant

CASES = [
    {'id':'S01','category':'single','question':'What similarity measure does Sentence-BERT use?','expected_sources':['P01'],'contains':'cosine similarity'},
    {'id':'S02','category':'single','question':'How does REALM train its retriever?','expected_sources':['P04'],'contains':'Masked language modeling'},
    {'id':'C01','category':'compare','question':'retriever','paper_ids':['P03','P04'],'expected_sources':['P03','P04']},
    {'id':'C02','category':'compare','question':'question answering','paper_ids':['P02','P04'],'expected_sources':['P02','P04']},
    {'id':'C03','category':'compare','question':'cosine similarity','paper_ids':['P01','P04'],'expected_abstain':True,'missing':['P04']},
    {'id':'C04','category':'compare','question':'2026 subscription price','paper_ids':['P03','P04'],'expected_abstain':True,'missing':['P03','P04']},
    {'id':'U01','category':'single','question':'What is the latest 2026 benchmark score for this assistant?','expected_abstain':True},
    {'id':'U02','category':'single','question':'What is the capital of France?','expected_abstain':True},
    {'id':'E01','category':'error','question':'retriever','paper_ids':['P01','P01'],'expected_error':True},
    {'id':'E02','category':'error','question':'','paper_ids':['P03','P04'],'expected_error':True},
    {'id':'E03','category':'error','question':'retriever','paper_ids':['P03','P99'],'expected_error':True},
    # Challenge probes are scored honestly, even if a lexical heuristic fails.
    {'id':'F01','category':'challenge','question':'Does REALM use cosine similarity?','expected_abstain':True},
    {'id':'F02','category':'challenge','question':'Does Sentence-BERT use masked language modeling?','expected_abstain':True},
]


def run():
    assistant = PaperAssistant()
    results = []
    for case in CASES:
        try:
            r = assistant.compare(case['question'],case['paper_ids']) if 'paper_ids' in case else assistant.ask(case['question'])
            passed = not case.get('expected_error', False)
            passed &= r['abstained'] == case.get('expected_abstain', False)
            if 'expected_sources' in case:
                passed &= set(c['paper_id'] for c in r['citations']) == set(case['expected_sources'])
            if 'contains' in case: passed &= case['contains'] in r['answer']
            if 'missing' in case: passed &= r['missing_paper_ids'] == case['missing']
            results.append({'case':case,'passed':bool(passed),'actual':r})
        except ValueError as exc:
            results.append({'case':case,'passed':case.get('expected_error',False),'error':str(exc)})
    report = {'label':'Development evaluation, not held-out research accuracy',
              'python_version':platform.python_version(),'scikit_learn_version':sklearn.__version__,
              'total':len(results),'passed':sum(r['passed'] for r in results),
              'failed':sum(not r['passed'] for r in results),'results':results}
    base = Path(__file__).parent / 'examples'
    base.mkdir(exist_ok=True)
    (base/'evaluation_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    lines=['# Task 3 development evaluation', '',f"Actual outcome: **{report['passed']}/{report['total']} checks passed; {report['failed']} failed.**",'',
           'These manually specified cases were visible during development. They test expected behavior, not generalization or complete factual correctness.', '',
           '| Case | Category | Outcome |','|---|---|---|']
    lines += [f"| {r['case']['id']} | {r['case']['category']} | {'PASS' if r['passed'] else 'FAIL'} |" for r in results]
    lines += ['', '## Failure analysis', '',
              'The challenge probes ask about a named paper using terms belonging to another note. Lexical retrieval may select the other paper and respond instead of declining the unsupported attribution. A returned citation and a high match score do not establish that the answer addresses the named paper.', '',
              'Comparison mode avoids one part of this problem by keeping explicit paper selections and testing topic evidence within each selected note. Single-question mode remains a limited baseline. Neither mode handles logical negation or verifies entailment.', '',
              'Next steps: paper-name-aware question routing, a held-out set of misleading/negated questions, and manual assessment of relevance and evidence support. Full PDF indexing and semantic retrieval remain outside this version.']
    (base/'EVALUATION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f"Evaluation: {report['passed']}/{report['total']} passed; {report['failed']} failed (see examples/EVALUATION.md).")
    return report


if __name__ == '__main__': run()
