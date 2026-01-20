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
- **Network**: br0.106 (192.168.106.51:10400)
- **Path**: /mnt/user/appdata/ai
- **GPU**: Available for training

## Implementation Progress

### Files Created

#### Docker Configuration
- `docker-compose.yml` - Production deployment with Wyoming protocol
  - Container: ha-wakeword-lu
  - Port: 10400
  - Network: br0.106 with static IP 192.168.106.51
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

## Next Steps
1. Collect audio samples of "Roberto" (100-200 samples)
2. Collect background/negative samples (500-1000 samples)
3. Train the wake word model using GPU container
4. Deploy trained model to openWakeWord container
5. Test with Home Assistant
6. Create GitHub repository
7. Push code and create v1.0 release
