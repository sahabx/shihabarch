---
id: c6-realtime-language-ai
title: "Realtime Language AI: Translation & Transcription Pipelines Built on a Decade of Multilingual Fieldwork"
status: draft
client: "personal R&D + Discover Islam Society applications"
client_public: true
period: "2026 (tooling), rooted in 2020–2024 field experience"
pillars: [ai-adoption]
stack: [WhisperX, faster-whisper, Qwen ASR/TTS, realtime Arabic↔English translation prototypes, LLM-assisted book translation workflows]
metrics_ids: []
summary: "AI translation/transcription tooling (realtime Arabic↔English, long-audio WhisperX pipelines sized to consumer hardware, TTS/ASR experiments, book-translation repair workflows) built by someone who spent 4 years doing this work by hand at a government protection center."
---

# C6 · Realtime Language AI

## Facts
- **Field credibility first**: 4+ years (2020–2024) providing real-time translation in person and on telephone conferences at LMRA Expat Protection Center (Bengali/Urdu/Hindi/Arabic/English casework). Google Translate activity from that period: 400–500 events/month at peak.
- **Realtime Arabic→English translation prototype** (May 2026) — the manual skill converted into tooling.
- **Long-audio transcription pipeline**: hardware-audited Whisper model selection (tiny→large vs actual PC specs), WhisperX batch transcription, speech-transcription cleanup workflows.
- **TTS/ASR experiments**: Qwen TTS local install + venv workflow (Jul 2026), Qwen3-ASR AMD-compatibility research (Feb 2026), qwen3asr repo (Jan–Feb 2026).
- **Book-translation engineering**: Umdat Al Bayaan — repairing a Google-Docs-exported manuscript, structured translation with exactness constraints, project journal (Jul–Sep 2026).
- Practical multilingual ops: multilingual outreach content, country-specific campaign localization (see C5).

## career_cut
The rare profile that pairs lived domain expertise (government-grade multilingual casework) with the AI engineering to automate it. Shows judgment about model sizing to hardware and about where AI translation is/isn't acceptable (religious texts = human-led, AI-assisted).

## business_cut
"What you get": translation/transcription automation designed by someone who has done the manual job — so the quality bar is field-tested, not theoretical. Use cases: call centers, NGOs with multilingual beneficiaries, long-form audio archives, localized campaign content.

## Open items
- [ ] Decide which prototypes to polish into public demos (a live realtime-translate demo would be strong on /ask page).
