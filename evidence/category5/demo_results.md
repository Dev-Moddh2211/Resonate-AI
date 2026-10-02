# Category 5 execution result

## Stereo fixture execution

The four WAV fixtures are synthetic/demo stereo recordings. The left channel is the agent and the right channel is the customer. This attribution comes from fixture construction; it is **not** general-purpose ASR diarization.

Real 1.0x replay with selected `base.en`, CPU, `int8` produced:

| scenario | duration | observed ASR evidence | signal | nudge | before completion |
|---|---:|---|---|---|---|
| compliance | 3866 ms | agent: `guaranteed.` | `compliance_gap` | `Do not imply guaranteed approval.` | yes, at 2000 ms |
| missed opportunity | 4767 ms | customer: `We are expanding.` | `missed_opportunity` | `Ask whether they also need financing for the expansion.` | yes, at 0 ms |
| frustration | 5579 ms | base.en: customer `frustrated. //` at 2000 ms; see transcript evidence | `rising_frustration` | `Acknowledge the concern before continuing.` | yes at 2000 ms |
| noisy/ambiguous | 3491 ms | customer: `is unclear.` | none | none | suppression observed |

The transcripts are actual FasterWhisper output and remain imperfect; no text was corrected or injected. A controlled comparison on the same clean 16 kHz stereo frustration WAV found tiny.en returned `cross-traded.` in all three fresh runs with no signal, while base.en returned `frustrated. //` in all three runs and fired the unchanged detector at 2000 ms. base.en is therefore the selected demo model for this fixture. The result does not claim general ASR determinism beyond these repeated runs.

## Implemented

The checkout contains WAV chunking, a FasterWhisper adapter, signal detection, nudge generation, an in-process realtime event store, HTTP start/poll endpoints, and a static dashboard.

## Executed and verified

- `faster-whisper` 1.2.1 imported successfully.
- `base.en` was selected after a same-fixture comparison and loaded on CPU with `int8`; it fired the frustration signal in all three comparison runs.
- All four real WAV fixtures were replayed incrementally at approximately 1.0x.
- FasterWhisper returned real ASR text for all scenarios; noisy audio returned only `Maybe not clear.` and then no text.
- The comparison path preserved the fixture's established left-agent/right-customer channel attribution; no detector or threshold changes were made.
- Browser dashboard live verification and screenshots were not captured. Endpoint polling was not treated as browser proof.
- No latency percentile claim is made: the existing stage timing records are only populated for emitted signals, and this run emitted none.

## Exact commands

```text
python3 -m pip install faster-whisper
python3 -c "import faster_whisper; print(faster_whisper.__version__)"
python3 -m voice_agent.http_server
```

The requested `python` spelling could not run because no `python` executable exists in this environment.

## Browser and latency status

The in-process pipeline and polling implementation were exercised, but this environment has no browser automation/control capability. The HTTP server could not be reached from a separate sandboxed curl process, so no browser screenshot or T5 browser-receive timestamp is claimed. Valid browser delivery P50/P95 and audio-to-dashboard P50/P95 therefore remain unavailable.

## Completion decision

Category 5 is **NOT COMPLETE**. Real ASR, stereo speaker attribution, signal detection, and pre-completion nudges succeeded. Browser verification, screenshots, and browser-delivery/end-to-end P50/P95 evidence remain outstanding.
