# Ha-WakeWord-LU Deployment Status

## ✅ Completed

### GitHub Repository
- **URL**: https://github.com/Racoon80/Ha-WakeWord-LU
- **Release**: v1.0
- **Status**: Public repository with complete documentation

### Unraid Deployment
- **Container Name**: ha-wakeword-lu
- **Image**: rhasspy/wyoming-openwakeword:latest
- **Status**: ✅ RUNNING
- **IP Address**: 192.168.106.20
- **Port**: 10400
- **Network**: br0.106 (macvlan)
- **Protocol**: Wyoming
- **Deployment Path**: /mnt/user/appdata/ai/Ha-WakeWord-LU

### File Structure on Unraid
```
/mnt/user/appdata/ai/
├── Ha-WakeWord-LU/           # Main project directory
│   ├── docker-compose.yml
│   ├── docker-compose-training.yml
│   ├── README.md
│   ├── deploy.sh
│   ├── .gitignore
│   └── training/
│       ├── collect_samples.py
│       ├── train_roberto.py
│       └── requirements.txt
├── roberto-models/            # Custom wake word models (EMPTY - needs training)
└── roberto-training/          # Training workspace directory
```

### Wyoming Service
- **Endpoint**: tcp://192.168.106.20:10400
- **Status**: ✅ READY and accepting connections
- **Custom Models Directory**: /mnt/user/appdata/ai/roberto-models
- **Debug Mode**: Enabled

## ⏳ Pending - Requires User Action

### 1. Audio Sample Collection
**Status**: NOT STARTED
**Required**: Record audio samples of "Roberto" in Luxembourgish

**Steps**:
```bash
# On a machine with microphone access
cd /path/to/Ha-WakeWord-LU/training
pip install -r requirements.txt
python collect_samples.py
```

**Requirements**:
- 100-200 positive samples (saying "Roberto")
- 500-1000 negative samples (background noise, other speech)
- Different voices, accents, environments
- Varying speaking speeds and volumes

### 2. Model Training
**Status**: NOT STARTED (waiting for audio samples)
**Environment**: GPU-accelerated training container ready on Unraid

**Steps**:
```bash
# SSH to Unraid
ssh root@192.168.10.100

# Navigate to project directory
cd /mnt/user/appdata/ai/Ha-WakeWord-LU

# Start training container
docker-compose -f docker-compose-training.yml up

# Or train locally after collecting samples
cd training
python train_roberto.py --train

# Copy trained model to deployment directory
cp training/models/roberto_lb.tflite /mnt/user/appdata/ai/roberto-models/

# Restart wake word service
docker-compose restart
```

### 3. Home Assistant Integration
**Status**: NOT CONFIGURED
**Service Ready**: Wyoming service is accessible at tcp://192.168.106.20:10400

**Manual Configuration Steps**:
1. Open Home Assistant: https://ha.racoon.lu
2. Go to **Settings** → **Devices & Services**
3. Click **Add Integration**
4. Search for **Wyoming Protocol**
5. Enter:
   - Host: `192.168.106.20`
   - Port: `10400`
6. Complete the setup wizard
7. The wake word service will appear as a device

**Alternative - Configuration via YAML** (if preferred):
Add to `configuration.yaml`:
```yaml
wyoming:
  - uri: tcp://192.168.106.20:10400
```
Then restart Home Assistant.

## 📊 System Overview

### Existing Services on br0.106 Network
- 192.168.106.7 - Existing openWakeWord (with Alexa model)
- 192.168.106.8 - OllamaUI
- 192.168.106.10 - LibreTranslate
- 192.168.106.15 - Luxembourgish-FishSpeech-TTS
- 192.168.106.20 - **Ha-WakeWord-LU (Roberto)** ← NEW

### Training Environment
- **GPU**: Available on Unraid
- **Framework**: TensorFlow with NVIDIA GPU support
- **Training Container**: docker-compose-training.yml
- **Workspace**: /mnt/user/appdata/ai/roberto-training

## 🔄 Next Steps

1. **Collect Audio Samples**
   - Record "Roberto" samples (100-200)
   - Record background/negative samples (500-1000)
   - Use `collect_samples.py` tool or record manually

2. **Train the Model**
   - Upload samples to Unraid
   - Run training container
   - Validate model performance

3. **Deploy Model**
   - Copy trained model to roberto-models directory
   - Restart ha-wakeword-lu container
   - The service will automatically load the model

4. **Configure Home Assistant**
   - Add Wyoming Protocol integration
   - Configure voice assistant to use Roberto wake word
   - Test detection

5. **Test & Tune**
   - Test wake word detection in various conditions
   - Adjust threshold if needed (currently 0.5)
   - Collect more samples if detection is poor

## 📝 Notes

- The Wyoming service is running but WITHOUT a wake word model
- Once the roberto_lb.tflite model is placed in /mnt/user/appdata/ai/roberto-models/, the service will load it automatically
- The container restarts policy is `unless-stopped` for reliability
- Debug logging is enabled for troubleshooting
- Network uses macvlan driver with static IP assignment

## 🔗 Resources

- **GitHub Repository**: https://github.com/Racoon80/Ha-WakeWord-LU
- **Wyoming Protocol**: https://github.com/rhasspy/wyoming
- **openWakeWord**: https://github.com/dscripka/openWakeWord
- **Home Assistant Voice**: https://www.home-assistant.io/voice_control/

## ⚙️ Troubleshooting

### Check Container Status
```bash
ssh root@192.168.10.100
docker ps | grep ha-wakeword-lu
docker logs ha-wakeword-lu
```

### Test Wyoming Connection
```bash
nc -zv 192.168.106.20 10400
```

### Restart Container
```bash
cd /mnt/user/appdata/ai/Ha-WakeWord-LU
docker-compose restart
```

### View Custom Models
```bash
ls -la /mnt/user/appdata/ai/roberto-models/
```

---

**Last Updated**: 2026-01-20
**Deployment Status**: ✅ Service Running | ⏳ Awaiting Model Training
