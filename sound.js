// Web Audio API Music Box & Paper Unfolding Sound Effects
// 100% offline, zero external dependencies

class CardSoundEngine {
  constructor() {
    this.ctx = null;
    this.isPlayingMusic = false;
    this.musicTimer = null;
    this.notes = [
      // "Can't Help Falling In Love" romantic music-box melody
      { note: "C4", duration: 1.0 },
      { note: "G4", duration: 1.0 },
      { note: "C5", duration: 1.5 },
      { note: "B4", duration: 0.5 },
      { note: "A4", duration: 1.0 },
      { note: "F4", duration: 0.5 },
      { note: "G4", duration: 1.5 },
      { note: "A4", duration: 1.0 },
      { note: "B4", duration: 1.0 },
      { note: "C5", duration: 1.5 },
      { note: "D5", duration: 0.5 },
      { note: "E5", duration: 1.0 },
      { note: "D5", duration: 0.5 },
      { note: "C5", duration: 1.5 },
      { note: "G4", duration: 1.0 },
      { note: "A4", duration: 1.0 },
      { note: "F4", duration: 1.5 },
      { note: "E4", duration: 0.5 },
      { note: "D4", duration: 1.0 },
      { note: "C4", duration: 2.0 }
    ];

    this.freqMap = {
      "C4": 261.63, "D4": 293.66, "E4": 329.63, "F4": 349.23,
      "G4": 392.00, "A4": 440.00, "B4": 493.88,
      "C5": 523.25, "D5": 587.33, "E5": 659.25, "F5": 698.46, "G5": 783.99
    };
  }

  init() {
    if (!this.ctx) {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.ctx = new AudioContext();
    }
    if (this.ctx.state === "suspended") {
      this.ctx.resume();
    }
  }

  // Realistic paper unfolding rustle sound
  playPaperRustle() {
    this.init();
    if (!this.ctx) return;

    const bufferSize = this.ctx.sampleRate * 0.35; // 350ms
    const buffer = this.ctx.createBuffer(1, bufferSize, this.ctx.sampleRate);
    const data = buffer.getChannelData(0);

    for (let i = 0; i < bufferSize; i++) {
      // White noise with decay envelope
      const decay = Math.exp(-i / (this.ctx.sampleRate * 0.08));
      data[i] = (Math.random() * 2 - 1) * decay;
    }

    const noise = this.ctx.createBufferSource();
    noise.buffer = buffer;

    // Filter to make it sound like thick cardstock / paper
    const filter = this.ctx.createBiquadFilter();
    filter.type = "bandpass";
    filter.frequency.value = 1100;
    filter.Q.value = 1.8;

    const gain = this.ctx.createGain();
    gain.gain.setValueAtTime(0.25, this.ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.35);

    noise.connect(filter);
    filter.connect(gain);
    gain.connect(this.ctx.destination);

    noise.start();
  }

  // Play a single bell/music box chime note
  playChimeNote(freq, duration = 1.0) {
    if (!this.ctx) return;

    const osc = this.ctx.createOscillator();
    const oscHarmonic = this.ctx.createOscillator();
    const gain = this.ctx.createGain();

    osc.type = "sine";
    osc.frequency.setValueAtTime(freq, this.ctx.currentTime);

    // Soft chime harmonic overtone
    oscHarmonic.type = "sine";
    oscHarmonic.frequency.setValueAtTime(freq * 2.76, this.ctx.currentTime);

    const now = this.ctx.currentTime;
    gain.gain.setValueAtTime(0.2, now);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + duration * 1.8);

    osc.connect(gain);
    oscHarmonic.connect(gain);
    gain.connect(this.ctx.destination);

    osc.start(now);
    oscHarmonic.start(now);
    osc.stop(now + duration * 2.0);
    oscHarmonic.stop(now + duration * 2.0);
  }

  // Toggle romantic music box playback
  toggleMusic(onToggleCallback) {
    this.init();
    if (this.isPlayingMusic) {
      this.stopMusic();
      if (onToggleCallback) onToggleCallback(false);
    } else {
      this.startMusic();
      if (onToggleCallback) onToggleCallback(true);
    }
  }

  startMusic() {
    this.isPlayingMusic = true;
    let noteIndex = 0;

    const playNext = () => {
      if (!this.isPlayingMusic) return;

      const item = this.notes[noteIndex];
      const freq = this.freqMap[item.note] || 440;
      this.playChimeNote(freq, item.duration);

      const delay = item.duration * 680; // BPM speed
      noteIndex = (noteIndex + 1) % this.notes.length;

      this.musicTimer = setTimeout(playNext, delay);
    };

    playNext();
  }

  stopMusic() {
    this.isPlayingMusic = false;
    if (this.musicTimer) {
      clearTimeout(this.musicTimer);
      this.musicTimer = null;
    }
  }
}

const SOUND = new CardSoundEngine();
