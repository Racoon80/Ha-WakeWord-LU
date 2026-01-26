# Porcupine "Albert" Wake Word for Home Assistant

Custom wake word detection using Picovoice Porcupine with "Albert" for Luxembourgish voice assistant.

## Overview

This setup uses **Porcupine** by Picovoice to detect the custom wake word **"Albert"** for your Home Assistant voice pipeline. Porcupine offers highly accurate, on-device wake word detection with minimal CPU usage.

## Why "Albert"?

"Albert" is a fitting wake word for a Luxembourgish voice assistant:
- Short and distinct
- Easy to pronounce in Luxembourgish
- Could reference Albert II, Grand Duke of Luxembourg
- Works well with Porcupine's detection algorithms

## Prerequisites

1. **Picovoice Access Key** (Free)
   - Sign up at https://console.picovoice.ai/
   - Create a new access key
   - Save it as environment variable: `PORCUPINE_ACCESS_KEY`

2. **Custom Wake Word Model** (`albert.ppn`)
   - Train at https://console.picovoice.ai/
   - Go to Porcupine section
   - Create new wake word for "Albert"
   - Download the `.ppn` model file
   - Place in `./models/albert.ppn`

## Quick Start

### Step 1: Get Picovoice Access Key

```bash
# Sign up at https://console.picovoice.ai/
# Navigate to: Account → Access Keys
# Create new access key
# Copy the key
```

### Step 2: Train "Albert" Wake Word

1. Go to https://console.picovoice.ai/
2. Navigate to **Porcupine** section
3. Click **"Train Wake Word"**
4. Enter wake phrase: `albert`
5. Select language: **English** (or closest match)
6. Click **Train**
7. Wait for training to complete (usually a few minutes)
8. Download the `albert.ppn` file

### Step 3: Set Up Environment

```bash
# Create .env file with your access key
echo "PORCUPINE_ACCESS_KEY=your_access_key_here" > .env
```

### Step 4: Place Model File

```bash
# Create models directory if it doesn't exist
mkdir -p models

# Copy your downloaded albert.ppn file
cp ~/Downloads/albert.ppn ./models/
```

### Step 5: Deploy

```bash
# Build and start the container
docker-compose -f docker-compose-porcupine.yml up -d

# Check logs
docker logs -f ha-wakeword-albert
```

You should see:
```
Starting Porcupine wake word detection...
Wake words: albert
Sensitivity: 0.5
Found custom wake word model: /app/models/albert.ppn
Using custom wake word models
Porcupine initialized successfully
Starting Wyoming Porcupine server on 0.0.0.0:10400
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORCUPINE_ACCESS_KEY` | *required* | Your Picovoice access key |
| `KEYWORDS` | `albert` | Wake word name (must match .ppn filename) |
| `SENSITIVITY` | `0.5` | Detection sensitivity (0.0-1.0) |
| `HOST` | `0.0.0.0` | Bind address |
| `PORT` | `10400` | Wyoming protocol port |

### Sensitivity Tuning

Adjust sensitivity based on your environment:

```yaml
environment:
  - SENSITIVITY=0.3  # Less sensitive - fewer false positives, might miss some
  - SENSITIVITY=0.5  # Default - balanced
  - SENSITIVITY=0.7  # More sensitive - catches more, might have false positives
```

## Home Assistant Integration

### Via UI

1. Go to **Settings → Devices & Services**
2. Click **Add Integration**
3. Search for **Wyoming Protocol**
4. Enter:
   - Host: `192.168.106.20` (or your Unraid IP)
   - Port: `10400`
5. Click **Submit**

### Via Configuration

Add to `configuration.yaml`:

```yaml
wyoming:
  - uri: tcp://192.168.106.20:10400
```

### In Voice Assistant Pipeline

1. Go to **Settings → Voice Assistants**
2. Edit your assistant
3. Set **Wake word** to: `albert`
4. Save changes

## Training Tips for "Albert"

To get the best detection accuracy:

### Recording Environment
- **Quiet room** - minimal background noise
- **Good microphone** - clear audio quality
- **Consistent distance** - 1-2 meters from mic

### Voice Variations
- **Multiple speakers** - different voices, ages, genders
- **Accents** - Luxembourgish and other accents
- **Speeds** - fast, normal, slow pronunciation
- **Volumes** - soft, normal, loud

### Samples Needed
Porcupine's web training typically handles this automatically, but if training locally:
- **Positive samples**: 20-50 recordings of "Albert"
- **Negative samples**: Background noise, other speech

## Troubleshooting

### Error: "ACCESS_KEY environment variable is required"

**Solution**: Set your Picovoice access key
```bash
export PORCUPINE_ACCESS_KEY="your_key_here"
# Or add to .env file
```

### Error: "No custom models found, trying built-in keywords"

**Cause**: The `albert.ppn` file is not in the `./models/` directory

**Solution**:
```bash
# Check if file exists
ls -la models/albert.ppn

# If not, download it from Picovoice Console
# Place in models directory
cp ~/Downloads/albert.ppn ./models/
```

### Error: "keyword 'albert' is not available"

**Cause**: Trying to use "albert" as a built-in keyword (it's not)

**Solution**: You MUST train and download the custom `albert.ppn` model

### Wake Word Not Detected

1. **Check sensitivity**: Try increasing to 0.7
2. **Check microphone**: Verify Home Assistant is receiving audio
3. **Check logs**: `docker logs ha-wakeword-albert`
4. **Test pronunciation**: Try saying "AL-bert" clearly
5. **Check distance**: Speak 1-2 meters from microphone

### Container Won't Start

```bash
# Check logs
docker logs ha-wakeword-albert

# Rebuild container
docker-compose -f docker-compose-porcupine.yml down
docker-compose -f docker-compose-porcupine.yml up --build -d
```

## File Structure

```
Ha-WakeWord-LU/
├── porcupine-wakeword/
│   ├── wyoming_porcupine.py    # Wyoming protocol server
│   ├── Dockerfile              # Container definition
│   ├── requirements.txt        # Python dependencies
│   └── start.sh               # Startup script
├── models/
│   └── albert.ppn             # Custom wake word model (you create this)
├── docker-compose-porcupine.yml  # Deployment config
├── .env                        # Environment variables (gitignored)
├── README-PORCUPINE.md        # This file
└── Notes/
    └── notes.md               # Project notes
```

## Comparison: Porcupine vs openWakeWord

| Feature | Porcupine | openWakeWord |
|---------|-----------|--------------|
| **Training** | Web-based, automatic | Manual, requires samples |
| **Accuracy** | Very high | Good |
| **CPU Usage** | Very low | Low |
| **Custom Words** | Easy via web interface | Requires TensorFlow training |
| **Cost** | Free tier available | Free |
| **Setup Time** | 5-10 minutes | 1-2 hours (with training) |

## Performance

- **CPU**: <1% on modern CPU
- **RAM**: ~50MB
- **Latency**: <100ms detection time
- **False Positives**: Very low with proper training

## Advanced: Multiple Wake Words

You can detect multiple wake words simultaneously:

```yaml
environment:
  - KEYWORDS=albert jarvis computer
```

Then place corresponding `.ppn` files:
```
models/
├── albert.ppn
├── jarvis.ppn
└── computer.ppn
```

Built-in keywords (computer, jarvis) don't need `.ppn` files.

## Updating

### Update Access Key
```bash
# Edit .env file
nano .env
# Change PORCUPINE_ACCESS_KEY value

# Restart container
docker-compose -f docker-compose-porcupine.yml restart
```

### Update Wake Word Model
```bash
# Replace albert.ppn with newly trained version
cp ~/Downloads/albert_v2.ppn ./models/albert.ppn

# Restart container
docker-compose -f docker-compose-porcupine.yml restart
```

## Resources

- **Picovoice Console**: https://console.picovoice.ai/
- **Porcupine Documentation**: https://picovoice.ai/docs/porcupine/
- **Wyoming Protocol**: https://github.com/rhasspy/wyoming
- **Home Assistant Voice**: https://www.home-assistant.io/voice_control/

## Support

- GitHub Issues: [Create an issue](https://github.com/yourusername/Ha-WakeWord-LU/issues)
- Home Assistant Community: [Voice Assistant Forum](https://community.home-assistant.io/c/voice-assistant/)

## License

MIT License

## Credits

- [Picovoice Porcupine](https://picovoice.ai/) - Wake word engine
- [Wyoming Protocol](https://github.com/rhasspy/wyoming) - Voice protocol
- Home Assistant Community

---

**Version**: 1.0-porcupine
**Wake Word**: Albert
**Language**: Luxembourgish
**Status**: Ready for deployment
