"""Summaries of observed asking prices; no market-wide inference."""
import math
from statistics import median


def percentile(values, p):
    values = sorted(values)
    if not values or not 0 <= p <= 1:
        raise ValueError('nonempty values and percentile from 0 to 1 required')
    pos = (len(values) - 1) * p
    lo, hi = math.floor(pos), math.ceil(pos)
    return values[lo] + (values[hi] - values[lo]) * (pos - lo)


def summarize(records):
    grouped = {}
    for row in records:
        value = row['asking_price_eur']
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0 or not isinstance(row['category'], str) or not row['category'].strip():
            raise ValueError('expected category and finite non-negative asking price')
        grouped.setdefault(row['category'], []).append(value)
    return {category: {'count': len(prices), 'median': median(prices), 'p25': percentile(prices, .25), 'p75': percentile(prices, .75)} for category, prices in sorted(grouped.items())}
