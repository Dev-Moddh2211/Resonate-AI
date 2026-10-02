# Category 5 testing

Automated tests cover incremental chunks, compliance, missed opportunity, noisy text suppression, repeated-trigger suppression, measured stage timing, and polling cursor behavior. Tests use synthetic pre-labelled text and do not claim audio ASR or true diarization.

The required live demonstrations are not marked complete: there is no actual audio file, no connected streaming ASR, and no browser dashboard connected to `pipeline.poll`. Compliance and opportunity behavior are verified before the replay sequence ends in pipeline tests.
