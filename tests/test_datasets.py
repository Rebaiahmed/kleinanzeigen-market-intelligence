import json
import unittest
from pathlib import Path

class DatasetTest(unittest.TestCase):
    def test_synthetic_labels_and_identifiers(self):
        ids = set()
        for path in Path('datasets/golden').glob('*.json'):
            rows = json.loads(path.read_text(encoding='utf-8'))
            self.assertTrue(rows)
            for row in rows:
                self.assertEqual(set(row), {'id','left','right','label','reason'} | ({'category'} if 'category' in row else set()))
                self.assertNotIn(row['id'], ids)
                ids.add(row['id'])
                self.assertTrue(type(row['label']) is bool or row['label'] == 'unknown')
                self.assertTrue(all(isinstance(row[k],str) and row[k] for k in ['id','left','right','reason']))
