"""Metrics for precomputed estimates and binary product matches."""
from statistics import median
import math


def price_metrics(records):
    if not records:
        raise ValueError('at least one price record is required')
    errors, percentages = [], []
    over = under = 0
    for row in records:
        reference, predicted = row['reference'], row['predicted']
        if isinstance(reference, bool) or isinstance(predicted, bool) or not isinstance(reference, (int, float)) or not isinstance(predicted, (int, float)) or not math.isfinite(reference) or not math.isfinite(predicted) or reference < 0 or predicted < 0:
            raise ValueError('prices must be finite non-negative numbers')
        errors.append(abs(predicted - reference))
        if reference > 0:
            percentages.append(abs(predicted - reference) / reference * 100)
        over += predicted > reference
        under += predicted < reference
    return {'count': len(records), 'mae': sum(errors) / len(errors), 'median_absolute_error': median(errors), 'mape_percent': sum(percentages) / len(percentages) if percentages else None, 'mape_excluded_zero_reference': len(records) - len(percentages), 'overpriced_count': over, 'underpriced_count': under}


def matching_metrics(records):
    tp = fp = fn = tn = 0
    for row in records:
        truth, prediction = row['label'], row['predicted']
        if type(truth) is not bool or type(prediction) is not bool:
            raise ValueError('labels and predictions must be booleans')
        tp += truth and prediction
        fp += not truth and prediction
        fn += truth and not prediction
        tn += not truth and not prediction
    precision = tp / (tp + fp) if tp + fp else None
    recall = tp / (tp + fn) if tp + fn else None
    f1 = 2 * precision * recall / (precision + recall) if precision is not None and recall is not None and precision + recall else None
    if precision == 0 and recall == 0:
        f1 = 0.0
    return {'count': len(records), 'tp': tp, 'fp': fp, 'fn': fn, 'tn': tn, 'precision': precision, 'recall': recall, 'f1': f1}
