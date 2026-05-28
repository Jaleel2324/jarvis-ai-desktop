# JARVIS OS — Engineering Journal & Project Overview

## Project Overview

JARVIS OS is a Windows-based AI desktop assistant inspired by the cinematic JARVIS systems seen in science fiction films. The project combines:

* A desktop frontend built with Tauri + TypeScript
* Real-time AI communication through WebSockets
* A Python FastAPI backend
* Local AI inference using Ollama + llama3.2
* Real-time speech recognition
* AI-generated voice responses
* Interactive orb visualization and audio-reactive UI
* Modular AI tooling architecture

The goal of the project is to build a production-style desktop AI assistant capable of:

* Conversational interaction
* Local AI inference
* Real-time voice communication
* Task execution
* System monitoring
* File/project awareness
* Autonomous assistance workflows
* Future screen/vision understanding

---

# Current Architecture

## Frontend

### Stack

* Tauri
* TypeScript
* Vite
* Web Audio API
* Web Speech API
* HTML/CSS
* Canvas rendering

### Responsibilities

The frontend currently handles:

* Orb rendering and animation
* Audio-reactive visualization
* Speech recognition
* WebSocket communication
* Audio playback queueing
* Status updates
* Desktop window rendering
* UI state management

### Key Frontend Files

```text
apps/desktop/src/main.ts
apps/desktop/src/orb.ts
apps/desktop/src/voice.ts
apps/desktop/src/ws.ts
apps/desktop/src/settings.ts
apps/desktop/src/style.css
```

---

## Backend

### Stack

* Python
* FastAPI
* Uvicorn
* WebSockets
* Ollama
* XTTS
* Pydub
* Torch
* Transformers

### Responsibilities

The backend currently handles:

* AI response generation
* Ollama integration
* Voice generation
* WebSocket routing
* Real-time event handling
* Status management
* Audio generation
* Future task orchestration

### Key Backend Files

```text
services/agent-api/main.py
services/agent-api/live_ws.py
services/agent-api/tts_engine.py
```

---

# AI Integration

## Ollama

The project currently uses:

```text
llama3.2
```

through:

```text
http://localhost:11434
```

The backend communicates with Ollama using OpenAI-compatible APIs.

### AI Responsibilities

* Conversational responses
* Assistant personality
* System status responses
* Coding assistance
* Future autonomous planning

---

# Voice System

## Current Voice Pipeline

### Components

* XTTS v2
* Pydub
* Web Audio API
* Base64 audio transport
* WebSocket streaming

### Features

* Local voice generation
* Cinematic post-processing
* Pitch shifting
* Compression
* Bass enhancement
* Audio normalization
* Browser audio playback

### Future Voice Goals

* Streaming speech
* Interruptible speech
* Lower latency
* Better emotional delivery
* Possible Fish Audio integration
* Possible custom JARVIS voice cloning

---

# Desktop Application Features

## Current Working Features

### Real-Time WebSocket Communication

The frontend and backend communicate through WebSockets for:

* Live status updates
* Transcript delivery
* AI responses
* Audio delivery
* Future autonomous task communication

### Orb Visualization

The orb system currently:

* Reacts to audio playback
* Responds to assistant states
* Supports idle/listening/thinking/speaking states
* Uses real-time audio analysis

### Voice Recognition

The project currently supports:

* Speech-to-text
* Continuous listening
* Auto restart
* Pause/resume handling
* Browser microphone support

### TTS Voice Playback

The system currently:

* Generates voice responses locally
* Encodes audio as base64
* Sends audio through WebSockets
* Plays responses in the desktop frontend

---

# Major Engineering Problems Solved

## 1. WebSocket Frontend/Backend Synchronization

### Problem

The frontend UI loaded correctly, but AI responses were not consistently triggering.

### Cause

The frontend and backend message formats became misaligned after merging the reference architecture with the custom Ollama backend.

### Diagnosis

* Checked browser DevTools
* Traced WebSocket events
* Compared frontend message types against backend handlers
* Manually tested WebSocket communication

### Fix

* Standardized message schemas
* Updated backend routes
* Stabilized response handling
* Reconnected frontend and backend event flow

### What I Learned

I learned how critical consistent event schemas are in real-time systems and improved my understanding of asynchronous frontend/backend communication.

---

## 2. AI Voice Playback Integration

### Problem

JARVIS generated text responses but audio playback failed.

### Cause

The TTS generation pipeline and frontend playback system were not fully connected.

### Diagnosis

* Checked frontend playback handlers
* Inspected backend payloads
* Validated WebSocket audio delivery
* Monitored browser console output

### Fix

* Integrated XTTS voice generation
* Connected backend audio generation to frontend playback
* Added base64 audio transport
* Validated Web Audio decoding

### What I Learned

I learned how AI-generated speech systems connect backend inference pipelines with frontend audio systems.

---

## 3. Python AI Dependency Compatibility

### Problem

The AI voice stack repeatedly failed due to dependency conflicts.

### Cause

XTTS, Torch, and Transformers are highly version-sensitive, especially on Windows.

### Diagnosis

* Traced runtime errors
* Verified active Python environments
* Compared dependency versions
* Tested stable compatibility combinations

### Fix

* Migrated to Python 3.11
* Created dedicated `.venv311`
* Installed compatible Torch and Transformers versions
* Stabilized XTTS dependencies

### What I Learned

I learned how fragile AI dependency ecosystems can be and gained experience managing virtual environments and AI inference compatibility.

---

## 4. Tauri Desktop Integration

### Problem

The desktop application initially failed to launch correctly because Tauri scripts and dependencies were incomplete.

### Cause

The project merged reference code with a custom architecture, which caused missing scripts and dependency mismatches.

### Diagnosis

* Checked npm scripts
* Verified package.json configuration
* Investigated Tauri startup logs
* Rebuilt missing dependencies

### Fix

* Added Tauri scripts
* Installed required dependencies
* Corrected build configuration
* Stabilized desktop startup flow

### What I Learned

I learned how desktop frontend frameworks coordinate with backend services and how desktop application startup pipelines function.

---

## 5. Audio Processing and Cinematic Voice Effects

### Problem

The default AI voice sounded robotic and lacked cinematic depth.

### Cause

Raw XTTS output lacked post-processing and cinematic audio shaping.

### Diagnosis

* Compared raw audio output
* Tested pitch and speed adjustments
* Investigated audio processing libraries
* Evaluated playback quality

### Fix

* Added Pydub audio processing
* Implemented pitch lowering
* Added compression and normalization
* Applied bass enhancement and cinematic tuning

### What I Learned

I learned how audio post-processing significantly impacts perceived realism in AI voice systems.

---

# Development Philosophy

The project aims to remain:

* Modular
* Local-first
* Windows-compatible
* Open-source-friendly
* AI-focused
* Real-time
* Expandable

The goal is not only to build an AI assistant, but to understand:

* system architecture
* debugging
* frontend/backend integration
* AI tooling
* desktop application engineering
* realtime communication systems
* audio processing
* dependency management

---

# Professional Architecture Explanation

## Architecture

The JARVIS project is structured as a modular desktop AI system instead of a single-file chatbot. The frontend, backend, AI engine, voice system, diagnostics, recovery tools, and safe editing systems are separated into different files and responsibilities.

The frontend is responsible for the desktop interface, orb visualization, microphone input, WebSocket communication, and audio playback. The backend is responsible for AI orchestration, command handling, Ollama communication, diagnostics, recovery, file operations, logging, and safe automation.

This architecture makes the project easier to debug, expand, and explain. Instead of having every feature inside one large file, each system has a clear job.

Professional explanation:

"I designed the project as a modular desktop AI assistant with a Tauri/TypeScript frontend and a FastAPI Python backend. The frontend handles the user interface, voice input, audio playback, and real-time WebSocket communication, while the backend handles AI processing, command routing, diagnostics, recovery tools, and file-system operations. This separation makes the system easier to maintain and extend."

---

## Debugging

Debugging this project required tracing issues across multiple layers:

* Frontend console errors
* Backend terminal logs
* WebSocket messages
* Python traceback errors
* Dependency/version conflicts
* Audio playback behavior
* Ollama response handling
* Windows startup behavior

A major part of the debugging process was identifying whether an issue came from the frontend, backend, voice system, local AI model, Python environment, or Windows configuration.

Professional explanation:

"When debugging JARVIS, I had to trace issues across the full stack. For example, if the assistant responded with text but no audio, I checked the backend response, WebSocket payload, frontend audio player, and browser console. This helped me learn how to isolate problems by following the full data flow from user input to backend processing to frontend output."

---

## Why Systems Were Separated

The systems were separated because JARVIS has many different responsibilities. Keeping everything in one file would make the project harder to debug and easier to break.

Examples:

* `main.py` handles command routing and orchestration
* `live_ws.py` handles real-time WebSocket voice communication
* `tts_engine.py` handles voice generation
* `diagnostics.py` checks system health
* `recovery.py` handles repair/recovery commands
* `safe_writer.py` handles protected AI editing
* `rollback_manager.py` handles file restoration
* `project_analyzer.py` scans the project structure
* `task_engine.py` runs safe terminal tasks

Professional explanation:

"I separated the backend into focused modules so each system had one responsibility. The WebSocket layer handles real-time communication, the TTS engine handles speech generation, the diagnostics layer checks system health, and the safe editing layer manages AI file edits with backup protection. This made the codebase more maintainable and reduced the risk of one feature breaking another."

---

## Rollback Safety

Rollback safety is one of the most important engineering features in the project. Since JARVIS can generate and edit files with AI, it needs protection against bad outputs, syntax errors, or accidental file corruption.

The rollback system works by:

1. Creating a backup before editing a file
2. Letting the AI generate or modify code
3. Running syntax validation
4. Restoring the backup if the edit fails
5. Logging the result

This prevents AI-generated mistakes from permanently damaging the project.

Professional explanation:

"Because the assistant can edit files, I built a safety layer around AI-generated changes. Before modifying a file, the system creates a backup. After the edit, it validates the syntax, and if the result fails, it automatically restores the previous version. This taught me how important rollback systems are when building AI-assisted developer tools."

---

## Diagnostics

The diagnostics system allows JARVIS to inspect its own health. The command `diagnose yourself` checks major parts of the system, including:

* Ollama status
* memory database access
* TTS engine loading
* logs folder
* backups folder
* task logs folder
* CPU, memory, and disk usage

This turns JARVIS from a simple assistant into a system that can report its own operational status.

Professional explanation:

"I added a diagnostics layer so the assistant can inspect its own health. It checks whether the local AI model is reachable, whether the database is accessible, whether the voice engine loads correctly, and whether core folders like logs and backups exist. This gave the project a more production-like monitoring layer."

---

## Backend/Frontend Orchestration

The frontend and backend communicate through WebSockets and HTTP commands. The frontend handles the interactive desktop experience, while the backend processes commands and sends responses back.

The basic flow is:

1. User speaks or types a command
2. Frontend sends the command to the backend
3. Backend routes the command
4. Backend may call Ollama, diagnostics, recovery tools, or file systems
5. Backend returns text and/or audio data
6. Frontend displays the response and plays audio
7. Orb reacts to assistant state and audio

Professional explanation:

"The frontend and backend are orchestrated through real-time communication. The Tauri frontend captures user input and sends it to the FastAPI backend, which determines whether the command should go to Ollama, diagnostics, recovery, file editing, or system monitoring. The backend then sends the response back to the frontend, where it is displayed, spoken, and reflected through the orb animation state."

---

# Future Roadmap

## Short-Term Goals

* Improve cinematic voice quality
* Add streaming speech
* Add wake word detection
* Improve orb animation quality
* Improve response latency
* Add persistent memory
* Add system monitoring commands

## Mid-Term Goals

* Autonomous task execution
* File/project awareness
* Local planning engine
* Voice interruption handling
* Better desktop automation
* Windows integration

## Long-Term Goals

* Vision/screen understanding
* Multi-agent systems
* Autonomous code generation
* Full desktop control
* Mobile integration
* Installer/updater system
* Production deployment

---

# Technologies Used

## Frontend

* Tauri
* TypeScript
* Vite
* Web Audio API
* Web Speech API
* Canvas API

## Backend

* Python
* FastAPI
* Uvicorn
* WebSockets
* Ollama
* XTTS
* Torch
* Transformers
* Pydub

## AI

* llama3.2
* XTTS v2
* Ollama local inference

---

# What I Personally Built and Implemented

## Frontend Contributions

I rebuilt and stabilized the desktop frontend architecture using:

* Tauri
* TypeScript
* Vite
* Web Audio APIs
* WebSocket communication

I integrated:

* Real-time orb rendering
* Audio-reactive visualization
* Desktop UI controls
* Speech recognition
* Audio playback queueing
* Assistant state handling
* WebSocket event flow

I also manually restored and merged large portions of the reference frontend after major file loss and ensured the frontend architecture remained compatible with the backend AI systems.

---

## Backend Contributions

I implemented and stabilized:

* FastAPI backend routing
* Ollama integration
* WebSocket communication pipelines
* Real-time assistant response handling
* AI status systems
* Base64 audio transport
* TTS response generation
* Python virtual environment management

I configured the backend to use:

```text
llama3.2 through Ollama
```

for local AI inference.

---

## AI and Voice Contributions

I integrated:

* XTTS v2 voice generation
* Cinematic audio post-processing
* Local AI voice generation
* Audio normalization
* Pitch shifting
* Audio compression
* Bass enhancement

I also researched and explored:

* Fish Audio
* cinematic voice systems
* API-based TTS providers
* voice cloning approaches
* local vs hosted AI voice architectures

---

## Engineering and Debugging Contributions

I diagnosed and resolved issues involving:

* WebSocket synchronization
* frontend/backend message mismatches
* Tauri desktop startup failures
* AI dependency conflicts
* Python version compatibility
* Torch/Transformers compatibility
* XTTS initialization failures
* frontend audio playback failures
* Windows environment setup
* FFmpeg integration
* real-time audio handling

I used:

* browser DevTools
* PowerShell
* backend runtime logs
* WebSocket tracing
* dependency debugging
* version pinning
* environment rebuilding

throughout the development process.

---

## System Design Contributions

I helped shape the project architecture around:

* local-first AI systems
* Windows desktop integration
* modular AI tooling
* realtime communication
* cinematic assistant interaction
* scalable backend/frontend separation

The project evolved from a reference implementation into a customized Windows-compatible AI desktop assistant integrated with Ollama and local voice systems.

---

# Professional Summary

JARVIS OS is a real-time desktop AI assistant project focused on:

* local AI inference
* real-time communication systems
* desktop application engineering
* AI voice generation
* frontend/backend integration
* realtime audio systems
* modular AI tooling

The project demonstrates practical experience with:

* debugging complex systems
* integrating AI services
* dependency management
* desktop application architecture
* realtime event-driven systems
* asynchronous communication
* voice/audio processing
* AI-assisted software engineering
/**
 * JARVIS — Multi-mode particle visualization.
 *
 * Floating particles with line connections between nearby ones.
 * Lines fade in/out based on state. Transition tumble on state change.
 * Speaking pulls particles closer for denser connections.
 */
/**
 * Voice input (Web Speech API) and audio output (AudioContext) for JARVIS.
 */

// ---------------------------------------------------------------------------
// Speech Recognition
// ---------------------------------------------------------------------------

export interface VoiceInput {
  start(): void;
  stop(): void;
  pause(): void;
  resume(): void;
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
declare const webkitSpeechRecognition: any;

export function createVoiceInput(
  onTranscript: (text: string) => void,
  onError: (msg: string) => void
): VoiceInput {
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const SR =
    (window as any).SpeechRecognition ||
    (typeof webkitSpeechRecognition !== "undefined"
      ? webkitSpeechRecognition
      : null);

  if (!SR) {
    onError("Speech recognition not supported in this browser");
    return { start() {}, stop() {}, pause() {}, resume() {} };
  }

  const recognition = new SR();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = "en-US";

  let shouldListen = false;
  let paused = false;

  let wakeWordActive = false;
  let wakeTimeout: number | null = null;

  recognition.onresult = (event: any) => {
    for (let i = event.resultIndex; i < event.results.length; i++) {
      if (event.results[i].isFinal) {
        const rawText = event.results[i][0].transcript.trim();
        const text = rawText.toLowerCase();

        console.log("[voice heard]", text);

        const wakeWords = ["hey jarvis", "jarvis", "okay jarvis"];

        const heardWakeWord = wakeWords.some((word) =>
          text.includes(word)
        );

        if (heardWakeWord) {
          wakeWordActive = true;

          console.log("[jarvis] wake word detected");

          if (wakeTimeout) {
            clearTimeout(wakeTimeout);
          }

          wakeTimeout = window.setTimeout(() => {
            wakeWordActive = false;
            console.log("[jarvis] returning to standby");
          }, 12000);

          const commandAfterWakeWord = text
            .replace("hey jarvis", "")
            .replace("okay jarvis", "")
            .replace("jarvis", "")
            .trim();

          if (commandAfterWakeWord) {
            onTranscript(commandAfterWakeWord);
          }

          continue;
        }

        if (!wakeWordActive) {
          continue;
        }

        if (rawText) {
          onTranscript(rawText);
        }
      }
    }
  };

  recognition.onend = () => {
    if (shouldListen && !paused) {
      try {
        recognition.start();
      } catch {
        // Already started
      }
    }
  };

  recognition.onerror = (event: any) => {
    if (event.error === "not-allowed") {
      onError("Microphone access denied. Please allow microphone access.");
      shouldListen = false;
    } else if (event.error === "no-speech") {
      // Normal, just restart
    } else if (event.error === "aborted") {
      // Expected during pause
    } else {
      console.warn("[voice] recognition error:", event.error);
    }
  };

  return {
    start() {
      shouldListen = true;
      paused = false;
      try {
        recognition.start();
      } catch {
        // Already started
      }
    },

    stop() {
      shouldListen = false;
      paused = false;
      wakeWordActive = false;

      if (wakeTimeout) {
        clearTimeout(wakeTimeout);
        wakeTimeout = null;
      }

      recognition.stop();
    },

    pause() {
      paused = true;
      recognition.stop();
    },

    resume() {
      paused = false;
      if (shouldListen) {
        try {
          recognition.start();
        } catch {
          // Already started
        }
      }
    },
  };
}

// ---------------------------------------------------------------------------
// Audio Player
// ---------------------------------------------------------------------------

export interface AudioPlayer {
  enqueue(base64: string): Promise<void>;
  stop(): void;
  getAnalyser(): AnalyserNode;
  onFinished(cb: () => void): void;
}

export function createAudioPlayer(): AudioPlayer {
  const audioCtx = new (
    window.AudioContext ||
    (window as any).webkitAudioContext
  )();

  const analyser = audioCtx.createAnalyser();
  analyser.fftSize = 256;
  analyser.smoothingTimeConstant = 0.8;
  analyser.connect(audioCtx.destination);

  const queue: AudioBuffer[] = [];
  let isPlaying = false;
  let currentSource: AudioBufferSourceNode | null = null;
  let finishedCallback: (() => void) | null = null;

  function playNext() {
    if (queue.length === 0) {
      isPlaying = false;
      currentSource = null;
      finishedCallback?.();
      return;
    }

    isPlaying = true;

    const buffer = queue.shift()!;
    const source = audioCtx.createBufferSource();

    source.buffer = buffer;
    source.connect(analyser);
    currentSource = source;

    source.onended = () => {
      if (currentSource === source) {
        playNext();
      }
    };

    source.start();
  }

  return {
    async enqueue(base64: string) {
      if (audioCtx.state === "suspended") {
        await audioCtx.resume();
      }

      try {
        const binary = atob(base64);
        const bytes = new Uint8Array(binary.length);

        for (let i = 0; i < binary.length; i++) {
          bytes[i] = binary.charCodeAt(i);
        }

        const audioBuffer = await audioCtx.decodeAudioData(
          bytes.buffer.slice(0)
        );

        queue.push(audioBuffer);

        if (!isPlaying) {
          playNext();
        }
      } catch (err) {
        console.error("[audio] decode error:", err);

        if (!isPlaying && queue.length > 0) {
          playNext();
        }
      }
    },

    stop() {
      queue.length = 0;

      if (currentSource) {
        try {
          currentSource.stop();
        } catch {
          // Already stopped
        }

        currentSource = null;
      }

      isPlaying = false;
    },

    getAnalyser() {
      return analyser;
    },

    onFinished(cb: () => void) {
      finishedCallback = cb;
    },
  };
}