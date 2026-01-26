# Ha-WakeWord-LU Project Notes

## Project Created: 2026-01-20

### Project Structure
- Project Name: Ha-WakeWord-LU
- Location: L:\Projects\Ha-WakeWord-LU
- AI Sessions: L:\Projects\Ha-WakeWord-LU\ai
- Notes: L:\Projects\Ha-WakeWord-LU\Notes

### Project Goal
Create a Luxembourgish wake word detector for Home Assistant that responds to "Roberto" using the Wyoming protocol and openWakeWord engine.

### Technical Specifications
- **Wake Word**: Roberto (Luxembourgish)
- **Engine**: openWakeWord
- **Protocol**: Wyoming
- **Deployment**: Docker on Unraid
- **Network**: br0.106 (192.168.106.20:10400)
- **Path**: /mnt/user/appdata/ai
- **GPU**: Available for training

## Implementation Progress

### Files Created

#### Docker Configuration
- `docker-compose.yml` - Production deployment with Wyoming protocol
  - Container: ha-wakeword-lu
  - Port: 10400
  - Network: br0.106 with static IP 192.168.106.20
  - Custom model directory: /mnt/user/appdata/ai/roberto-models

- `docker-compose-training.yml` - GPU-accelerated training container
  - TensorFlow with NVIDIA GPU support
  - Training workspace: /mnt/user/appdata/ai/roberto-training

#### Training Tools
- `training/train_roberto.py` - Model training script
  - Configures model name: roberto_lb
  - Sample rate: 16kHz
  - Training epochs: 100

- `training/collect_samples.py` - Interactive audio collection tool
  - Records 2-second samples at 16kHz mono
  - Separates positive (Roberto) and negative (background) samples
  - Recommended: 100-200 positive, 500-1000 negative samples

- `training/requirements.txt` - Python dependencies for training

#### Documentation
- `README.md` - Comprehensive project documentation
  - Installation instructions
  - Training guide
  - Home Assistant integration
  - Troubleshooting section

## GitHub Repository
- **URL**: https://github.com/Racoon80/Ha-WakeWord-LU
- **Release**: v1.0 - https://github.com/Racoon80/Ha-WakeWord-LU/releases/tag/v1.0
- **Status**: Public repository with complete documentation

## Deployment
- **Script**: `deploy.sh` created for automated Unraid deployment
- **Target**: 192.168.10.100:/mnt/user/appdata/ai/Ha-WakeWord-LU
- **Models Path**: /mnt/user/appdata/ai/roberto-models
- **Service Endpoint**: tcp://192.168.106.20:10400

## ✅ DEPLOYMENT COMPLETE

### What's Running
- **Container**: ha-wakeword-lu
- **Status**: RUNNING on Unraid
- **IP**: 192.168.106.20:10400
- **Protocol**: Wyoming
- **Service**: READY and accepting connections

### What's Deployed
✅ Project files copied to /mnt/user/appdata/ai/Ha-WakeWord-LU
✅ Docker container running with Wyoming protocol
✅ Network configuration fixed (br0.106 with valid IP)
✅ Custom models directory created
✅ Training environment ready
✅ GitHub repository with v1.0 release
✅ Complete documentation (README + DEPLOYMENT-STATUS)

## ⏳ Pending - Requires User Involvement

These steps CANNOT be automated and require the user:

### 1. Collect Audio Samples
- Record 100-200 samples of saying "Roberto" in Luxembourgish
- Record 500-1000 background/negative samples
- Use `training/collect_samples.py` or record manually
- **WHY**: AI cannot generate voice samples; real human voice needed

### 2. Train the Model
- Upload samples to Unraid
- Run: `docker-compose -f docker-compose-training.yml up`
- Copy trained model to /mnt/user/appdata/ai/roberto-models/
- **WHY**: Training requires the audio samples from step 1

### 3. Configure Home Assistant
- Go to https://ha.racoon.lu
- Settings → Devices & Services → Add Integration
- Add Wyoming Protocol integration
- Host: 192.168.106.20, Port: 10400
- **WHY**: User denied browser automation access

## Summary

**Everything that CAN be automated HAS been completed:**
- ✅ Code development
- ✅ GitHub repository & release
- ✅ Unraid deployment
- ✅ Docker container running
- ✅ Wyoming service active
- ✅ Network configured
- ✅ Training environment ready
- ✅ Documentation complete

**What CANNOT be automated (requires human):**
- ⏳ Recording voice samples (needs physical voice)
- ⏳ Model training (needs samples first)
- ⏳ Home Assistant UI configuration (browser access denied)

See `DEPLOYMENT-STATUS.md` for detailed next steps.

---

## Porcupine "Albert" Implementation

### Date: 2026-01-26

### Alternative Wake Word Approach

Added **Porcupine by Picovoice** implementation as an alternative to openWakeWord:

#### Why Porcupine?
- **Easier setup**: Web-based training (no manual sample collection)
- **Faster deployment**: Train and deploy in 10 minutes
- **Higher accuracy**: Industry-leading wake word detection
- **Lower CPU usage**: Highly optimized on-device processing
- **Custom wake words**: Easy to create "Albert" or other Luxembourgish words

#### Wake Word: "Albert"
- Chosen for Luxembourgish assistant
- Could reference Albert II, Grand Duke of Luxembourg
- Short, distinct, easy to pronounce
- Works well with Porcupine's algorithms

### Files Created for Porcupine

#### Porcupine Implementation
- `porcupine-wakeword/wyoming_porcupine.py` - Wyoming protocol server for Porcupine
  - Event handling for Wyoming protocol
  - Audio chunk processing (16kHz, 16-bit PCM)
  - Frame-based detection (512 samples per frame)
  - Support for custom and built-in wake words

- `porcupine-wakeword/requirements.txt` - Dependencies
  - wyoming==1.5.2
  - pvporcupine>=3.0.0

- `porcupine-wakeword/Dockerfile` - Container with Python 3.11 and audio support

- `porcupine-wakeword/start.sh` - Startup script
  - Access key validation
  - Auto-detection of custom .ppn models
  - Fallback to built-in keywords if no custom models

#### Deployment Configuration
- `docker-compose-porcupine.yml` - Porcupine-specific deployment
  - Container: ha-wakeword-albert
  - Port: 10400 (same as openWakeWord)
  - Network: br0.106 with IP 192.168.106.20
  - Volume mount for custom models: ./models:/app/models
  - No GPU needed (CPU only)

#### Documentation
- `README-PORCUPINE.md` - Comprehensive Porcupine documentation
  - Why "Albert" for Luxembourgish
  - Complete setup guide
  - Training instructions via Picovoice Console
  - Home Assistant integration
  - Troubleshooting guide
  - Comparison with openWakeWord

- `SETUP-ALBERT.md` - Quick setup guide (10-minute deployment)
  - Step-by-step Picovoice account creation
  - Access key generation
  - Wake word training walkthrough
  - Unraid deployment (manual + script options)
  - Home Assistant configuration
  - Testing procedures

### Setup Requirements

#### Prerequisites
1. **Picovoice Access Key** (Free)
   - Sign up: https://console.picovoice.ai/
   - Create access key
   - Set as: `PORCUPINE_ACCESS_KEY`

2. **Custom Wake Word Model** (albert.ppn)
   - Train at Picovoice Console
   - Download .ppn file
   - Place in `./models/albert.ppn`

#### Built-in Wake Words Available
If you don't want to train "Albert", Porcupine includes:
- computer, jarvis, alexa
- hey google, ok google, hey siri
- picovoice, porcupine
- bumblebee, grasshopper, terminator
- americano, blueberry, grapefruit

### Deployment Options

You now have TWO wake word implementations:

#### Option 1: openWakeWord with "Roberto"
```bash
docker-compose up -d  # Uses docker-compose.yml
```
- Custom TensorFlow training
- Manual sample collection
- Better for highly customized words

#### Option 2: Porcupine with "Albert"
```bash
docker-compose -f docker-compose-porcupine.yml up -d
```
- Web-based training
- Faster setup (10 minutes)
- Higher accuracy
- Recommended for quick deployment

### Quick Start: Porcupine "Albert"

1. **Get Access Key**: https://console.picovoice.ai/ → Access Keys
2. **Train "Albert"**: Porcupine section → Train Wake Word
3. **Download Model**: Save `albert.ppn` to `./models/`
4. **Create .env**: `echo "PORCUPINE_ACCESS_KEY=your_key" > .env`
5. **Deploy**: `docker-compose -f docker-compose-porcupine.yml up -d`
6. **Configure HA**: Settings → Devices & Services → Wyoming Protocol
7. **Test**: Say "Albert" and issue command in Luxembourgish

### Next Steps for Porcupine

- [ ] Sign up for Picovoice account
- [ ] Generate access key
- [ ] Train "Albert" wake word via web interface
- [ ] Download albert.ppn model
- [ ] Deploy to Unraid using docker-compose-porcupine.yml
- [ ] Add to Home Assistant
- [ ] Test with Luxembourgish voice pipeline

### Status: Ready for Deployment

All Porcupine code is complete and ready. User just needs to:
1. Create Picovoice account (2 min)
2. Train "Albert" wake word (5 min)
3. Deploy container (5 min)

**Total setup time: ~15 minutes** (vs hours for openWakeWord training)
