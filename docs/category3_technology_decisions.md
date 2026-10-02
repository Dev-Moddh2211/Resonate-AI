# Category 3 technology decisions

The runtime uses the existing Python retrieval interface directly. The voice boundary is a provider-neutral HTTP webhook with Twilio-compatible `Gather`/`Say` XML: a Twilio number can point its voice URL at `/voice/start`, and speech posts to `/voice/turn`. This was selected because it provides a real callable-phone path while keeping ASR/TTS and telephony replaceable.

Alternatives considered: browser WebRTC would require a frontend and browser media permissions; a direct provider SDK would couple the conversation manager to one vendor; a CLI transcript is insufficient for the assessment. The adapter currently relies on the telephony provider for ASR/TTS and does not claim transfer completion.

Known limitations: the prototype stores active call state in process memory, has no production authentication/signature middleware, and uses the repository's synthetic knowledge sources. Deploy behind HTTPS, validate provider signatures, use durable controlled storage, and replace synthetic sources before real users. Provider pricing and availability vary by region and account; confirm current rates with the selected provider before deployment.
