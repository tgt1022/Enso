"""Basic sequence labeling metrics."""
import json

from sklearn.metrics import accuracy_score, precision_score, recall_score
from enso.metrics import SequenceLabelingMetric


def overlap(x1, x2):
    return x1["end"] >= x2["start"] and x2["end"] >= x1["start"]


def label_chars(sequence, null_label="none"):
    output = []
    for item in sequence:
        output.extend([null_label] * (item["start"] - len(output)))
        output.extend([item["label"]] * (item["end"] - item["start"]))
    return output


def convert_to_per_char_labs(ground_truth, result, null_label="none"):
    truth = (json.loads(g) for g in ground_truth)
    res = (json.loads(r) for r in result)
    true_out = []
    res_out = []
    for truth_b, res_b in zip(truth, res):
        truth_per_char = label_chars(truth_b, null_label)
        res_per_char = label_chars(res_b, null_label)

        res_per_char += [null_label] * (len(truth_per_char) - len(res_per_char))
        res_per_char = res_per_char[:len(truth_per_char)]
        true_out.extend(truth_per_char)
        res_out.extend(res_per_char)
    return true_out, res_out



class OverlapAccuracy(SequenceLabelingMetric):
    """ Accuracy of overlaps """

    def evaluate(self, ground_truth, result):
        """Return AUC metric."""
        truth, res = convert_to_per_char_labs(ground_truth, result)
        return accuracy_score(truth, res)


class OverlapPrecision(SequenceLabelingMetric):
    """ precision of overlaps """

    def evaluate(self, ground_truth, result):
        """Return AUC metric."""
        truth, res = convert_to_per_char_labs(ground_truth, result)
        return precision_score(truth, res, average="weighted")

class OverlapRecall(SequenceLabelingMetric):
    """ Accuracy of overlaps """

    def evaluate(self, ground_truth, result):
        """Return AUC metric."""
        truth, res = convert_to_per_char_labs(ground_truth, result)
        return recall_score(truth, res, average="weighted")