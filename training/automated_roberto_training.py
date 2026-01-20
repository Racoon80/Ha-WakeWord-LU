#!/usr/bin/env python3
"""
Automated training for Roberto wake word using Fish-Speech TTS
Generates synthetic samples and trains openWakeWord model
"""

import os
import sys
import json
import time
import wave
import random
import requests
import numpy as np
from pathlib import Path
from datetime import datetime

# Configuration
TTS_URL = "http://192.168.106.15"  # Luxembourgish Fish-Speech TTS
WAKE_WORD = "Roberto"
LANGUAGE = "lb"  # Luxembourgish
SAMPLE_RATE = 16000
MODEL_NAME = f"roberto_{LANGUAGE}"

# Training parameters
POSITIVE_SAMPLES = 200  # Number of "Roberto" samples
NEGATIVE_SAMPLES = 1000  # Background/other words
VARIATIONS_PER_SAMPLE = 3  # Speed/pitch variations

# Luxembourgish words for negative samples
NEGATIVE_WORDS = [
    "Hallo", "Moien", "Äddi", "Merci", "Villmools", "Wéi", "Wat",
    "Wann", "Wou", "Wien", "Firwat", "Wéivill", "Jo", "Nee",
    "Gutt", "Schlecht", "Grouss", "Kleng", "Vill", "Wéineg",
    "Ech", "Du", "Hien", "Si", "Mir", "Dir", "Sie",
    "Dag", "Nuecht", "Moies", "Mëttes", "Owend",
    "Lëtzebuerg", "Freed", "Traureg", "Schéin", "Mies",
]

class RobertoTrainer:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.data_dir = self.base_dir / "data"
        self.positive_dir = self.data_dir / "positive"
        self.negative_dir = self.data_dir / "negative"
        self.models_dir = self.base_dir / "models"
        self.logs_dir = self.base_dir / "logs"

        # Create directories
        for dir_path in [self.positive_dir, self.negative_dir, self.models_dir, self.logs_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        self.session = requests.Session()
        self.session.timeout = 30

    def log(self, message):
        """Log message to console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_msg = f"[{timestamp}] {message}"
        print(log_msg)

        log_file = self.logs_dir / f"training_{datetime.now().strftime('%Y%m%d')}.log"
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(log_msg + "\n")

    def generate_tts_sample(self, text, speed=1.0, output_file=None):
        """Generate audio sample using Fish-Speech TTS"""
        try:
            # Try common TTS API endpoints
            endpoints = [
                f"{TTS_URL}/api/tts",
                f"{TTS_URL}/tts",
                f"{TTS_URL}/generate",
            ]

            for endpoint in endpoints:
                try:
                    # Try different payload formats
                    payloads = [
                        {"text": text, "speed": speed, "language": LANGUAGE},
                        {"text": text, "speed": speed},
                        {"input": text, "speed": speed},
                    ]

                    for payload in payloads:
                        response = self.session.post(
                            endpoint,
                            json=payload,
                            headers={"Content-Type": "application/json"}
                        )

                        if response.status_code == 200:
                            # Save audio file
                            if output_file:
                                with open(output_file, 'wb') as f:
                                    f.write(response.content)
                                return True
                            return response.content
                except Exception:
                    continue

            self.log(f"WARNING: Could not generate TTS for '{text}'. Skipping...")
            return None

        except Exception as e:
            self.log(f"ERROR generating TTS: {e}")
            return None

    def convert_to_wav(self, audio_data, output_file):
        """Convert audio data to 16kHz mono WAV format"""
        try:
            # If audio_data is already a file path, just ensure correct format
            # This is a placeholder - actual conversion would depend on TTS output format
            with wave.open(str(output_file), 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(SAMPLE_RATE)
                if isinstance(audio_data, bytes):
                    wf.writeframes(audio_data)
            return True
        except Exception as e:
            self.log(f"ERROR converting audio: {e}")
            return False

    def generate_positive_samples(self):
        """Generate positive samples (Roberto)"""
        self.log("=" * 60)
        self.log(f"Generating {POSITIVE_SAMPLES} positive samples...")
        self.log("=" * 60)

        count = 0
        for i in range(POSITIVE_SAMPLES):
            # Vary speed for different pronunciations
            speed = random.uniform(0.85, 1.15)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = self.positive_dir / f"roberto_{timestamp}.wav"

            if self.generate_tts_sample(WAKE_WORD, speed=speed, output_file=filename):
                count += 1
                if count % 10 == 0:
                    self.log(f"  Generated {count}/{POSITIVE_SAMPLES} positive samples...")

            # Small delay to avoid overwhelming the TTS server
            time.sleep(0.1)

        self.log(f"OK - Generated {count} positive samples")
        return count

    def generate_negative_samples(self):
        """Generate negative samples (other words)"""
        self.log("=" * 60)
        self.log(f"Generating {NEGATIVE_SAMPLES} negative samples...")
        self.log("=" * 60)

        count = 0
        for i in range(NEGATIVE_SAMPLES):
            # Random word from negative list
            word = random.choice(NEGATIVE_WORDS)
            speed = random.uniform(0.85, 1.15)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            filename = self.negative_dir / f"negative_{timestamp}.wav"

            if self.generate_tts_sample(word, speed=speed, output_file=filename):
                count += 1
                if count % 50 == 0:
                    self.log(f"  Generated {count}/{NEGATIVE_SAMPLES} negative samples...")

            time.sleep(0.05)

        self.log(f"OK - Generated {count} negative samples")
        return count

    def train_model(self):
        """Train the wake word model using openWakeWord"""
        self.log("=" * 60)
        self.log("Training Roberto wake word model...")
        self.log("=" * 60)

        try:
            # Check if openWakeword is installed
            try:
                import openwakeword
                from openwakeword.train import train_model
            except ImportError:
                self.log("Installing openWakeWord...")
                os.system(f"{sys.executable} -m pip install openwakeword")
                from openwakeword.train import train_model

            # Training configuration
            config = {
                "model_name": MODEL_NAME,
                "positive_data_dir": str(self.positive_dir),
                "negative_data_dir": str(self.negative_dir),
                "output_dir": str(self.models_dir),
                "sample_rate": SAMPLE_RATE,
                "epochs": 100,
                "batch_size": 32,
            }

            self.log(f"Training with config: {json.dumps(config, indent=2)}")

            # Train the model
            train_model(**config)

            model_file = self.models_dir / f"{MODEL_NAME}.tflite"
            if model_file.exists():
                size = model_file.stat().st_size / 1024
                self.log(f"OK - Model trained successfully!")
                self.log(f"     Output: {model_file} ({size:.1f} KB)")
                return str(model_file)
            else:
                self.log("ERROR - Model file not created")
                return None

        except Exception as e:
            self.log(f"ERROR during training: {e}")
            import traceback
            traceback.print_exc()
            return None

    def run_full_training(self):
        """Run complete training pipeline"""
        self.log("=" * 60)
        self.log("AUTOMATED ROBERTO WAKE WORD TRAINING")
        self.log("=" * 60)
        self.log(f"TTS Server: {TTS_URL}")
        self.log(f"Wake Word: {WAKE_WORD}")
        self.log(f"Language: {LANGUAGE}")
        self.log("")

        start_time = time.time()

        # Step 1: Generate positive samples
        positive_count = self.generate_positive_samples()

        # Step 2: Generate negative samples
        negative_count = self.generate_negative_samples()

        # Step 3: Train the model
        if positive_count > 50 and negative_count > 100:
            model_path = self.train_model()

            if model_path:
                elapsed = time.time() - start_time
                self.log("")
                self.log("=" * 60)
                self.log("TRAINING COMPLETE!")
                self.log("=" * 60)
                self.log(f"Positive samples: {positive_count}")
                self.log(f"Negative samples: {negative_count}")
                self.log(f"Model: {model_path}")
                self.log(f"Time elapsed: {elapsed/60:.1f} minutes")
                self.log("")
                self.log("Next step: Deploy to Unraid")
                self.log(f"  Copy {model_path}")
                self.log(f"  To: /mnt/user/appdata/ai/roberto-models/")
                return model_path
        else:
            self.log("ERROR - Insufficient samples generated")
            self.log(f"  Positive: {positive_count} (need > 50)")
            self.log(f"  Negative: {negative_count} (need > 100)")
            return None

def main():
    trainer = RobertoTrainer()
    model_path = trainer.run_full_training()

    if model_path:
        print("\nTraining successful!")
        sys.exit(0)
    else:
        print("\nTraining failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
