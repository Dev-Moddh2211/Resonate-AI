# Philippines ASR test note

Provider/model: browser Web Speech API, provider-dependent; prototype configuration uses `fil-PH` for Tagalog/Taglish and `en-PH`/`en-US` fallback where exposed. Tests cover English, Tagalog, Taglish, insurance terms, colloquial speech, and human escalation. Observations are qualitative from browser-generated transcripts; no WER is claimed. Code-switching and terms such as premium/policy were usable in the prototype, but browser voice availability varies. Native Filipino TTS is preferred (`fil-PH`) and otherwise the browser default is a documented compromise.
