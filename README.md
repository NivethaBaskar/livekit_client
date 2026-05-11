# LiveKit Voice Assistant

A real-time voice assistant built with LiveKit. The React frontend connects to a LiveKit room where a Python AI agent joins automatically, listens to your speech, and responds using GPT-4o-mini — with live captions displayed in the UI.

## Architecture

```
Browser (React UI)
    │
    │  WebRTC (audio/video)
    ▼
LiveKit Server (ws://localhost:7880)
    │
    │  Agent Worker connection
    ▼
Python Agent
  ├── Silero VAD  →  detects when you speak
  ├── OpenAI Whisper  →  transcribes speech to text
  ├── GPT-4o-mini  →  generates a response
  └── OpenAI TTS  →  speaks the response back
```

## Project Structure

```
livekit-practice/
├── agent/
│   ├── agent.py          # Python voice assistant agent
│   ├── requirements.txt  # Python dependencies
│   └── .env.example      # Environment variable template
└── livekit-ui/
    ├── src/
    │   ├── App.js        # React app with LiveKit room + live captions
    │   └── ...
    ├── token.js          # JWT token generator for local dev
    └── package.json
```

## Prerequisites

- [Node.js](https://nodejs.org/) v18+
- [Python](https://python.org/) 3.11+
- [LiveKit server](https://docs.livekit.io/home/self-hosting/local/) (local or Docker)
- OpenAI API key

## Setup

### 1. Start the LiveKit Server

**Using Docker (recommended):**
```bash
docker run --rm \
  -p 7880:7880 -p 7881:7881 -p 7882:7882/udp \
  livekit/livekit-server --dev
```

**Using the CLI:**
```bash
livekit-server --dev
```

### 2. Set Up the Python Agent

```bash
cd agent
pip install -r requirements.txt
```

Copy the environment template and fill in your OpenAI key:
```bash
cp .env.example .env
```

Edit `agent/.env`:
```env
LIVEKIT_URL=ws://localhost:7880
LIVEKIT_API_KEY=devkey
LIVEKIT_API_SECRET=secret
OPENAI_API_KEY=sk-...your-key-here...
```

Start the agent:
```bash
python agent.py dev
```

### 3. Set Up the React UI

```bash
cd livekit-ui
npm install
```

Generate a fresh JWT token (valid 24h):
```bash
node token.js
```

Paste the printed token into `livekit-ui/src/App.js` at the `TOKEN` constant, then start the app:
```bash
npm start
```

Open [http://localhost:3000](http://localhost:3000) — allow microphone and camera access.

## How It Works

1. The React app connects to the LiveKit room using a signed JWT token.
2. The agent worker polls the LiveKit server for new room participants.
3. When you join, the agent automatically enters the room as a participant.
4. The agent greets you, then listens for your voice using Silero VAD.
5. When you speak, Whisper transcribes your audio and the transcription appears as live captions in the UI.
6. GPT-4o-mini generates a reply, which is spoken back using OpenAI TTS.

## Key Configuration

| Variable | Default | Description |
|---|---|---|
| `LIVEKIT_URL` | `ws://localhost:7880` | LiveKit server WebSocket URL |
| `LIVEKIT_API_KEY` | `devkey` | Must match the key used to sign the UI token |
| `LIVEKIT_API_SECRET` | `secret` | Must match the secret used to sign the UI token |
| `OPENAI_API_KEY` | — | Your OpenAI API key |

## Tech Stack

- **Frontend:** React, [@livekit/components-react](https://github.com/livekit/components-js)
- **Agent:** Python, [livekit-agents](https://github.com/livekit/agents), OpenAI (Whisper STT + GPT-4o-mini + TTS), Silero VAD
- **Transport:** LiveKit (WebRTC)
