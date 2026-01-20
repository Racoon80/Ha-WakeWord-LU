#!/usr/bin/env python3
"""
Audio sample collection script for 'Roberto' wake word training
Records audio samples for training the Luxembourgish wake word
"""

import os
import wave
import pyaudio
from pathlib import Path
from datetime import datetime

# Audio configuration
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK = 1024
RECORD_SECONDS = 2
FORMAT = pyaudio.paInt16

def record_sample(output_dir, sample_type="positive"):
    """Record a single audio sample"""

    output_path = Path(output_dir) / sample_type
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = output_path / f"{sample_type}_{timestamp}.wav"

    audio = pyaudio.PyAudio()

    print(f"\nRecording {sample_type} sample...")
    if sample_type == "positive":
        print("Say 'Roberto' clearly when recording starts...")
    else:
        print("Recording background noise/other speech...")

    input("Press Enter to start recording...")

    stream = audio.open(
        format=FORMAT,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK
    )

    print("Recording... (2 seconds)")
    frames = []

    for _ in range(0, int(SAMPLE_RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Recording complete!")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Save audio file
    with wave.open(str(filename), 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(b''.join(frames))

    print(f"Saved: {filename}")
    return filename

def collect_training_data():
    """Interactive session to collect multiple samples"""

    print("=" * 60)
    print("Roberto Wake Word - Sample Collection")
    print("=" * 60)
    print("\nThis tool helps you collect audio samples for training.")
    print("\nRecommended samples:")
    print("  - Positive (Roberto): 100-200 samples")
    print("  - Negative (other): 500-1000 samples")
    print("\nTips:")
    print("  - Record in different environments")
    print("  - Use different voices/accents")
    print("  - Vary speaking speed and volume")
    print("  - Include background noise in negative samples")
    print("=" * 60)

    output_dir = "data"

    positive_count = 0
    negative_count = 0

    while True:
        print("\n" + "=" * 60)
        print(f"Samples collected - Positive: {positive_count}, Negative: {negative_count}")
        print("=" * 60)
        print("\nOptions:")
        print("  1. Record positive sample (say 'Roberto')")
        print("  2. Record negative sample (background noise/other speech)")
        print("  3. Quit")

        choice = input("\nEnter choice (1-3): ").strip()

        if choice == "1":
            record_sample(output_dir, "positive")
            positive_count += 1
        elif choice == "2":
            record_sample(output_dir, "negative")
            negative_count += 1
        elif choice == "3":
            print(f"\nCollection complete!")
            print(f"Total positive samples: {positive_count}")
            print(f"Total negative samples: {negative_count}")
            print(f"\nSamples saved in: {output_dir}/")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    try:
        collect_training_data()
    except KeyboardInterrupt:
        print("\n\nCollection interrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure PyAudio is installed: pip install pyaudio")
