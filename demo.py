"""Produce actual example outputs from the installed library integration."""
import json
import platform
from pathlib import Path
import sklearn
from engine import PaperAssistant

questions = [
    'What similarity measure does Sentence-BERT use?',
    'How does REALM train its retriever?',
    'What does Lost in the Middle investigate?',
    'What role does the neural retriever play in Retrieval-Augmented Generation?',
    'What is the latest 2026 benchmark score for this assistant?',
    'What is the capital of France?',
]
assistant = PaperAssistant()
results = {'python_version':platform.python_version(), 'scikit_learn_version':sklearn.__version__,
           'note':'Actual smoke-demo outputs, not a held-out research benchmark.',
           'examples':[assistant.ask(q) for q in questions]}
out = Path(__file__).parent / 'examples' / 'actual_outputs.json'
out.parent.mkdir(exist_ok=True)
out.write_text(json.dumps(results, indent=2), encoding='utf-8')
for result in results['examples']:
    print('\nQUESTION:', result['question'])
    print('ANSWER:', result['answer'])
print('\nSaved examples/actual_outputs.json')
