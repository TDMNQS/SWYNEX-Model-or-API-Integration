import unittest
from engine import PaperAssistant


class AssistantTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.assistant = PaperAssistant()

    def test_similarity_answer_has_support_and_correct_source(self):
        result = self.assistant.ask('What similarity measure does Sentence-BERT use?')
        self.assertFalse(result['abstained'])
        self.assertIn('cosine similarity', result['answer'])
        self.assertEqual(result['citations'][0]['paper_id'], 'P01')
        self.assertIn(result['answer'], self.assistant.papers[0]['text'])

    def test_training_paraphrase(self):
        result = self.assistant.ask('How does REALM train its retriever?')
        self.assertFalse(result['abstained'])
        self.assertIn('Masked language modeling', result['answer'])
        self.assertEqual(result['citations'][0]['paper_id'], 'P04')

    def test_unsupported_question_does_not_emit_citation(self):
        result = self.assistant.ask('What is the latest 2026 benchmark score for this assistant?')
        self.assertTrue(result['abstained'])
        self.assertEqual(result['citations'], [])

    def test_scope_cannot_leak_other_papers(self):
        result = self.assistant.ask('What similarity measure does Sentence-BERT use?', 'P04')
        self.assertTrue(result['abstained'])

    def test_invalid_input(self):
        for q in ['', '   ', None, 5, 'x'*1001]:
            with self.assertRaises(ValueError): self.assistant.ask(q)
        with self.assertRaises(ValueError): self.assistant.ask('retrieval', 'P99')


if __name__ == '__main__': unittest.main()
