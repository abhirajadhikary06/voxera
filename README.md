# Voxera

**Orchestrate. Speak.**

> One framework, every voice.

Voxera is a unified orchestration framework built exclusively for speech — bringing every major transcription and voice synthesis backend under a single consistent interface. It delivers production-grade primitives like streaming, parallel batch processing, memory, tools, and middleware to audio pipelines with a speed and flexibility no existing framework offers.

---

## What Voxera Solves

Every speech project today forces the same choices: pick a provider, write glue code, handle retries manually, build your own streaming logic, and start over when you want to swap providers. Voxera removes all of that.

You define what you want done with audio. Voxera handles how.

---

## Core Features

### Unified Model Interface
Every speech-to-text and text-to-speech backend — whether a local offline package or a cloud API — is accessed through the same interface. Swap providers by changing one string. No rewrite required.

### Parallel Batch Engine
A 60-minute audio file can be split into segments and processed concurrently. Wall-clock time approaches the length of the longest single segment, not the sum of all segments. This is not an optimization — it is a core architectural feature.

### Streaming Engine
Real-time STT and TTS pipelines built on async generators. Audio chunks flow from source to model to callback without blocking. TTS streaming buffers incoming text to sentence boundaries before dispatching, minimizing latency while preserving natural speech rhythm.

### Audio Tools
Pre-built and custom callables that slot into any pipeline at defined hook points — voice activity detection, speaker diarization, PII redaction, audio normalization, language detection, sentiment analysis, and pronunciation dictionaries.

### Pipeline Memory
Session-scoped in-memory transcript accumulation, persistent database-backed storage, and optional vector memory for semantic search over past transcripts. All attached to a pipeline via a single `checkpointer` parameter.

### Structured Output
Declare the fields you need — word timestamps, speaker labels, sentiment, chapters, entities — and Voxera routes only to providers capable of satisfying the schema. Automatic fallback to post-processing tools when a provider lacks a native feature.

### Middleware
Retry on rate limits, automatic provider fallback on hard failure, audio format conversion, cost metering, and latency tracing — all composable and replaceable.

### Observability
Structured telemetry at every pipeline step. Plugs into stdout, OpenTelemetry, Datadog, or a custom webhook.

---

## Supported Backends

### Speech to Text

| Backend | Type | Streaming | Languages | Notes |
|---|---|---|---|---|
| faster-whisper | Offline pip | With extensions | 98+ | 4-10x faster than base Whisper, VAD filter |
| openai-whisper | Offline pip | Partial | 99+ | SOTA accuracy, translation mode |
| vosk | Offline pip | Yes | 20+ | Lightweight, works on embedded devices |
| pvleopard / pvcheetah | Offline pip | Yes (Cheetah) | 12+ | Ultra-low latency, on-device privacy |
| SpeechRecognition | Offline pip | Limited | Many (via APIs) | Beginner wrapper, Sphinx offline weak |
| pocketsphinx | Offline pip | Yes | Limited | Legacy, non-neural, keyword spotting |
| Deepgram Nova-3 / Flux | API | Yes | 36+ | Sub-300ms, end-of-turn detection |
| AssemblyAI | API | Yes | 99+ | Sentiment, PII redaction, chapters in one call |
| ElevenLabs Scribe | API | Yes | 30+ | Event tagging, integrates with ElevenLabs TTS |
| Gladia | API | Yes | 100+ | Code-switching, very low latency |
| Speechmatics | API | Yes | 55+ | Strong accent robustness |
| Rev.ai | API | Yes | English-focused | High accuracy batch |
| Microsoft Azure Speech | API | Yes | 100+ | Custom acoustic and language models |
| Google Cloud STT | API | Yes | 125+ | Chirp 2 best batch accuracy |
| Amazon Transcribe | API | Yes | 36+ | Medical domain model, PII detection |
| OpenAI Whisper API | API | Batch | 100+ | Simple REST, GPT-4o Transcribe adds streaming |
| Groq Whisper | API | No | 99+ | Fastest Whisper inference via Groq hardware |
| Cartesia STT | API | Yes | 40+ | State Space Model, sub-90ms |

### Text to Speech

| Backend | Type | Streaming | Languages | Notes |
|---|---|---|---|---|
| ElevenLabs | API | Yes | 70+ | 75ms Flash, 10k+ voices, cloning, voice design |
| Cartesia Sonic | API | Yes | 40+ | 90ms TTFA, State Space Model, on-device deploy |
| Deepgram Aura-2 | API | Yes | English-primary | Sub-250ms, built by same team as Nova-3 |
| Play.ht | API | Yes | Many | 600+ voices, voice cloning |
| Murf.ai | API | No | Many | Studio quality, video integration |
| Amazon Polly | API | Yes | 60+ | SSML, speech marks, cost-effective at scale |
| Microsoft Azure TTS | API | Yes | 140+ | Speaking styles, viseme output for lip sync |
| Respeecher | API | No | Limited | Film-grade voice cloning |
| Resemble AI | API | Yes | Many | Emotion controls, custom voice creation |
| Google Cloud TTS | API | Yes | 50+ | WaveNet, Neural2, audio profiles |
| OpenAI TTS | API | Yes | Many | Simple REST, 6 built-in voices |
| Noiz.ai | API | Yes | Many | Expressive, fast generation, dubbing |

---

## Quick Start

```python
from voxera import AudioPipeline, AudioInput
from voxera.adapters.stt import FasterWhisperSTTModel
from voxera.tools import SileroVAD, PIIRedactor
from voxera.core.structured import TranscriptSchema

pipeline = AudioPipeline(
    steps=[
        SileroVAD(),
        FasterWhisperSTTModel("large-v3"),
        PIIRedactor(),
    ],
    response_format=TranscriptSchema(words=True, speakers=True),
)

result = await pipeline.invoke(AudioInput.from_file("meeting.wav"))
print(result.text)
```

### Swap to a cloud provider — one line changes

```python
from voxera.adapters.stt import DeepgramSTTModel

pipeline = AudioPipeline(
    steps=[
        SileroVAD(),
        DeepgramSTTModel("nova-3"),
        PIIRedactor(),
    ],
    response_format=TranscriptSchema(words=True, speakers=True),
)
```

### Parallel batch processing

```python
from voxera import batch

audio_files = [AudioInput.from_file(f) for f in file_list]
results = await batch(pipeline, audio_files, concurrency=20)
```

### Real-time streaming STT

```python
from voxera import VoicePipeline
from voxera.adapters.stt import DeepgramSTTModel
from voxera.adapters.tts import ElevenLabsTTSModel

voice = VoicePipeline(
    stt=DeepgramSTTModel("nova-3"),
    tts=ElevenLabsTTSModel("flash-v2.5", voice="rachel"),
)

async for chunk in voice.stream(microphone_source):
    audio_player.play(chunk)
```

### With memory and session context

```python
from voxera.core.memory import PersistentMemory

pipeline = AudioPipeline(
    steps=[FasterWhisperSTTModel("large-v3")],
    checkpointer=PersistentMemory(db_url="postgresql://localhost/voxera"),
    session_id="user-abc-123"
)

# Transcript accumulates across multiple calls in this session
result1 = await pipeline.invoke(AudioInput.from_file("turn_1.wav"))
result2 = await pipeline.invoke(AudioInput.from_file("turn_2.wav"))
history = pipeline.memory.get_transcript_so_far()
```

### Custom audio tool

```python
from voxera.core.tools import audio_tool, ToolRuntime
from voxera.core.messages import Transcript

@audio_tool
async def profanity_filter(transcript: Transcript, runtime: ToolRuntime) -> Transcript:
    filtered = transcript.text.replace("badword", "[filtered]")
    return transcript.with_text(filtered)

pipeline = AudioPipeline(
    steps=[
        FasterWhisperSTTModel("base"),
        profanity_filter,
    ]
)
```

---

## Architecture

```
User-facing pipeline API          pipeline(), invoke(), stream(), batch()
        |
Orchestration layer               Agents, pipelines, concurrency scheduler
        |
Core primitives
  Models      Messages      Tools          Memory
  STT/TTS     AudioChunk    VAD, diarize   Session, persistent, vector
        |
Streaming engine                  Async generators, WebSocket, chunk queues
Structured output                 TranscriptSchema, SpeechSchema
        |
Middleware layer                  Retry, fallback, format conversion, cost meter
        |
Provider adapters
  Offline pip packages            faster-whisper, vosk, pvleopard, whisper
  STT API providers               Deepgram, AssemblyAI, ElevenLabs, Gladia
  TTS API providers               ElevenLabs, Cartesia, Deepgram Aura
        |
Observability + telemetry         Latency tracing, WER tracking, cost metering
```

---

## Package Structure

```
voxera/
  core/
    messages.py         AudioInput, AudioChunk, Transcript, SpeechOutput
    models.py           BaseSTTModel, BaseTTSModel, VoiceConfig
    tools.py            @audio_tool decorator, ToolRuntime
    memory.py           SessionMemory, PersistentMemory, VectorMemory
    streaming.py        ChunkQueue, AudioSplitter, ParallelBatchEngine
    structured.py       TranscriptSchema, SpeechSchema
  agents/
    pipeline.py         AudioPipeline
    agent.py            AudioAgent
    voice_pipeline.py   VoicePipeline
  adapters/
    stt/                One file per provider
    tts/                One file per provider
  tools/
    vad.py
    diarizer.py
    normalizer.py
    language_detector.py
    pii_redactor.py
    sentiment.py
    pronunciation.py
  middleware/
    retry.py
    fallback.py
    cost_meter.py
    latency_tracer.py
    format_converter.py
  observability/
    telemetry.py
    runtime.py
```

---

## Message Types

Every piece of data flowing through Voxera is a typed primitive.

`AudioInput` — wraps raw audio bytes, sample rate, channel count, format, source (file, URL, bytes, microphone stream), duration hint, language hint.

`AudioChunk` — a time-bounded slice of an `AudioInput` used during streaming. Contains byte payload, timestamp offset, chunk index, is-final flag.

`Transcript` — output of STT. Contains full text, list of `Word` objects (each with `text`, `start`, `end`, `confidence`, `speaker_id`), detected language, duration, provider name, model used.

`TranscriptChunk` — streaming partial from STT. Contains partial text, is_final flag, timestamp, speaker change signal.

`SpeechOutput` — output of TTS. Contains audio bytes, format, sample rate, optional word timestamps, provider name, model used.

`SpeechChunk` — streaming partial from TTS. Contains audio bytes, is_final flag, chunk index.

---

## Middleware

Middleware wraps every model call and is applied automatically to all pipelines.

```python
from voxera.middleware import RetryMiddleware, FallbackMiddleware, CostMeterMiddleware

pipeline = AudioPipeline(
    steps=[DeepgramSTTModel("nova-3")],
    middleware=[
        RetryMiddleware(max_attempts=3, backoff=2.0),
        FallbackMiddleware(fallback=AssemblyAISTTModel()),
        CostMeterMiddleware(budget_usd=5.0),
    ]
)
```

Pre-built middleware:

- `RetryMiddleware` — exponential backoff on 429 and 503 responses.
- `FallbackMiddleware` — on hard failure from primary provider, routes to secondary with the same interface.
- `CostMeterMiddleware` — tracks audio seconds (STT) or character count (TTS) per session and emits cost estimates. Optional hard stop at a budget ceiling.
- `LatencyTracerMiddleware` — records time-to-first-chunk, total duration, and provider response time.
- `AudioFormatMiddleware` — converts input audio to the provider-required format before dispatch.

---

## Observability

```python
from voxera.observability import OTelTelemetry

pipeline = AudioPipeline(
    steps=[FasterWhisperSTTModel("large-v3")],
    telemetry=OTelTelemetry(endpoint="http://localhost:4317")
)
```

Every pipeline step emits a structured event containing step name, duration, input size, output size, provider, model, and error details if applicable. Supported backends: stdout (default), OpenTelemetry, Datadog, custom webhook.

---

## Installation

```bash
pip install voxera
```

With offline models:

```bash
pip install voxera[offline]
```

With all API provider SDKs:

```bash
pip install voxera[all]
```

---

## Environment Variables

```bash
DEEPGRAM_API_KEY=...
ASSEMBLYAI_API_KEY=...
ELEVENLABS_API_KEY=...
CARTESIA_API_KEY=...
OPENAI_API_KEY=...
AZURE_SPEECH_KEY=...
AZURE_SPEECH_REGION=...
GOOGLE_APPLICATION_CREDENTIALS=path/to/service_account.json
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
PICOVOICE_ACCESS_KEY=...
GROQ_API_KEY=...
```

---

## Roadmap

- Phone call integration (Twilio, Vonage)
- Browser WASM support for on-device offline models
- Fine-tune adapter for custom Whisper models
- Native speaker diarization across all streaming providers
- Cost dashboard UI
- gRPC transport option for high-throughput deployments
- Audio vector store for episode-level semantic search

---

## License

MIT

---

## Contributing

Contributions are welcome. To add a new provider adapter, implement `BaseSTTModel` or `BaseTTSModel` and place the file under `voxera/adapters/stt/` or `voxera/adapters/tts/`. The adapter is responsible for translating the universal interface into provider-specific calls. All existing tests must pass and a new adapter-level test must be included.

---

*Voxera — Speech, orchestrated.*
