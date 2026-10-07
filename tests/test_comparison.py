import unittest
from engine import PaperAssistant


class ComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.assistant = PaperAssistant()

    def test_both_papers_supply_real_extracts(self):
        r = self.assistant.compare('retriever', ['P03','P04'])
        self.assertFalse(r['abstained'])
        self.assertEqual([c['paper_id'] for c in r['citations']], ['P03','P04'])
        for e in r['evidence']:
            text = next(p['text'] for p in self.assistant.papers if p['id']==e['paper_id'])
            for extract in e['extracts']: self.assertIn(extract, text)

    def test_partial_support_does_not_claim_complete_comparison(self):
        r = self.assistant.compare('cosine similarity', ['P01','P04'])
        self.assertTrue(r['abstained'])
        self.assertEqual(r['missing_paper_ids'], ['P04'])
        self.assertEqual(r['evidence'][1]['extracts'], [])

    def test_absent_topic(self):
        r = self.assistant.compare('2026 subscription price', ['P03','P04'])
        self.assertTrue(r['abstained'])
        self.assertEqual(r['citations'], [])

    def test_bad_selection_and_input(self):
        for ids in [None, [], ['P01'], ['P01','P01'], ['P01','P99'], ['P01',{}], 'P01,P02']:
            with self.assertRaises(ValueError): self.assistant.compare('retriever', ids)
        for q in ['', None, 3, 'x'*1001, 'compare REALM versus Sentence-BERT']:
            with self.assertRaises(ValueError): self.assistant.compare(q, ['P01','P04'])

    def test_ask_handles_malformed_paper_id(self):
        for pid in [[], {}, 2]:
            with self.assertRaises(ValueError): self.assistant.ask('retriever', pid)
