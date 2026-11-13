"""Run offline analytics and metric calculations over JSON input."""
import argparse
import json
from pathlib import Path
from .analysis import summarize
from .metrics import matching_metrics, price_metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['prices', 'matching', 'asking-prices'])
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    records = json.loads(args.input.read_text(encoding='utf-8'))
    if not isinstance(records, list):
        parser.error('input must be a JSON array')
    func = {'prices': price_metrics, 'matching': matching_metrics, 'asking-prices': summarize}[args.operation]
    print(json.dumps(func(records), ensure_ascii=False, indent=2, allow_nan=False))

if __name__ == '__main__':
    main()
