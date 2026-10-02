# Category 5 false-positive analysis

The detector is intentionally conservative and rule-backed. It requires an exact evidence phrase, the expected speaker label, and a configurable confidence threshold. Ambiguous/noisy text therefore produces no nudge in the prototype. Repeated evidence is suppressed by signal cooldown; a materially different high-priority signal can still appear. These are synthetic transcript tests, not audio false-positive measurements.

The recorded cases and verdicts are in `evaluation/false_positive_results.json`. Confidence is a detector score, not a calibrated probability. Speaker labels come from replay metadata; this prototype does not claim diarization.
