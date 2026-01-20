# Ha-WakeWord-LU

Luxembourgish wake word "Roberto" for Home Assistant using Wyoming Protocol and openWakeWord.

## Overview

This project provides a custom wake word detector for Home Assistant that responds to "Roberto" in Luxembourgish. It uses the Wyoming protocol for seamless integration with Home Assistant's voice assistant pipeline.

## Features

- 🇱🇺 Luxembourgish wake word detection
- 🎯 Custom trained model for "Roberto"
- 🔌 Wyoming protocol compatible
- 🐳 Docker deployment on Unraid
- 🎮 GPU-accelerated training

## Architecture

- **Wake Word Engine**: openWakeWord
- **Protocol**: Wyoming
- **Deployment**: Docker on Unraid
- **Network**: br0.106 (192.168.106.51)
- **Path**: /mnt/user/appdata/ai

## Quick Start

### Prerequisites

- Unraid server with GPU support
- Docker and Docker Compose
- Network br0.106 configured
- Microphone for training samples

### Installation

1. Clone this repository to your Unraid server:
```bash
cd /mnt/user/appdata/ai
git clone https://github.com/yourusername/Ha-WakeWord-LU.git
cd Ha-WakeWord-LU
```

2. Deploy the wake word service:
```bash
docker-compose up -d
```

3. Configure Home Assistant to use the wake word service at `tcp://192.168.106.51:10400`

## Training Your Own Model

### Step 1: Collect Audio Samples

Run the sample collection script:
```bash
cd training
pip install -r requirements.txt
python collect_samples.py
```

**Recommendations:**
- Record 100-200 positive samples (saying "Roberto")
- Record 500-1000 negative samples (background noise, other speech)
- Use different voices, accents, and environments
- Vary speaking speed and volume

### Step 2: Train the Model

Using the training Docker container:
```bash
docker-compose -f docker-compose-training.yml up
```

Or train locally:
```bash
cd training
python train_roberto.py --train
```

### Step 3: Deploy the Model

Copy the trained model to the models directory:
```bash
cp training/models/roberto_lb.tflite /mnt/user/appdata/ai/roberto-models/
```

Restart the wake word service:
```bash
docker-compose restart
```

## Configuration

### Docker Compose

The service is configured to:
- Listen on port 10400 (Wyoming protocol)
- Load custom model from `/mnt/user/appdata/ai/roberto-models/`
- Use static IP 192.168.106.51 on network br0.106

### Home Assistant Integration

Add to your `configuration.yaml`:
```yaml
wyoming:
  - uri: tcp://192.168.106.51:10400
```

Or configure via UI:
1. Settings → Devices & Services
2. Add Integration → Wyoming Protocol
3. Host: 192.168.106.51
4. Port: 10400

## File Structure

```
Ha-WakeWord-LU/
├── docker-compose.yml              # Production deployment
├── docker-compose-training.yml     # Training container
├── config/                         # Configuration files
├── training/
│   ├── train_roberto.py           # Training script
│   ├── collect_samples.py         # Sample collection tool
│   ├── requirements.txt           # Python dependencies
│   └── data/
│       ├── positive/              # "Roberto" samples
│       └── negative/              # Background samples
├── models/                        # Trained models
├── Notes/
│   └── notes.md                   # Project notes
└── README.md
```

## Troubleshooting

### Wake word not detected
- Check microphone configuration in Home Assistant
- Verify the service is running: `docker logs ha-wakeword-lu`
- Test with different voice volumes and distances

### Training issues
- Ensure sufficient samples (min 100 positive, 500 negative)
- Check GPU availability for training
- Verify audio format (16kHz, mono, WAV)

### Connection issues
- Verify network br0.106 is configured
- Check firewall rules for port 10400
- Test connection: `nc -zv 192.168.106.51 10400`

## Technical Details

- **Sample Rate**: 16kHz
- **Channels**: Mono
- **Format**: WAV (PCM 16-bit)
- **Model Framework**: TensorFlow Lite
- **Protocol**: Wyoming Protocol v1.0

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

MIT License

## Credits

- [openWakeWord](https://github.com/dscripka/openWakeWord) - Wake word detection engine
- [Wyoming Protocol](https://github.com/rhasspy/wyoming) - Home Assistant voice protocol
- Home Assistant Community

## Version

v1.0 - Initial release with Luxembourgish "Roberto" wake word support
