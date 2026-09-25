import numpy as np
import wave
import struct

sample_rate = 44100

# Note frequency dictionary (Hz)
notes = {
    'C2': 65.41, 'D2': 73.42, 'E2': 82.41, 'F2': 87.31, 'G2': 98.00, 'A2': 110.00, 'B2': 123.47,
    'C3': 130.81, 'D3': 146.83, 'E3': 164.81, 'F3': 174.61, 'G3': 196.00, 'A3': 220.00, 'B3': 246.94,
    'C4': 261.63, 'D4': 293.66, 'E4': 329.63, 'F4': 349.23, 'G4': 392.00, 'A4': 440.00, 'B4': 493.88,
    'C5': 523.25, 'D5': 587.33, 'E5': 659.25, 'F5': 698.46, 'G5': 783.99, 'A5': 880.00, 'B5': 987.77,
    'C6': 1046.50
}

def render_piano_note(freq, duration, velocity=0.8):
    length = int(sample_rate * duration)
    t = np.linspace(0, duration, length, False)
    
    harmonics = [
        (1.0, 1.0, 1.2),
        (2.0, 0.6, 1.6),
        (3.0, 0.35, 2.2),
        (4.0, 0.22, 2.8),
        (5.0, 0.12, 3.4),
        (6.0, 0.07, 4.0),
        (7.0, 0.04, 4.8)
    ]
    tone = np.zeros(length, dtype=np.float32)
    for h_mult, h_amp, decay_mult in harmonics:
        f = freq * h_mult
        env = np.exp(-t * (1.6 * decay_mult))
        tone += h_amp * np.sin(2 * np.pi * f * t) * env
        
    attack_samples = min(int(sample_rate * 0.008), length)
    tone[:attack_samples] *= np.linspace(0, 1, attack_samples)
    
    # Warm sub-harmonic depth for piano soundboard
    sub = 0.2 * np.sin(2 * np.pi * (freq * 0.5) * t) * np.exp(-t * 2.0)
    return (tone + sub) * velocity

def render_strings_pad(freq, duration, velocity=0.25):
    length = int(sample_rate * duration)
    t = np.linspace(0, duration, length, False)
    
    # Warm, lush ensemble with subtle chorus detune
    detune1 = 1.002
    detune2 = 0.998
    s1 = np.sin(2 * np.pi * freq * t)
    s2 = 0.7 * np.sin(2 * np.pi * (freq * 2.0 * detune1) * t)
    s3 = 0.5 * np.sin(2 * np.pi * (freq * 3.0 * detune2) * t)
    raw = (s1 + s2 + s3)
    
    # Slow attack and gentle release
    att = int(sample_rate * 0.4)
    rel = int(sample_rate * 0.5)
    env = np.ones(length, dtype=np.float32)
    if length > att + rel:
        env[:att] = np.linspace(0, 1, att)
        env[-rel:] = np.linspace(1, 0, rel)
    return raw * env * velocity

bpm = 64
beat_sec = 60.0 / bpm
total_beats = 48  # 12 measures of 4/4 = 45 seconds
total_duration = total_beats * beat_sec + 4.0 # with ring-out
total_samples = int(sample_rate * total_duration)

left_channel = np.zeros(total_samples, dtype=np.float32)
right_channel = np.zeros(total_samples, dtype=np.float32)

def add_audio(start_beat, audio, pan=0.0):
    start_sample = int(start_beat * beat_sec * sample_rate)
    end_sample = start_sample + len(audio)
    if end_sample > total_samples:
        audio = audio[:total_samples - start_sample]
        end_sample = total_samples
        
    left_gain = np.cos((pan + 1.0) * np.pi / 4.0)
    right_gain = np.sin((pan + 1.0) * np.pi / 4.0)
    
    left_channel[start_sample:end_sample] += audio * left_gain
    right_channel[start_sample:end_sample] += audio * right_gain

# 12-Measure Romantic Chord Progression:
# Measure 1: C major
# Measure 2: G/B
# Measure 3: Am
# Measure 4: Em/G
# Measure 5: F major
# Measure 6: C/E
# Measure 7: Dm7
# Measure 8: G7sus4 -> G7
# Measure 9: F major
# Measure 10: G major
# Measure 11: Am
# Measure 12: C major (gentle romantic resolution)

chords = [
    # (root, bass, arpeggio notes)
    (0,  'C3', ['C3', 'G3', 'C4', 'E4', 'G4', 'E4', 'C4', 'G3']),
    (4,  'B2', ['B2', 'G3', 'D4', 'G4', 'B4', 'G4', 'D4', 'G3']),
    (8,  'A2', ['A2', 'E3', 'A3', 'C4', 'E4', 'C4', 'A3', 'E3']),
    (12, 'G2', ['G2', 'E3', 'G3', 'B3', 'E4', 'B3', 'G3', 'E3']),
    (16, 'F2', ['F2', 'C3', 'F3', 'A3', 'C4', 'A3', 'F3', 'C3']),
    (20, 'E2', ['E2', 'C3', 'E3', 'G3', 'C4', 'G3', 'E3', 'C3']),
    (24, 'D2', ['D2', 'A2', 'D3', 'F3', 'A3', 'F3', 'D3', 'A2']),
    (28, 'G2', ['G2', 'D3', 'G3', 'B3', 'D4', 'B3', 'G3', 'D3']),
    (32, 'F2', ['F2', 'C3', 'F3', 'A3', 'C4', 'F4', 'C4', 'A3']),
    (36, 'G2', ['G2', 'D3', 'G3', 'B3', 'D4', 'G4', 'D4', 'B3']),
    (40, 'A2', ['A2', 'E3', 'A3', 'C4', 'E4', 'A4', 'E4', 'C4']),
    (44, 'C2', ['C2', 'G2', 'C3', 'E3', 'G3', 'C4', 'E4', 'G4'])
]

# Add Left Hand Arpeggios & Strings Pad
for start_b, bass_note, arp in chords:
    # Warm strings pad beneath chord
    pad_note = notes[arp[0]]
    pad_wave = render_strings_pad(pad_note, beat_sec * 4.2, velocity=0.22)
    add_audio(start_b, pad_wave, pan=-0.2)
    pad_wave_hi = render_strings_pad(notes[arp[3]], beat_sec * 4.2, velocity=0.18)
    add_audio(start_b, pad_wave_hi, pan=0.2)
    
    # Deep bass note on beat 1
    bass_wave = render_piano_note(notes[bass_note], beat_sec * 3.5, velocity=0.85)
    add_audio(start_b, bass_wave, pan=-0.3)
    
    # Flowing arpeggio notes (half beat each = 8 notes per measure)
    for i, n_str in enumerate(arp):
        t_note = start_b + i * 0.5
        v = 0.55 if i != 0 else 0.7
        n_wave = render_piano_note(notes[n_str], beat_sec * 2.0, velocity=v)
        add_audio(t_note, n_wave, pan=-0.15 + (i % 2) * 0.1)

# Soulful Romantic Vocal Melody (Right Hand Piano / Celesta)
# Melody inspired by "Can't Help Falling In Love" / "Until I Found You"
melody = [
    # Measure 1 (C)
    (0.0, 'G4', 1.0, 0.85),
    (1.0, 'C5', 2.0, 0.90),
    (3.0, 'B4', 1.0, 0.80),
    # Measure 2 (G/B)
    (4.0, 'A4', 1.5, 0.85),
    (5.5, 'G4', 2.5, 0.85),
    # Measure 3 (Am)
    (8.0, 'A4', 1.0, 0.85),
    (9.0, 'B4', 1.0, 0.85),
    (10.0, 'C5', 2.0, 0.95),
    # Measure 4 (Em)
    (12.0, 'D5', 1.5, 0.85),
    (13.5, 'C5', 2.5, 0.85),
    # Measure 5 (F)
    (16.0, 'C5', 1.0, 0.85),
    (17.0, 'D5', 1.0, 0.85),
    (18.0, 'E5', 2.0, 0.95),
    # Measure 6 (C/E)
    (20.0, 'D5', 1.5, 0.85),
    (21.5, 'C5', 2.5, 0.85),
    # Measure 7 (Dm7)
    (24.0, 'B4', 1.0, 0.80),
    (25.0, 'A4', 1.0, 0.80),
    (26.0, 'G4', 2.0, 0.85),
    # Measure 8 (G7)
    (28.0, 'A4', 1.5, 0.85),
    (29.5, 'B4', 2.5, 0.90),
    # Measure 9 (F) - Climax
    (32.0, 'C5', 1.0, 0.90),
    (33.0, 'E5', 2.0, 1.00),
    (35.0, 'D5', 1.0, 0.85),
    # Measure 10 (G)
    (36.0, 'C5', 1.5, 0.90),
    (37.5, 'B4', 2.5, 0.85),
    # Measure 11 (Am)
    (40.0, 'A4', 1.5, 0.90),
    (41.5, 'G4', 1.5, 0.85),
    (43.0, 'F4', 1.0, 0.80),
    # Measure 12 (C Resolution)
    (44.0, 'E4', 2.0, 0.85),
    (46.0, 'C4', 3.0, 0.90)
]

for m_beat, m_note, m_dur, m_vel in melody:
    m_wave = render_piano_note(notes[m_note], beat_sec * m_dur * 1.5, velocity=m_vel)
    add_audio(m_beat, m_wave, pan=0.15)
    
    # Add gentle celesta harmonic sparkle above key melody notes
    if m_dur >= 1.5:
        sparkle_freq = notes[m_note] * 2.0
        if sparkle_freq < 2000:
            sp_wave = render_piano_note(sparkle_freq, beat_sec * m_dur * 1.2, velocity=m_vel * 0.35)
            add_audio(m_beat + 0.02, sp_wave, pan=0.35)

# Simple Schroeder-style Reverb for warm acoustic concert room ambiance
def apply_reverb(signal, delay_ms, decay):
    delay_samples = int(sample_rate * delay_ms / 1000.0)
    out = np.copy(signal)
    for i in range(delay_samples, len(signal)):
        out[i] += out[i - delay_samples] * decay
    return out

print('Applying acoustic room reverb...')
rev_l = apply_reverb(left_channel, 35, 0.35)
rev_r = apply_reverb(right_channel, 48, 0.35)
rev_l = apply_reverb(rev_l, 72, 0.25)
rev_r = apply_reverb(rev_r, 89, 0.25)

left_final = left_channel * 0.75 + rev_l * 0.25
right_final = right_channel * 0.75 + rev_r * 0.25

# Normalize to prevent any clipping
max_peak = max(np.max(np.abs(left_final)), np.max(np.abs(right_final)))
if max_peak > 0:
    left_final = (left_final / max_peak) * 0.88
    right_final = (right_final / max_peak) * 0.88

# Export 16-bit Stereo PCM WAV
stereo_interleaved = np.empty((total_samples * 2,), dtype=np.int16)
stereo_interleaved[0::2] = (left_final * 32767).astype(np.int16)
stereo_interleaved[1::2] = (right_final * 32767).astype(np.int16)

with wave.open('romantic_love_song.wav', 'wb') as wav_file:
    wav_file.setnchannels(2)
    wav_file.setsampwidth(2)
    wav_file.setframerate(sample_rate)
    wav_file.writeframes(stereo_interleaved.tobytes())

print(f'Successfully generated romantic_love_song.wav ({total_duration:.1f}s)!')
