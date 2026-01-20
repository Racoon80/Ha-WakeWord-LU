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
