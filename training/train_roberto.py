#!/usr/bin/env python3
"""
Training script for Luxembourgish wake word 'Roberto'
Uses openWakeWord training framework
"""

import os
import sys
from pathlib import Path

# Training configuration
WAKE_WORD = "roberto"
LANGUAGE = "lb"  # Luxembourgish
SAMPLE_RATE = 16000
MODEL_NAME = f"{WAKE_WORD}_{LANGUAGE}"

def setup_training_environment():
    """Set up directories and dependencies for training"""
    print("Setting up training environment for 'Roberto' wake word...")

    # Create directories
    dirs = [
        "data/positive",  # Audio samples of "Roberto"
        "data/negative",  # Background noise and other speech
        "models",
        "logs"
    ]

    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {dir_path}")

    print("\nTraining directory structure created!")
    print("\nNext steps:")
    print("1. Place audio samples of 'Roberto' in data/positive/")
    print("2. Place background noise samples in data/negative/")
    print("3. Run training with: python train_roberto.py --train")

def train_model():
    """Train the wake word model"""
    try:
        from openwakeword.train import train_model as train

        print(f"Training wake word model: {MODEL_NAME}")

        config = {
            "model_name": MODEL_NAME,
            "positive_samples_dir": "data/positive",
            "negative_samples_dir": "data/negative",
            "output_dir": "models",
            "sample_rate": SAMPLE_RATE,
            "epochs": 100,
            "batch_size": 32,
        }

        train(**config)

        print(f"\nModel trained successfully!")
        print(f"Model saved to: models/{MODEL_NAME}.tflite")

    except ImportError:
        print("Error: openwakeword not installed")
        print("Install with: pip install openwakeword")
        sys.exit(1)

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--train":
        train_model()
    else:
        setup_training_environment()

if __name__ == "__main__":
    main()
