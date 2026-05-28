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
  recognition.maxAlternatives = 1;

  let shouldListen = false;
  let paused = false;

  let wakeWordActive = false;
  let wakeTimeout: number | null = null;

  async function requestMicrophonePermission(): Promise<boolean> {
    try {
      if (!navigator.mediaDevices?.getUserMedia) {
        onError("Microphone API is not available in this environment.");
        return false;
      }

      const stream = await navigator.mediaDevices.getUserMedia({
        audio: true,
      });

      stream.getTracks().forEach((track) => track.stop());

      console.log("[voice] microphone permission granted");
      return true;
    } catch (err) {
      console.error("[voice] microphone permission failed", err);

      onError(
        "Microphone permission denied. Please allow microphone access in Windows and browser settings."
      );

      return false;
    }
  }

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
      window.setTimeout(() => {
        try {
          recognition.start();
        } catch {
          // Already started
        }
      }, 250);
    }
  };

  recognition.onerror = (event: any) => {
    console.warn("[voice] recognition error:", event.error);

    if (event.error === "not-allowed") {
      onError("Microphone access denied. Please allow microphone access.");
      shouldListen = false;
    } else if (event.error === "no-speech") {
      // Normal, just restart
    } else if (event.error === "aborted") {
      // Expected during pause
    } else {
      onError(`Speech recognition error: ${event.error}`);
    }
  };

  return {
    async start() {
      shouldListen = true;
      paused = false;

      const allowed = await requestMicrophonePermission();

      if (!allowed) {
        shouldListen = false;
        return;
      }

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
        requestMicrophonePermission().then((allowed) => {
          if (!allowed) return;

          try {
            recognition.start();
          } catch {
            // Already started
          }
        });
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