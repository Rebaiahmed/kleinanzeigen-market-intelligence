"""Run offline analytics and metric calculations over JSON or CSV input."""
import argparse
import csv
import json
from pathlib import Path
from .analysis import summarize
from .metrics import matching_metrics, price_metrics


def load_records(path, operation):
    """Load JSON arrays or CSV rows, converting the operation's typed fields."""
    if path.suffix.lower() != '.csv':
        records = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(records, list):
            raise ValueError('input must be a JSON array')
        return records
    numeric = {'asking-prices': ('asking_price_eur',), 'prices': ('reference', 'predicted'), 'matching': ()}[operation]
    boolean = ('label', 'predicted') if operation == 'matching' else ()
    with path.open(encoding='utf-8-sig', newline='') as source:
        reader = csv.DictReader(source)
        if not reader.fieldnames or len(reader.fieldnames) != len(set(reader.fieldnames)):
            raise ValueError('CSV must have a header with unique field names')
        rows = list(reader)
    for line, row in enumerate(rows, start=2):
        try:
            for key in numeric:
                row[key] = float(row[key])
            for key in boolean:
                value = row[key].strip().lower()
                if value not in ('true', 'false'):
                    raise ValueError(f'{key} must be true or false')
                row[key] = value == 'true'
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f'CSV row {line}: {exc}') from exc
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation', choices=['prices', 'matching', 'asking-prices'])
    parser.add_argument('input', type=Path)
    args = parser.parse_args()
    try:
        records = load_records(args.input, args.operation)
        func = {'prices': price_metrics, 'matching': matching_metrics, 'asking-prices': summarize}[args.operation]
        result = func(records)
    except (OSError, KeyError, TypeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))

if __name__ == '__main__':
    main()
