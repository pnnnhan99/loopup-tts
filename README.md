# LOOPUP-TTS

A browser-based, high-performance Text-to-Speech (TTS) and Automatic Speech Recognition (ASR) web application powered by Piper TTS, Sherpa-ONNX, and ONNX Runtime Web. Generate high-quality speech and transcribe audio directly inside your browser with **zero server processing**. Live demo: [https://tts.loopup.io.vn](https://tts.loopup.io.vn)

---

## 🌟 Highlights

- **100% Client-Side Inference**: Runs entirely in the browser via WebAssembly (WASM) and Web Workers—ensuring total privacy and zero backend compute costs.
- **Advanced Vietnamese Normalization**: Native text preprocessing handling numbers, currencies (VND/USD), dates, times, fractions, phone numbers, and Roman numerals.
- **Multi-Language Support**: Dedicated routes and models for Vietnamese (`/`), English (`/en`), and Indonesian (`/id`).
- **Real-Time Speech Recognition**: Integrated ASR via Sherpa-ONNX with Voice Activity Detection (VAD) for live microphone transcription and file export (SRT/TXT).
- **Offline & PWA Ready**: Leverages IndexedDB for persistent audio generation history and efficient model caching.

---

## 🛠️ Features

### Text-to-Speech (TTS)
- 🌐 **Serverless Processing**: High-speed ONNX runtime streaming inside Web Workers (~5× real-time processing speed).
- 🎙️ **Custom & Multi-Speaker Support**: Support for custom fine-tuned voices and multi-speaker ONNX checkpoints.
- ⚡ **Real-Time Audio Streaming**: Stream and play audio chunks as they are generated.
- 🎚️ **Playback Control**: Adjustable reading speed, audio export (WAV), and real-time word/character count stats.
- 📜 **Generation History**: IndexedDB-backed history panel to replay, copy, or re-download past outputs.

### Automatic Speech Recognition (ASR)
- 🎙️ **Microphone Stream Mode**: Live voice capture with automated Silero VAD segmentation.
- 📂 **Batch File Upload**: Transcribe audio files with real-time visual progress tracking.
- 📝 **Subtitle Export**: Export transcribed text into `.srt` subtitles with precise timestamps or plain `.txt`.

---

## 🏗️ Tech Stack

- **Frontend Framework**: Vue 3 + Vite + Tailwind CSS
- **TTS Engine**: Piper TTS (ONNX Format)
- **ASR Engine**: Sherpa-ONNX WASM + Silero VAD
- **Inference Pipeline**: ONNX Runtime Web (WASM)
- **Hosting & Storage**: Cloudflare Pages + Cloudflare R2 (Edge Model Storage)

---

## 📂 Project Structure
```bash
loopup-tts/
├── src/
│   ├── App.vue                 # Main shell with tab navigation and history modal
│   ├── router/index.js         # Routes: / (Vietnamese), /en, /id, /asr
│   ├── views/                  # Main page views (VietnameseView, LanguageView, ASRView)
│   ├── components/             # UI components (HistoryPanel, ModelSelector, SpeedControl, etc.)
│   ├── lib/                    # Inference wrappers for Piper TTS and Sherpa-ONNX
│   ├── utils/                  # Vietnamese text processing and IndexedDB stores
│   └── workers/                # Multi-threaded Web Workers for background TTS processing
├── functions/api/              # Cloudflare Pages Functions for serving models from R2
└── public/                     # Static assets, WASM binaries, and local development models
├── tts-model/              # Local TTS models (vi/, en/, id/)
├── asr-model/              # Local ASR model folders
└── vad-model/              # Silero VAD model assets
```

---

## 🚀 Local Development Setup

### Prerequisites

- **Node.js**: `v18.0.0` or higher
- **Package Manager**: `npm` or `yarn`

### Installation & Run

1. **Clone the repository**:
   ```bash
   git clone [https://github.com/pnnnhan99/loopup-tts.git](https://github.com/pnnnhan99/loopup-tts.git)
   cd loopup-tts
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Configure local models:
   Place your .onnx models and .onnx.json configuration pairs inside the corresponding public directories:

   ```bash
   public/
   ├── tts-model/
   │   ├── vi/    # Vietnamese models (.onnx + .onnx.json)
   │   ├── en/    # English models
   │   └── id/    # Indonesian models
   └── asr-model/ # Sherpa-ONNX model folders
   ```
4. Start the development server:
   ```bash
   npm run dev
   ```
   Navigate to http://localhost:5173 in your browser.

### Configure local models:
Place your .onnx models and .onnx.json configuration pairs inside the corresponding public directories:

```bash
public/
├── tts-model/
│   ├── vi/    # Vietnamese models (.onnx + .onnx.json)
│   ├── en/    # English models
│   └── id/    # Indonesian models
└── asr-model/ # Sherpa-ONNX model folders
Start the development server:

Bash
npm run dev
Navigate to http://localhost:5173 in your browser.

📦 Model Requirements
Each TTS voice model requires two paired files under the corresponding language path:

{model_name}.onnx — The compiled binary ONNX model file.

{model_name}.onnx.json — The JSON configuration containing phoneme maps and speaker settings.

📄 License & Legal Notice
This project is released under the MIT License.

✅ Free for personal and commercial use

✅ Modify, adapt, and distribute freely

Disclaimer
This software is provided "as is", without warranty of any kind. Users are solely responsible for ensuring that all voice models and audio generated through this platform adhere to local intellectual property, voice likeness, and copyright laws.

🙌 Acknowledgments
This application is built upon open-source core voice technology projects:

Piper TTS by OHF-Voice (GPL-3.0)

Sherpa-ONNX by k2-fsa (Apache-2.0)

ONNX Runtime Web by Microsoft (MIT)