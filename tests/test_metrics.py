import unittest
from market_intelligence.metrics import matching_metrics, price_metrics
from market_intelligence.analysis import summarize

class MetricsTest(unittest.TestCase):
    def test_price_and_zero_reference(self):
        result = price_metrics([{'reference':100,'predicted':110},{'reference':0,'predicted':10}])
        self.assertEqual(result['mae'],10)
        self.assertEqual(result['mape_percent'],10)
        self.assertEqual(result['mape_excluded_zero_reference'],1)
    def test_reject_invalid_price(self):
        for x in (float('nan'), -1, True):
            with self.assertRaises(ValueError):
                price_metrics([{'reference':x,'predicted':1}])
    def test_matching(self):
        result = matching_metrics([{'label':True,'predicted':True},{'label':False,'predicted':True},{'label':True,'predicted':False}])
        self.assertEqual(result['precision'],0.5)
        self.assertEqual(result['recall'],0.5)
        self.assertEqual(result['f1'],0.5)
    def test_empty_matching_undefined(self):
        self.assertIsNone(matching_metrics([])['precision'])
    def test_distribution(self):
        result = summarize([{'category':'a','asking_price_eur':x} for x in [10,20,30]])['a']
        self.assertEqual((result['median'],result['p25'],result['p75']), (20,15,25))

if __name__ == '__main__': unittest.main()
